"""
abstract_popup.py defines the attributes and methods required for a popup.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from abc import ABC, abstractmethod
from tkinter import *


class AbstractPopup(ABC):
    """
    Create a popup window.
    """

    @abstractmethod
    def __init__(self, message):
        # Need to define self.title in subclasses
        pass
    
    def create(self):
        """Construct the popup window with title and message.

        Should not be overwritten by subclasses. This method should cover the
        base construction of a popup window.
        """
        popup = Tk()
        popup.title(self.title)

        popup_message = Label(popup, text=self.message)
        popup_message.pack(side="top", fill="both", expand=True)

        popup_button = Button(popup, text="Okay", command=popup.destroy)
        popup_button.pack()

        popup.mainloop()