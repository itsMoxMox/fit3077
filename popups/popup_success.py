"""
popup_success.py creates a popup that indicates the user of a successful
action.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from tkinter import *

# File imports
from .abstract_popup import AbstractPopup

class PopupSuccess(AbstractPopup):
    """
    Create a popup window that notifies the user that their recent action
    on the UI is successful.
    """

    def __init__(self, message):
        self.title = "SUCCESS"
        self.message = message
        self.create()
