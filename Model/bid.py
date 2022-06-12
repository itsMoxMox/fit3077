"""
bid.py contains the class of the Bid.
"""

__author__ = "Max Chan, Nick Chua"

import popups
from api_constants import *

class Bid:
    """
    Bids allow a student to find a suitable tutor based on their offer. Students
    can open either an open or closed bid and select whichever tutor they want.
    """

    def __init__(
        self,
        bid_type,
        initiator_id,
        date_created,
        subject_id,
        mins,
        sessions,
        rate,
        competency,
        duration
    ):
        # Input data checking
        if bid_type not in ["open", "closed"]:
            return

        if not initiator_id:
            return

        if not date_created:
            return

        if not subject_id:
            popups.PopupError("You must select a subject")
            return

        try:
            duration = int(duration)
        except TypeError:
            popups.PopupError("Duration (in months) must be an integer")
            return  # Contract duration must be an integer

        response = requests.post(
            url=bid_url,
            headers={
                "Authorization": my_api_key
            },
            json={
                "type": bid_type,
                "initiatorId": initiator_id,
                "dateCreated": date_created,
                "subjectId": subject_id,
                "additionalInfo": {
                    "minutes_per_session": mins,
                    "sessions_per_week": sessions,
                    "preferred_hourly_rate": rate,
                    "tutor_competency": competency,
                    "contract_duration": duration
                }
            }
        )

        if response.status_code == ApiCode.STATUS_SUCCESS.value:
            self.bid_id = None  # no way to get it from the same request.
            self.bid_type = bid_type
            self.initiator_id = initiator_id
            self.date_created = date_created
            self.subject_id = subject_id
            self.mins = mins
            self.sessions = sessions
            self.rate = rate
            self.competency = competency
            self.duration = int(duration)

            popups.PopupSuccess("New bid successfully created")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def get_type(self):
        return self.bid_type

    def set_type(self, bid_type):
        if bid_type in ["open", "closed"]:
            self.bid_type = bid_type

    def get_initiator_id(self):
        return self.initiator_id

    def set_initiator_id(self, new_id):
        for u in api_get(user_url):
            if u["id"] == new_id and u["isStudent"]:
                self.initiator_id = new_id

    def get_subject_id(self):
        return self.subject_id

    def set_subject_id(self, new_id):
        for s in api_get(subject_url):
            if s["id"] == new_id:
                self.subject_id = new_id

    def get_terms(self):
        return self.mins, self.sessions, self.rate, self.competency

    def get_duration(self):
        return self.duration

    def patch(self, mins, sessions, rate, competency):
        """Update bid information onto the API. This method ensures that
        bidding info is always up to date.
        """
        response = requests.patch(
            url=bid_url + "/" + self.bid_id,
            headers={
                "Authorization": my_api_key
            },
            json={
                "additionalInfo": {
                    "minutes_per_session": mins,
                    "sessions_per_week": sessions,
                    "preferred_hourly_rate": rate,
                    "tutor_competency": competency
                }
            }
        )
        if response.status_code == ApiCode.STATUS_OK.value:
            popups.PopupSuccess("Bid successfully updated")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def delete(self):
        """Delete bid information on the API."""
        if not self.bid_id:
            return  # if the current bid does not have an ID it cannot be deleted.

        response = requests.delete(
            url=bid_url + "/" + self.bid_id,
            headers={
                "Authorization": my_api_key
            }
        )
        if response.status_code == ApiCode.STATUS_DELETED.value:
            popups.PopupSuccess("Bid successfully deleted")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def close(self, date):
        """Update a bid to be closed once a student selects a tutor."""
        if not self.bid_id:
            return  # no bid id
        response = requests.post(
            url=bid_url + "/" + self.bid_id + "/close-downs",
            headers={
                "Authorization": my_api_key
            },
            json={
                "dateClosedDown": date
            }
        )
        if response.status_code == ApiCode.STATUS_OK.value:
            popups.PopupSuccess("Bid successfully closed down")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))
