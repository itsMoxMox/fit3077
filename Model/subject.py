"""
subject.py contains the class for a subcject(s)
"""

import popups
from api_constants import *


class Subject:
    """
    The possible lessons that can be taught to students.
    """

    def __init__(self, name, description):
        if not name:
            return  # raise exception
        if not description:
            return  # raise exception

        response = requests.post(
            url=subject_url,
            headers={
                "Authorization": my_api_key
            },
            json={
                "name": name,
                "description": description,
            }
        )
        if response.status_code == ApiCode.STATUS_SUCCESS.value:
            self.subject_id = None
            self.subject_name = name
            self.description = description

            popups.PopupSuccess("New Subject successfully created")
        else:
            popups.PopupError("Error: " + str(response.json()["message"]))

    def get_name(self):
        return self.subject_name

    def set_name(self, new_name):
        self.subject_name = new_name

    def get_description(self):
        return self.description

    def set_description(self, new_desc):
        self.description = new_desc

    def put(self, name, description):
        """Add subject information into the API."""
        if not self.subject_id:
            return  # no subject id

        response = requests.put(
            url=subject_url + "/" + self.subject_id,
            headers={
                "Authorization": my_api_key
            },
            json={
                "name": name,
                "description": description
            }
        )
        if response.status_code == ApiCode.STATUS_OK:
            popups.PopupSuccess("Subject successfully updated")
        else:
            popups.PopupError("Error: " + str(response.json()["message"]))

    def patch(self, name, description):
        """Edit subject information on the API."""
        if not self.subject_id:
            return  # no subject id
        response = requests.patch(
            url=subject_url + "/" + self.subject_id,
            headers={
                "Authorization": my_api_key
            },
            json={
                "name": name,
                "description": description
            }
        )
        if response.status_code == ApiCode.STATUS_OK:
            popups.PopupSuccess("Subject successfully updated")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def delete(self):
        """Delete subject information from the API."""
        if not self.subject_id:
            return  # no subject id
        response = requests.delete(
            url=message_url + "/" + self.subject_id,
            headers={
                "Authorization": my_api_key
            }
        )
        if response.status_code == ApiCode.STATUS_DELETED.value:
            popups.PopupSuccess("Message successfully deleted")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))
