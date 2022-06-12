"""
abstract_frame.py contains an abstract class of how a frame should operate.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from tkinter import *

# File imports
from abc import ABC, abstractmethod


class AbstractFrame(Frame, ABC):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.user = self.controller.user
        self.cont = None  # frame controller

        # Store an easy reference to Entries, eg. value-checking
        self.entries = {}

    @abstractmethod
    def load_base_ui(self):
        """Load basic elements of the frame; eg. title, buttons. """

    @abstractmethod
    def update_frame(self):
        """Update frame with new information whenever it is shown on the window."""

    def place_input_cluster(
        self,
        key: str,
        input_text: str,
        coords: tuple,
        char_display: str = None,
    ) -> (Label, Entry):
        """Accurately place a cluster of a label and an entry using absolute
        positioning. Store this instance into a dictionary for easy reference.
        Return the label and entry if needed for extension.

        This method is unique where it uses absolute positioning with place().
        """
        label = Label(self, text=input_text)
        label.place(x=coords[0], y=coords[1])
        entry = Entry(self, show=char_display)
        entry.place(x=coords[0], y=coords[1] + 20)

        self.entries[key] = entry
        return label, entry

    def grid_input_cluster(
        self,
        key: str,
        input_text: str,
        grid: tuple,
        char_display: str = None,
    ) -> (Label, Entry):
        """Assemble a cluster of a label and an input entry onto a grid
        on the interface. Store this instance into a dictionary for easy
        reference. Return the label and entry if needed for extension.

        This method is unique where it positions the cluster as if the window
        is a grid of rows and columns.
        """
        label = Label(self, text=input_text)
        label.grid(row=grid[0], column=grid[1])
        entry = Entry(self, show=char_display)
        entry.grid(row=grid[0], column=grid[1] + 1, padx=20, pady=10)

        self.entries[key] = entry
        return label, entry
