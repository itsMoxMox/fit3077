"""
message.py contains the class for a message(s)
"""

import popups
from api_constants import *

class Message:
    """
    Sends messages between tutors and students to communicate tutoring rates
    and student requirements.
    """

    def __init__(self, bid_id, poster_id, date_posted, content, additional_info):
        if not bid_id:
            return  # raise exception
        if not poster_id:
            return  # raise exception

        response = requests.post(
            url=message_url,
            headers={
                "Authorization": my_api_key
            },
            json={
                "bidId": bid_id,
                "posterId": poster_id,
                "datePosted": date_posted,
                "content": content,
                "additionalInfo": additional_info  # TODO: test this
            }
        )
        if response.status_code == ApiCode.STATUS_SUCCESS.value:
            self.message_id = None
            self.bid_id = bid_id
            self.poster_id = poster_id
            self.date_posted = date_posted
            self.content = content
            self.additional_info = additional_info

            popups.PopupSuccess("New Message successfully created")
        else:
            popups.PopupError("Error: " + str(response.json()["message"]))

    def get_poster_id(self):
        return self.poster_id

    def set_poster_id(self, new_id):
        for u in api_get(user_url):
            if u["id"] == new_id and u["isTutor"]:
                self.poster_id = new_id

    def get_content(self):
        return self.content

    def set_content(self, new_content):
        self.content = new_content

    def patch(self, data):
        """Update message information onto the API."""
        if not self.message_id:
            return  # no message id

        response = requests.patch(
            url=message_url + "/" + self.message_id,
            headers={
                "Authorization": my_api_key
            },
            json=data  # TODO: TEST before deployment
        )
        if response.status_code == ApiCode.STATUS_OK:
            popups.PopupSuccess("Message successfully updated")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))

    def delete(self):
        """Delete messages on the API."""
        if not self.message_id:
            return  # no message id
        response = requests.delete(
            url=message_url + "/" + self.message_id,
            headers={
                "Authorization": my_api_key
            }
        )
        if response.status_code == ApiCode.STATUS_DELETED.value:
            popups.PopupSuccess("Message successfully deleted")
        else:
            popups.PopupError("Something went wrong, Error code: " + str(response.status_code))
