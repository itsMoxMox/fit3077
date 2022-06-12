"""
open_bid_frame.py represents the frame that handles the creation of
open auctions.

Can only be seen by a student.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports

# File imports
from View.abstract_frames import BidFrame


class OpenBidFrame(BidFrame):
    def __init__(self, parent, controller):
        BidFrame.__init__(self, parent, controller)

    def update_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.load_base_ui()
        self.text_welcome.set("Create new Open Auction")
        self.setup_request_form("open")
