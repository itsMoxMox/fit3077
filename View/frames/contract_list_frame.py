"""
contract_list_frame.py lists all the contracts the student have been a part of.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
import tkinter
import datetime
from tkinter import *
from tkinter import ttk

# File imports
from Controller.contract_list_controller import ContractListController
from View.abstract_frames import AbstractFrame


class ContractListFrame(AbstractFrame):
    def __init__(self, parent, controller):
        AbstractFrame.__init__(self, parent, controller)
        self.cont = ContractListController()

    def load_base_ui(self):
        """
        Overrides superclass method to load a treeview of contracts
        """
        # Title Texts
        self.contract_list_label = Label(self, text="List of all Contracts")
        self.contract_list_label.place(x=60, y=20)

        self.contract_list_label = Label(self, text="Contract Info")
        self.contract_list_label.place(x=700, y=20)

        # Treeview
        self.contract_list = ttk.Treeview(self)
        self.contract_list["columns"] = (
            "id",
            "first",
            "second",
            "subj",
            "date_created",
            "date_exp"
        )

        # Set up columns
        self.contract_list.column("#0", width=0, minwidth=0)
        self.contract_list.column("id", width=0, stretch=tkinter.NO, anchor=tkinter.W)
        self.contract_list.column("first", width=100, minwidth=100, anchor=tkinter.W)
        self.contract_list.column("second", width=100, minwidth=100, anchor=tkinter.W)
        self.contract_list.column("subj", width=90, minwidth=90, anchor=tkinter.W)
        self.contract_list.column("date_created", width=180, minwidth=180, anchor=tkinter.W)
        self.contract_list.column("date_exp", width=180, minwidth=180, anchor=tkinter.W)

        # Set up headers
        self.contract_list.heading(
            "first", text="First"
        )
        self.contract_list.heading(
            "second", text="Second"
        )
        self.contract_list.heading(
            "subj", text="Subject"
        )
        self.contract_list.heading(
            "date_created",
            text="Date Created"
        )
        self.contract_list.heading(
            "date_exp",
            text="Date of Expiry"
        )
        self.contract_list.place(x=20, y=60)

        # Buttons
        self.back_button = Button(
            self,
            text="Back",
            command=lambda: self.controller.show_frame("MainFrame"),
            width=10,
        )
        self.back_button.place(x=920, y=10)

        self.view_contract_button = Button(
            self, text="View", command=lambda: self.select_item_treeview(), width=10
        )
        self.view_contract_button.place(x=574, y=300)

        self.curr_contract_text = StringVar()
        self.curr_contract = Label(
            self,
            width=37,
            height=20,
            borderwidth=2,
            relief="groove",
            textvariable=self.curr_contract_text,
            justify=LEFT,
            wraplength=330,
        )
        self.curr_contract.place(x=700, y=60)

        # New Contract Terms input cluster
        self.label_contract_renew = Label(self, text="New Contract Terms").place(x=40, y=410)
        self.place_input_cluster("minsPerSesssion", "Mins per session: ", (40, 440))
        self.place_input_cluster("numSessions", "Number of Sessions: ", (40, 490))
        self.place_input_cluster("sessionRate", "Rate per session: ", (40, 540))
        self.place_input_cluster("contractDuration", "Contract Duration: ", (40, 590))

        # Contract Renewal subsection
        self.label_contract_renew = Label(self, text="Contract Renewal").place(x=300, y=410)

        self.place_input_cluster("newTutorUser", "New Tutor Username: ", (300, 560))
        self.button_new_tutor = Button(self, command=lambda: self.cont.renew_contract(
            self.select_item_treeview(),
            self.entries["newTutorUser"].get(),
            self.entries["renewDuration"].get(),
            (self.entries["minsPerSesssion"].get(),
             self.entries["numSessions"].get(),
             self.entries["sessionRate"].get())
        ),
                                       text="Form contract with new Tutor").place(x=300, y=610)

        self.place_input_cluster("renewDuration", "Renew Duration: ", (300, 440))
        self.button_renew = Button(self, command=lambda: self.cont.renew_contract(
            self.select_item_treeview(),
            None,
            self.entries["renewDuration"].get(),
            (self.entries["minsPerSesssion"].get(),
             self.entries["numSessions"].get(),
             self.entries["sessionRate"].get())

        ),
                                   text="Renew contract").place(x=300, y=490)

    def update_frame(self):
        """Implement abstract method"""
        for widget in self.winfo_children():
            widget.destroy()
        self.load_base_ui()
        self.update_contracts()

    def update_contracts(self):
        self.contract_list.delete(*self.contract_list.get_children())
        if not self.controller.user.contracts:
            return
        for i in self.controller.user.contracts:
            # only list contract if the user is the STUDENT in the contract.
            if i.first_id == self.controller.user.get_id():
                try:
                    self.contract_list.insert(
                        "",
                        1,
                        values=(
                            i.contract_id,
                            i.data["firstParty"]["userName"],
                            i.data["secondParty"]["userName"],
                            i.data["subject"]["name"],
                            datetime.datetime.fromisoformat(i.date_created[:-1]).strftime(
                                "%a %d %B %Y, %I:%M:%S%p"
                            ),
                            datetime.datetime.fromisoformat(i.date_expiry[:-1]).strftime(
                                "%a %d %B %Y"
                            )
                        )
                    )
                except TclError:
                    pass

    def select_item_treeview(self):
        """Return the currently selected item in the treeview box"""
        current = self.contract_list.focus()
        item = self.contract_list.item(current)["values"]

        if item:
            for c in self.controller.user.contracts:
                if item[0] == c.contract_id:
                    self.display_contract_details(c)
                    return c

    def display_contract_details(self, contract):
        """Display contract that is currently being viewed
        Details are shown in the right textbox.
        """
        text = ""
        # Put expiry warning at top
        if contract in self.controller.user.expiring_contracts:
            text += "WARNING:\nThis contract will expire in less than a month.\n\n"

        # Set up text to display
        text += "Contract ID: " + contract.contract_id + "\n\n"
        text += (
                "Date Created: \n"
                + datetime.datetime.fromisoformat(contract.date_created[:-1]).strftime(
            "%a %d %B %Y, %I:%M:%S%p"
        )
                +
                "\n\nDate of Expiry: \n"
                + datetime.datetime.fromisoformat(contract.date_expiry[:-1]).strftime(
            "%a %d %B %Y, %I:%M:%S%p")
                + "\n\n"
        )
        text += (
                contract.data["firstParty"]["givenName"]
                + " "
                + contract.data["firstParty"]["familyName"]
                + " and "
                + contract.data["secondParty"]["givenName"]
                + " "
                + contract.data["secondParty"]["familyName"]
                + "\n"
        )
        text += (
                contract.data["subject"]["name"] + ": " + contract.data["subject"]["description"] + "\n\n"
        )

        text += (
                contract.lesson_info["sessions_per_week"] + " sessions per week\n\n" +
                contract.lesson_info["minutes_per_session"] + " minutes per session at\n" +
                "$" + contract.lesson_info["hourly_rate"] + " per hour\n"

        )
        for key, value in contract.additional_info.items():
            text += key + ": " + str(value) + "\n"
        self.curr_contract_text.set(text)
