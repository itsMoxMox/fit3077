"""
bid_list_frame.py is an abstract class for listing auctions. View varies based on user.
"""

# Library imports
from abc import ABC, abstractmethod
import datetime
import tkinter
from tkinter import ttk
from tkinter import *

# File imports
from api_constants import *
from View.abstract_frames import AbstractFrame
from Controller.bid_list_controller import BidListController

class BidListFrame(AbstractFrame, ABC):
    """
    A class to list auctions, will be inherited by the screens of tutors and students differently
    """

    def __init__(self, parent, controller):
        AbstractFrame.__init__(self, parent, controller)
        self.cont = BidListController()

        self.bids = []
        self.offers = []

    def load_base_ui(self):
        """
        Overrides superclass method to load a treeview of bids, a text box for bid details,
        and a listbox to hold offers made to a bid
        """
        # Title Text
        self.bid_list_label = Label(self, text="List of all Bids")
        self.bid_list_label.place(x=60, y=10)

        # Treeview
        self.bid_list = ttk.Treeview(self)
        self.bid_list["columns"] = (
            "id",
            "status",
            "type",
            "faculty",
            "subj",
            "poster",
            "date_post",
        )

        # Set up columns
        self.bid_list.column("#0", width=0, minwidth=0)
        self.bid_list.column("id", width=0, stretch=tkinter.NO, anchor=tkinter.W)
        self.bid_list.column("status", width=100, minwidth=69, anchor=tkinter.W)
        self.bid_list.column("type", width=100, minwidth=69, anchor=tkinter.W)
        self.bid_list.column("faculty", width=100, minwidth=100, anchor=tkinter.W)
        self.bid_list.column("subj", width=180, minwidth=100, anchor=tkinter.W)
        self.bid_list.column("poster", width=100, minwidth=100, anchor=tkinter.W)
        self.bid_list.column("date_post", width=180, minwidth=120, anchor=tkinter.W)

        # Set up headers
        self.bid_list.heading(
            "status", text="Status"
        )
        self.bid_list.heading(
            "type", text="Bid Type"
        )
        self.bid_list.heading(
            "faculty", text="Faculty"
        )
        self.bid_list.heading(
            "subj", text="Subject"
        )
        self.bid_list.heading(
            "poster", text="Poster"
        )
        self.bid_list.heading(
            "date_post",
            text="Date Posted"
        )
        self.bid_list.place(x=10, y=60)

        # Buttons
        self.back_button = Button(
            self,
            text="Back",
            command=lambda: self.controller.show_frame("MainFrame"),
            width=10,
        )
        self.back_button.place(x=920, y=20)

        self.view_bid_button = Button(
            self, text="View", command=lambda: self.select_item_treeview(), width=10
        )
        self.view_bid_button.place(x=20, y=300)

        self.curr_auction_text = StringVar()
        self.curr_bid = Label(
            self,
            width=50,
            height=20,
            borderwidth=2,
            relief="groove",
            textvariable=self.curr_auction_text,
            justify=LEFT,
            wraplength=400,
        )
        self.curr_bid.place(x=20, y=340)

        self.curr_auction_bids_label = Label(self, text="This Bid's offers").place(
            relx=0.5, y=300
        )
        self.curr_bid_offer = Listbox(self, width=50, height=9)
        self.curr_bid_offer.place(relx=0.5, y=340)

        self.load_bid_cluster()

    @abstractmethod
    def load_bid_cluster(self):
        """
        Method to be overridden which handles loading of buttons in the
        lower right cluster, where messages for current bid are shown.
        """

    @abstractmethod
    def get_bids(self, usertype, controller):
        """Display all vaild auctions onto the frame."""
        pass

    def update_bids(self):
        """Update Treeview with existing auctions."""
        self.bid_list.delete(*self.bid_list.get_children())
        if not self.bids:
            return
        for i in self.bids:
            try:
                self.bid_list.insert(
                    "",
                    1,
                    i["id"],
                    values=(
                        i["id"],
                        "inactive" if i["dateClosedDown"] else "active",
                        i["type"],
                        i["subject"]["name"],
                        i["subject"]["description"],
                        i["initiator"]["userName"],
                        datetime.datetime.fromisoformat(i["dateCreated"][:-1]).strftime(
                            "%a %d %B %Y, %I:%M:%S%p"
                        ),
                    ),
                )
            except TclError:
                pass

    def display_bid_details(self, bid, usertype):
        """Display auction that is currently being viewed and its bids.
        Details are shown in the lower-left textbox.
        """
        # Set up text to display
        text = "Auction ID: " + bid["id"] + "\n\n"
        text += (
            "Date Posted: \n"
            + datetime.datetime.fromisoformat(bid["dateCreated"][:-1]).strftime(
                "%a %d %B %Y, %I:%M:%S%p"
            )
            + "\n\n"
        )
        text += (
                bid["subject"]["name"] + ": " + bid["subject"]["description"] + "\n"
        )
        text += (
                bid["initiator"]["givenName"]
                + " "
                + bid["initiator"]["familyName"]
                + "\n\n"
        )
        for key, value in bid["additionalInfo"].items():
            text += key + ": " + str(value) + "\n"
        self.curr_auction_text.set(text)

        # Display the competing offers of open bids, OR show that it is a closed bid.
        self.curr_bid_offer.delete(0, tkinter.END)

        self.offers = []
        row = 0
        # You can only see the messages if it is an open bid OR if you're looking at your own bids
        if bid["type"] == "open" or usertype == "student":
            for m in api_get(message_url):
                if m["bidId"] == bid["id"]:
                    self.offers.append(m)
                    message_content = ""
                    try:
                        message_content += (
                            ": {}x {} min sessions at ${} per hour. {} Month Contract".format(
                                m["additionalInfo"]["numsOffer"],
                                m["additionalInfo"]["minsOffer"],
                                m["additionalInfo"]["rateOffer"],
                                m["additionalInfo"]["durationOffer"]
                            )
                        )
                    except KeyError:
                        pass  # this message is not formatted to have offer data
                    self.curr_bid_offer.insert(
                        row,
                        "["
                        + m["poster"]["userName"]
                        + "] "
                        + m["content"]
                        + message_content,
                    )
                    row += 1
        else:
            self.curr_bid_offer.insert(row, "This is a closed auction.")

    def select_item_listbox(self):
        """ Return the currently selected item in the listbox"""
        bids_list = self.curr_bid_offer.get(0, END)
        query = self.curr_bid_offer.get(ACTIVE)
        i = 0
        for bid in bids_list:
            if bid == query:
                return self.offers[i]
            i += 1

    def select_item_treeview(self):
        """Return the currently selected item in the treeview box"""
        current = self.bid_list.focus()
        item = self.bid_list.item(current)["values"]

        if item:
            for auction in self.bids:
                if item[0] == auction["id"]:
                    self.display_bid_details(
                        auction,
                        "student"
                        if self.controller.user.is_acting_as_student()
                        else "tutor",
                    )
                    return auction
