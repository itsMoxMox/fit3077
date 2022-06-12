"""
bid_list_controller.py contains the code for handling logic behind the bid_list frames
including interaction with the API
"""

__author__ = "Max Chan, Nick Chua"

import popups
from Model.message import Message
from api_constants import *
from datetime import *


class BidListController:
    def __init__(self):
        pass

    def get_bids(self, user_type, user):
        temp = []
        out = []
        for bid in api_get(bid_url):
            expiration_date = datetime.fromisoformat(
                bid["dateCreated"][:-1]
            ) + timedelta(minutes=30)

            if datetime.utcnow().isoformat() < expiration_date.isoformat():
                temp.append(bid)
        if user_type == "student":
            for bid in temp:
                if bid["initiator"]["id"] == user.get_id():
                    out.append(bid)
        elif user_type == "tutor":
            for bid in temp:
                if not bid["dateClosedDown"]:
                    out.append(bid)
        else:  # get all bids as default
            out = [bid for bid in temp]
        return out

    def send_offer(self, frame, offer_mins, offer_num, offer_rate, offer_comments, offer_duration):
        """Send an offer to the student based on tutor's given rates."""
        for value in [offer_mins, offer_num, offer_rate]:
            if not value.get().isdigit():
                print(value["text"] + " must be a number")
                return

        bid_data = frame.select_item_treeview()
        if not bid_data:
            return
        if self.check_valid_competency(frame, bid_data):
            Message(bid_data["id"],
                    frame.controller.user.get_id(),
                    datetime.utcnow().isoformat() + "Z",
                    offer_comments.get(),
                    {
                        "minsOffer": offer_mins.get(),
                        "numsOffer": offer_num.get(),
                        "rateOffer": offer_rate.get(),
                        "durationOffer": offer_duration.get() or 6  # defaults to 6 months
                    }
            )

    def check_valid_competency(self, frame, bid_data):
        """Assess if tutor is qualified to teach student."""
        qualified = False
        for c in frame.controller.user.get_competencies():
            if c["subject"]["id"] == bid_data["subject"]["id"]:
                if (
                        c["level"]
                        >= int(bid_data["additionalInfo"]["tutor_competency"]) + 2
                ):
                    qualified = True
        if not qualified:
            popups.PopupError("You are not qualified to teach this student")
            return False
        return True

    def buyout(self, frame):
        """Buy the contract and close the auction."""
        bid_data = frame.select_item_treeview()
        if not bid_data:
            return

        count = 0
        for c in api_get(contract_url):
            if c["firstParty"]["id"] == bid_data["initiator"]["id"]:
                count += 1
                if count >= 5:
                    popups.PopupError("This user cannot form any more contracts")


        if self.check_valid_competency(frame, bid_data):
            # Buyout the contract
            response = requests.post(
                url=contract_url,
                headers={"Authorization": my_api_key},
                json={
                    "firstPartyId": bid_data["initiator"]["id"],
                    "secondPartyId": frame.controller.user.get_id(),
                    "subjectId": bid_data["subject"]["id"],
                    "dateCreated": datetime.utcnow().isoformat() + "Z",
                    "expiryDate": (
                        datetime.utcnow() + timedelta(
                            days=30 * int(bid_data["additionalInfo"]["contract_duration"])
                        )
                    ).isoformat() + "Z",
                    "paymentInfo": {},
                    "lessonInfo": {
                        "sessions_per_week": bid_data["additionalInfo"][
                            "sessions_per_week"
                        ],
                        "minutes_per_session": bid_data["additionalInfo"][
                            "minutes_per_session"
                        ],
                        "hourly_rate": bid_data["additionalInfo"][
                            "preferred_hourly_rate"
                        ],
                    },
                    "additionalInfo": {},
                },
            )
            if response.status_code != ApiCode.STATUS_SUCCESS.value:
                # If response failed
                popups.PopupError(response.json()["message"])
                return

            # Close the auction
            response = requests.post(
                url=bid_url + "/" + bid_data["id"] + "/close-down",
                headers={
                    "Authorization": my_api_key,
                },
                json={"dateClosedDown": datetime.utcnow().isoformat() + "Z"},
            )
            if response.status_code == ApiCode.STATUS_OK.value:
                popups.PopupSuccess("Successfully Formed a contract.")
            else:
                popups.PopupError(response.json()["message"])
            frame.update_frame()

    def monitor(self, user):
        """ Gets the current selected bid's ID and adds that to the subscribed list"""
        bid_data = self.select_item_treeview()
        if not bid_data:
            return
        if bid_data["id"] in user.subscribed_bids:
            user.unsubscribe(bid_data["id"])
        if bid_data["type"] != "open":
            popups.PopupError("You can only subscribe to open bids")
            return
        user.subscribe_new_bid(bid_data["id"])

    def finalise_offer(self, frame):
        """Students' version of contract finalisation."""

        if len(frame.controller.user.contracts) >= 5:
            popups.PopupError("You cannot form more than 5 contracts")

        offer = frame.select_item_listbox()
        bid = frame.select_item_treeview()

        response = requests.post(
            url=contract_url,
            headers={"Authorization": my_api_key},
            json={
                "firstPartyId": frame.controller.user.get_id(),
                "secondPartyId": offer["poster"]["id"],
                "subjectId": bid["subject"]["id"],
                "dateCreated": datetime.utcnow().isoformat() + "Z",
                "expiryDate": (
                    datetime.utcnow() + timedelta(days=30 * int(offer["additionalInfo"]["durationOffer"]))
                ).isoformat() + "Z",
                "paymentInfo": {},
                "lessonInfo": {
                    "sessions_per_week": offer["additionalInfo"]["numsOffer"],
                    "minutes_per_session": offer["additionalInfo"]["minsOffer"],
                    "hourly_rate": offer["additionalInfo"]["rateOffer"],
                },
                "additionalInfo": {},
            },
        )
        if response.status_code == ApiCode.STATUS_SUCCESS.value:
            popups.PopupSuccess("Successfully Formed a contract.")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))
            return
        response = requests.post(
            url=bid_url + "/" + bid["id"] + "/close-down",
            headers={
                "Authorization": my_api_key,
            },
            json={"dateClosedDown": datetime.utcnow().isoformat() + "Z"},
        )
        if response.status_code == ApiCode.STATUS_SUCCESS:
            frame.update_bids()
            popups.PopupSuccess("Contract successfully finalised")
        else:
            popups.PopupError("Something went wrong, error code: " + str(response.status_code))
