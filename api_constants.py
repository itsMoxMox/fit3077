"""
api_constants.py contains all the values related to interacting with the API, so that all the files
have access to these values.
"""

from enum import Enum
import requests

# API status code constants
class ApiCode(Enum):
    STATUS_OK = 200
    STATUS_SUCCESS = 201
    STATUS_DELETED = 204
    STATUS_UNAUTHORISED = 401
    STATUS_BAD_REQUEST = 400
    STATUS_FORBIDDEN = 403


f = open("apikey.txt")
my_api_key = f.read()
f.close()


# split up each url type to avoid hard-coding in sections
api_url = "https://fit3077.com/api/v2"
user_url = api_url + "/user"
subject_url = api_url + "/subject"
qualification_url = api_url + "/qualification"
competency_url = api_url + "/competency"
contract_url = api_url + "/contract"
bid_url = api_url + "/bid"
message_url = api_url + "/message"


def api_get(url):
    response = requests.get(url=url, headers={"Authorization": my_api_key})
    return response.json()
