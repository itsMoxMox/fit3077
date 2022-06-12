"""
popup_error.py creates a popup which explains its error message.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from tkinter import *

# File imports
from .abstract_popup import AbstractPopup

class PopupError(AbstractPopup):
    """
    Create a popup window that explains the user as to what its error
    message is. Should not be confused with Python's built-in exceptions
    and errors.
    """

    def __init__(self, message):
        self.title = "ERROR"
        self.message = message
        self.create()
