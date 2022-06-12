"""
student_auction_list_screen.py lists all the auctions the student have created.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from tkinter import *

# File imports
from View.abstract_frames import BidListFrame


class StudentBidListFrame(BidListFrame):
    def __init__(self, parent, controller):
        BidListFrame.__init__(self, parent, controller)

    def get_bids(self):
        """
        Pull auctions that are tied to the current user
        """
        self.bids = self.cont.get_bids(self, "student", self.controller.user)

    def update_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.load_base_ui()
        self.get_bids()
        self.update_bids()

    def load_bid_cluster(self):
        """ Place a button for choosing an offer to finalise a contract """

        self.choose_bid_button = Button(
            self, text="Finalise Offer", command=lambda: self.cont.finalise_offer(self, self)
        )
        self.choose_bid_button.place(relx=0.5, y=600)

    def is_positive_integer(self, value):
        """Evaluate whether given value is a positive integer. Return a
        boolean value.
        """
        if not value.isdigit():
            return False
        elif not int(value) > 0:
            return False
