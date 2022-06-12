"""
login_controller.py handles the logic for logging in
"""

__author__ = "Max Chan, Nick Chua"

import requests

import popups
from Model.user import User
from api_constants import ApiCode, my_api_key, user_url


class LoginHandler:
    def login(self, username, password, controller):
        """
        Execute login procedure.
        :param controller: Frame controller of its parent object, necessary
        for changing screen
        :param username: Content of the username entry field
        :param password: Content of the password entry field
        :return:
        """

        response = requests.post(
            url=user_url + "/login",
            headers={"Authorization": my_api_key},
            params={"jwt": "true"},
            data={"userName": username, "password": password},
        )
        response_data = response.json()

        # Evaluate API's response
        if response.status_code == ApiCode.STATUS_OK.value:
            controller.user = User(username, response_data["jwt"])
            controller.user.jwt_pull(controller.user.web_token)
            controller.show_frame("MainFrame")
        elif response.status_code == ApiCode.STATUS_FORBIDDEN.value:
            popups.PopupError("The password that you've entered is incorrect.")
        elif response.status_code == ApiCode.STATUS_BAD_REQUEST.value:
            popups.PopupError("Missing Username or Password")
        else:
            unknown_error_message = (
                    "Something went wrong while logging in, Error Code: "
                    + str(response.status_code)
            )

            popups.PopupError(unknown_error_message)
