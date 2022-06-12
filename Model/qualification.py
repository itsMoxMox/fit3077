"""
qualification.py contains the class for a competency(s)
"""
import popups
from api_constants import *


class Qualification:
    """
    Tutor's qualifications determines a tutor's competency.
    """

    def __init__(self, title, description, verified, owner_id):
        if not title:
            return  # raise exception
        if not description:
            return  # raise exception
        if not verified:
            return  # raise exception
        if not owner_id:
            return  # raise exception

        response = requests.post(
            url=qualification_url,
            headers={
                "Authorization": my_api_key
            },
            json={
                "title": title,
                "description": description,
                "verified": verified,
                "ownerId": owner_id
            }
        )
        if response.status_code == ApiCode.STATUS_SUCCESS.value:
            self.qualification_id = None
            self.title = title
            self.description = description
            self.verified = verified
            self.owner_id = owner_id

            popups.PopupSuccess("New Qualification successfully created")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def get_title(self):
        return self.title

    def set_title(self, new_title):
        self.title = new_title

    def get_description(self):
        return self.description

    def set_description(self, new_desc):
        self.description = new_desc

    def get_verified(self):
        return self.verified

    def set_verified(self, new_verified):
        if isinstance(new_verified, bool):
            self.verified = new_verified

    def get_owner_id(self):
        return self.owner_id

    def set_owner_id(self, new_id):
        for u in api_get(user_url):
            if u["id"] == new_id:
                self.owner_id = new_id

    def patch(self, data):
        """Update qualification information onto the API."""
        if not self.qualification_id:
            return  # no competency id

        response = requests.patch(
            url=qualification_url + "/" + self.qualification_id,
            headers={
                "Authorization": my_api_key
            },
            json=data  # TODO: TEST before deployment
        )
        if response.status_code == ApiCode.STATUS_OK:
            popups.PopupSuccess("Qualification successfully updated")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def delete(self):
        """Delete qualification information on the API."""
        if not self.qualification_id:
            return  # no competency id

        response = requests.delete(
            url=qualification_url + "/" + self.qualification_id,
            headers={
                "Authorization": my_api_key
            }
        )
        if response.status_code == ApiCode.STATUS_DELETED.value:
            popups.PopupSuccess("Qualification successfully deleted")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))
