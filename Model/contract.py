"""
Contract.py contains the class for a contract(s)
"""

__author__ = "Max Chan, Nick Chua"

from datetime import *

import popups
from api_constants import *
import requests

class Contract:
    """
    Contracts establish a written agreement between a tutor and their
    students. These outline the rate of tutoring and the parties
    involved.
    """

    def __init__(self, first_id, second_id, subj_id, date_created, exp_date,
                 payment_info, lesson_info, additional_info, data, contract_id=None):
        self.contract_id = contract_id
        self.first_id = first_id
        self.second_id = second_id
        self.subject_id = subj_id
        self.date_created = date_created
        self.date_expiry = exp_date
        self.payment_info = payment_info
        self.lesson_info = lesson_info
        self.additional_info = additional_info
        self.data = data

    def post(self, first_id, second_id, subj_id, date_created, exp_date,
             payment_info, lesson_info, additional_info):
        response = requests.post(
            url=contract_url,
            headers={
                "Authorization": my_api_key
            },
            json={
                "firstPartyId": first_id,
                "secondPartyId": second_id,
                "subjectId": subj_id,
                "dateCreated": date_created,
                "expiryDate": exp_date,
                "paymentInfo": payment_info,
                "lessonInfo": lesson_info,
                "additionalInfo": additional_info
            }
        )
        if response.status_code == ApiCode.STATUS_SUCCESS:
            # Signs on submission because the tutors consent to signing a signature
            # by sending an offer.
            now = datetime.utcnow().isoformat() + "Z"
            self.sign(now)
            self.date_signed = now
            popups.PopupSuccess("New Contract successfully created")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def get_id(self):
        if self.contract_id:
            return self.contract_id
        else:
            for c in api_get(contract_url):
                if c["firstParty"]["id"] == self.first_id and c["secondParty"]["id"] == self.second_id and \
                        c["dateCreated"] == self.date_created:
                    self.contract_id = c["id"]
                    return self.contract_id

    def get_first_id(self):
        return self.first_id

    def set_first_id(self, new_id):
        if new_id != self.second_id:
            for u in api_get(user_url):
                if u["id"] == new_id:
                    self.first_id = new_id

    def get_second_id(self):
        return self.first_id

    def set_second_id(self, new_id):
        if new_id != self.first_id:
            for u in api_get(user_url):
                if u["id"] == new_id:
                    self.second_id = new_id

    def get_subject_id(self):
        return self.subject_id

    def set_subject_id(self, new_id):
        for s in api_get(subject_url):
            if s["id"] == new_id:
                self.subject_id = new_id

    def patch(self, data):
        """Update contract information onto the API."""
        if not self.contract_id:
            return  # no contract id
        response = requests.patch(
            url=contract_url + "/" + self.contract_id,
            headers={
                "Authorization": my_api_key
            },
            json=data
        )
        if response.status_code == ApiCode.STATUS_OK.value:
            popups.PopupSuccess("Contract successfully updated")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def delete(self):
        """Delete contract information on the API."""
        if not self.contract_id:
            return  # no contract id
        response = requests.delete(
            url=contract_url + "/" + self.contract_id,
            headers={
                "Authorization": my_api_key
            }
        )
        if response.status_code == ApiCode.STATUS_DELETED.value:
            popups.PopupSuccess("Contract successfully deleted")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def sign(self, date_signed):
        """Establish the beginning of the contract by signing its date."""
        if not self.contract_id:
            return  # no contract id
        response = requests.post(
            url=contract_url + "/" + self.contract_id + "/sign",
            headers={
                "Authorization": my_api_key
            },
            json={
                "dateSigned": date_signed
            }
        )
        if response.status_code == ApiCode.STATUS_OK.value:
            popups.PopupSuccess("Contract successfully signed")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def terminate(self, date_terminated):
        """Cease the contract by signing the ending date."""
        if not self.contract_id:
            return  # no contract id
        response = requests.post(
            url=contract_url + "/" + self.contract_id + "/terminate",
            headers={
                "Authorization": my_api_key
            },
            json={
                "terminationDate": date_terminated
            }
        )
        if response.status_code == ApiCode.STATUS_OK.value:
            popups.PopupSuccess("Contract successfully terminated")
        else:
            popups.PopupError("Something went wrong, Error: " + str(response.status_code))
