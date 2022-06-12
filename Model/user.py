"""
user.py stores information about the current user accessing the program.
"""

__author__ = "Max Chan, Nick Chua"

# library imports
import jwt

# file imports
import popups
from Model.contract import Contract
from Model.competency import Competency
from Model.qualification import Qualification
from api_constants import *
from datetime import *

class User:
    """
    Handles the processes and information related to the current user.
    """

    def __init__(self, username, web_token):
        # Basic information
        self.id = ""
        self.username = username
        self.web_token = web_token
        self.first_name = ""
        self.family_name = ""
        self.bool_tutor = False
        self.bool_student = False
        # For student-tutors, when they press "Open Auctions" or
        # "View Auctions", acting_as_student carries that information
        # across the screens
        self.acting_as_student = True

        # Lists of tutoring information
        self.qualifications = []
        self.competencies = []
        self.subscribed_bids = []       # list of ids of subbed bids

        # Lists of contract information
        self.contracts = []             # list of all contracts the user has been/is a part of
        self.expiring_contracts = []    # list of contracts expiring next month

    def get_name(self):
        return self.first_name, self.family_name

    def is_tutor(self):
        return self.bool_tutor

    def is_student(self):
        return self.bool_student

    def get_id(self):
        return self.id

    def is_acting_as_student(self):
        return self.acting_as_student

    def get_competencies(self):
        self.pull_competencies()
        return self.competencies

    def get_qualifications(self):
        self.pull_qualifications()
        return self.qualifications

    def set_name(self, firstname, lastname):
        self.first_name = firstname
        self.family_name = lastname

    def set_is_student(self, new_is_student):
        try:
            self.bool_student = new_is_student
            self.pull_competencies()
        except TypeError:
            print("is_student must be a boolean value")

    def set_is_tutor(self, new_is_tutor):
        try:
            self.bool_tutor = new_is_tutor
            self.pull_competencies()
            self.pull_qualifications()
        except TypeError:
            print("is_tutor must be a boolean value")

    def set_id(self, newid):
        self.id = newid

    def set_acting_as_student(self, act_as_student):
        self.acting_as_student = act_as_student

    def jwt_pull(self, token):
        """Request user information from API. If successful, set information
        as the current user.
        """
        response = requests.post(
            url=user_url + "/verify-token",
            headers={
                "Authorization": my_api_key,
            },
            data={"jwt": token},
        )

        if response.status_code == ApiCode.STATUS_OK.value:
            # decode token
            user_info = jwt.decode(
                token,
                "secret",
                algorithms=["HS256"],
                options={"verify_signature": False},
            )
            self.set_name(user_info["givenName"], user_info["familyName"])
            self.set_is_student(user_info["isStudent"])
            self.set_is_tutor(user_info["isTutor"])
            self.set_id(user_info["sub"])
            add_info = api_get(user_url + "/" + self.id)["additionalInfo"]
            self.pull_contracts()
            self.check_expiring_contracts()
            try:
                self.subscribed_bids = add_info["subscribedBids"]
            except KeyError:
                print("User has no subscribed bids")
                return  # this user has no subscribed bids
        else:
            print("Token is invalid")

    def pull_qualifications(self):
        """Request qualification information about this user."""
        for qual in api_get(qualification_url):
            if qual["owner"]["id"] == self.id:
                curr = Qualification(
                    qual["title"],
                    qual["description"],
                    qual["verified"],
                    qual["id"],
                )
                self.qualifications.append(curr)

    def pull_competencies(self):
        """Request competency information about this user."""
        for comp in api_get(competency_url):
            if comp["owner"]["id"] == self.id:
                curr = Competency(
                    comp["id"],
                    comp["subject"],
                    comp["level"]
                )
                self.competencies.append(curr)

    def subscribe_new_bid(self, bid_id):
        """ Add bid id to local list and also updates server data of user to have a copy """
        self.subscribed_bids.append(bid_id)
        response = self.update_api_subs()
        if response.status_code == ApiCode.STATUS_OK.value:
            popups.PopupSuccess("New bid successfully subscribed")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def unsubscribe(self, bid_id):
        self.subscribed_bids.remove(bid_id)
        response = self.update_api_subs()
        if response.status_code == ApiCode.STATUS_OK.value:
            popups.PopupSuccess("Successfully unsubscribed from a bid")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def update_api_subs(self):
        response = requests.patch(
            url=user_url + "/" + self.id,
            headers={
                "Authorization": my_api_key
            },
            json={
                "additionalInfo": {
                    "subscribedBids": self.subscribed_bids
                }
            }

        )
        return response

    def pull_contracts(self):
        """ pull contracts from the API and for each one where the user's id appears, add it to a list"""
        for cont in api_get(contract_url):
            if cont["firstParty"]["id"] == self.id or cont["secondParty"]["id"] == self.id:
                temp = Contract(
                    cont["firstParty"]["id"],
                    cont["secondParty"]["id"],
                    cont["subject"]["id"],
                    cont["dateCreated"],
                    cont["expiryDate"],
                    cont["paymentInfo"],
                    cont["lessonInfo"],
                    cont["additionalInfo"],
                    cont,
                    cont["id"]
                )
                self.contracts.append(temp)
        return self.contracts

    def check_expiring_contracts(self):
        """ check all contracts to see if the month of expiry is the next month, then add that to a list"""
        for c in self.contracts:
            if datetime.fromisoformat(c.date_expiry[:-1]) - datetime.utcnow() < timedelta(days=30):
                self.expiring_contracts.append(c)
        return self.expiring_contracts
