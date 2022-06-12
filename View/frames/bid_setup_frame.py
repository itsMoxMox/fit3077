"""
auction_setup_screen.py asks the user how they want to set up an auction.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from tkinter import *

# File imports
from View.abstract_frames import AbstractFrame, IUniqueFrames


class BidSetupFrame(AbstractFrame, IUniqueFrames):
    def __init__(self, parent, controller):
        AbstractFrame.__init__(self, parent, controller)

    def load_base_ui(self):
        """ Base UI will only contain a back button """
        frame_base_ui = Frame(self)

        button_back = Button(
            frame_base_ui,
            text="Back",
            command=lambda: self.controller.show_frame("MainFrame"),
        )
        button_back.grid(row=0, column=4, padx=20)

        frame_base_ui.grid(row=0, column=0)

    def update_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.load_base_ui()

        # Check which button was just pressed
        if self.controller.user.is_acting_as_student():
            self.load_student_frame()
        else:
            self.load_tutor_frame()

    def load_student_frame(self):
        """ Loads buttons to display options for student """
        # Create Open Auction cluster
        label_open_auction = Label(self, text="Create Open Auction")
        label_open_auction.grid(row=1, column=1)
        button_open_auction = Button(
            self, text="Open Auction", command=self.show_open_auction
        )
        button_open_auction.grid(row=2, column=1)

        # Create Closed Auction cluster
        label_closed_auction = Label(self, text="Create Closed Auction")
        label_closed_auction.grid(row=1, column=2)
        button_closed_auction = Button(
            self, text="Closed Auction", command=self.show_closed_auction
        )
        button_closed_auction.grid(row=2, column=2)

        # Create List User Auctions cluster
        label_closed_auction = Label(self, text="Show My Auctions")
        label_closed_auction.grid(row=1, column=3)
        button_closed_auction = Button(
            self, text="My Auctions", command=self.show_my_auctions
        )
        button_closed_auction.grid(row=2, column=3)

    def show_open_auction(self):
        """Show frame for open auctions."""
        self.controller.show_frame("OpenBidFrame")

    def show_closed_auction(self):
        """Show frame for closed auctions."""
        self.controller.show_frame("ClosedBidFrame")

    def show_my_auctions(self):
        """Show frame for list of user's auctions"""
        self.controller.show_frame("StudentBidListFrame")

    def load_tutor_frame(self):
        """Tutors do not have buttons here, because they cannot start bids"""
        pass
