"""
abstract_window.py contains an abstract class of how a window should operate.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from tkinter import *
from abc import ABC


class AbstractWindow(Tk, ABC):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Instance attributes
        self.user = None
        self.frames = {}

        self.option_add("*Font", "Helvetica 12")  # Font

    def show_frame(self, screen_name):
        """
        Display frame based on given screen_name.
        :param screen_name:  name of the frame object to display
        """
        frame = self.frames[screen_name]
        frame.update_frame()
        frame.tkraise()
