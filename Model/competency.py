"""
competency.py contains the class for a tutor's competency.
"""
import popups
from api_constants import *


class Competency:
    """
    Competencies assists bids determining whether a tutor is suitable to 
    teach a student. A tutor can teach a student only if the tutor is
    two levels above.
    """

    def __init__(self, owner_id, subject_id, level):
        if not owner_id:
            return  # raise exception
        if not subject_id:
            return  # raise exception
        if not level:
            return  # raise exception

        response = requests.post(
            url=competency_url,
            headers={
                "Authorization": my_api_key
            },
            json={
                "ownerId": owner_id,
                "subjectId": subject_id,
                "level": level
            }
        )
        if response.status_code == ApiCode.STATUS_SUCCESS.value:
            self.competency_id = None
            self.owner_id = owner_id
            self.subject_id = subject_id
            self.level = level

            popups.PopupSuccess("New Competency successfully created")
        else:
            popups.PopupError("Error: " + str(response.json()["message"]))

    def get_owner_id(self):
        return self.owner_id

    def set_owner_id(self, new_id):
        for u in api_get(user_url):
            if u["id"] == new_id:
                self.owner_id = new_id

    def get_subject_id(self):
        return self.subject_id

    def set_subject_id(self, new_id):
        for s in api_get(subject_url):
            if s["id"] == new_id:
                self.subject_id = new_id

    def get_level(self):
        return self.level

    def set_level(self, new_level):
        if new_level:
            if new_level.isdigit() and new_level > 0:
                self.level = new_level

    def patch(self, data):
        """Update competency information onto the API."""
        if not self.competency_id:
            return  # no competency id

        response = requests.patch(
            url=competency_url + "/" + self.competency_id,
            headers={
                "Authorization": my_api_key
            },
            json=data  # TODO: TEST before deployment
        )
        if response.status_code == ApiCode.STATUS_OK:
            popups.PopupSuccess("Competency successfully updated")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def delete(self):
        """Delete competency information on the API."""
        if not self.competency_id:
            return  # no competency id

        response = requests.delete(
            url=competency_url + "/" + self.competency_id,
            headers={
                "Authorization": my_api_key
            }
        )
        if response.status_code == ApiCode.STATUS_DELETED.value:
            popups.PopupSuccess("Competency successfully deleted")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))
