"""
contract_list_controller.py is the controller file containing logic code for the contract list frame
"""

__author__ = "Max Chan, Nick Chua"

from api_constants import *
from datetime import *
import popups

class ContractListController:
    def __init__(self):
        self.contracts = []

    def get_contracts(self, user):
        self.contracts = user.pull_contracts()

    def renew_contract(self, contract, tutor_username, duration, terms):
        if not contract:
            return

        curr_terms = (contract.lesson_info["sessions_per_week"],
                      contract.lesson_info["minutes_per_session"],
                      contract.lesson_info["hourly_rate"])

        new_tutor_id = ""
        if tutor_username:
            # search for competencies
            for c in api_get(competency_url):
                # if the id OR username matches the input query and the subject matches
                if (c["owner"]["userName"] == tutor_username or c["owner"]["id"] == tutor_username) \
                        and c["subject"]["id"] == contract.subject_id:
                    if c["level"] < int(terms[2] or curr_terms[2]) + 2:
                        popups.PopupError("This tutor is not qualified to teach you")
                        return  # not qualified to teach

            for u in api_get(user_url):
                if u["userName"] == tutor_username or u["id"] == tutor_username:
                    new_tutor_id = u["id"]

        response = contract.patch({
            "secondPartyId": new_tutor_id or contract.second_id,
            "expiryDate": str(datetime.fromisoformat(contract.date_expiry[:-1]) + timedelta(days=30 * int(duration or 3))) + "Z",
            "lessonInfo": {
                "sessions_per_week": terms[0] or curr_terms[0],
                "minutes_per_session": terms[1] or curr_terms[1],
                "hourly_rate": terms[2] or curr_terms[2]
            },
        })

