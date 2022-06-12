"""
tutor_auction_list_screen.py lists all auctions available for the tutor to send offers for.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from datetime import *
from tkinter import *

# File imports
from View.abstract_frames import BidListFrame


class TutorBidListFrame(BidListFrame):
    def __init__(self, parent, controller):
        BidListFrame.__init__(self, parent, controller)

    def get_bids(self):
        """
        Simply pull all active auctions
        """
        self.bids = self.cont.get_bids(self, "tutor", self.controller.user)

    def update_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.load_base_ui()
        self.get_bids()
        self.update_bids()

    def load_bid_cluster(self):
        """
        Places fields for counteroffers, and buttons for submitting offer or buying out bid.
        """
        self.disclaimer_label = Label(self, text=
        "DISCLAIMER: \nBy sending an offer you are consenting to signing a \ncontract"
        " between you and this student")
        self.disclaimer_label.place(x=666, y=520)

        _, offer_mins = self.place_input_cluster(
            "minsPerSession", "Mins per session", (666, 580)
        )
        _, offer_num = self.place_input_cluster(
            "numSessions", "Number of sessions", (666, 620)
        )
        _, offer_rate = self.place_input_cluster(
            "sessionRate", "Rate per Session", (666, 660)
        )
        _, offer_comments = self.place_input_cluster("comments", "Comments", (870, 620))

        # Allows user to specify contract duration
        _, offer_duration = self.place_input_cluster(
            "contract_duration",
            "Contract Duration in months ",
            (870, 580)
        )

        def monitor_bid():
            """Call the controller to monitor the selected bid"""
            self.cont.monitor(self, self.controller.user)

        self.toggle_monitor = Button(
            self, text="Monitor this Bid", command=monitor_bid
        )
        self.toggle_monitor.place(x=140, y=300)

        self.send_offer_button = Button(
            self, text="Send Offer", command=lambda: self.cont.send_offer(self,
                                                                          offer_mins,
                                                                          offer_num,
                                                                          offer_rate,
                                                                          offer_comments,
                                                                          offer_duration)
        )
        self.send_offer_button.place(x=870, y=675)

        self.buyout_button = Button(self, text="Buyout Bid", command=lambda: self.cont.buyout(self))
        self.buyout_button.place(x=540, y=520)
