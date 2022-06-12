"""
main_screen.py handles all processes related to the main screen.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from tkinter import *

# File imports
from View.abstract_frames import AbstractFrame, IUniqueFrames


class MainFrame(AbstractFrame, IUniqueFrames):
    """
    Control the processes and elements shown on the main screen, which follows
    from the login screen.
    """

    def __init__(self, parent, controller):
        AbstractFrame.__init__(self, parent, controller)

    def load_base_ui(self):
        frame_base_ui = Frame(self)

        # Logout button
        button_logout = Button(
            frame_base_ui,
            text="Logout",
            command=lambda: self.controller.show_frame("LoginFrame"),
        )
        button_logout.grid(row=0, column=2, padx=20, pady=0)

        # Welcome Text
        self.text_welcome = StringVar()
        self.text_welcome.set("Welcome")
        self.label_welcome = Label(frame_base_ui, textvariable=self.text_welcome)
        self.label_welcome.grid(row=2, column=1, padx=10)

        # Warning Text for expiring contracts
        self.warning_text = StringVar()
        if self.controller.user.expiring_contracts:
            self.warning_text.set("You have contracts expiring in less than a month")
        self.label_warning = Label(frame_base_ui, textvariable=self.warning_text)
        self.label_warning.grid(row=3, column=1)

        frame_base_ui.grid(row=0, column=0, padx=30)

    def update_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.load_base_ui()

        if self.controller.user.is_student():
            self.load_student_frame()
        if self.controller.user.is_tutor():
            self.load_tutor_frame()

    def load_student_frame(self):
        """ Loads the UI for the student, and changes the welcome message to state the user's type """
        self.text_welcome.set(
            "Welcome, "
            + self.controller.user.get_name()[0]
            + " "
            + self.controller.user.get_name()[1]
            + " (Student)"
        )

        # initialise student subsection
        frame_student = Frame(self, bd=2, relief="groove", padx=5, pady=5)

        # Section Label
        label_student_subsec = Label(frame_student, text="Student Section:")
        label_student_subsec.grid(row=0, column=0)

        # View Bids Button
        button_new_auction = Button(
            frame_student, text="View Bids", command=self.open_new_bid
        )
        button_new_auction.grid(row=1, column=0, pady=10)

        # View Contracts Button
        button_new_auction = Button(
            frame_student, text="View Contracts", command=self.open_all_contracts
        )
        button_new_auction.grid(row=2, column=0, pady=10)

        frame_student.grid(row=3, column=0, pady=10)

    def load_tutor_frame(self):
        """ Loads the UI for the tutor, and changes the welcome message to state user's type """
        self.text_welcome.set(
            "Welcome, "
            + self.controller.user.get_name()[0]
            + " "
            + self.controller.user.get_name()[1]
            + " (Tutor)"
        )

        # initialise tutor subsection
        frame_tutor = Frame(self, bd=2, relief="groove", padx=5, pady=5)

        # Section Label
        label_tutor_subsec = Label(frame_tutor, text="Tutor Section:")
        label_tutor_subsec.grid(row=0, column=0)

        # Find Auctions Button
        button_search_bid = Button(
            frame_tutor, text="Find Bids", command=self.open_all_bid
        )
        button_search_bid.grid(row=1, column=0, pady=10)

        # Open Monitoring Dashboard
        button_open_dash = Button(
            frame_tutor, text="Open Dashboard", command=self.open_dashboard
        )
        button_open_dash.grid(row=2, column=0)

        frame_tutor.grid(row=4, column=0, pady=10)

    def open_new_bid(self):
        """Show frame to create a new auction. Only seen by students."""
        self.controller.user.set_acting_as_student(True)
        self.controller.show_frame("BidSetupFrame")

    def open_all_contracts(self):
        """Show the frame to display all bids"""
        self.controller.user.set_acting_as_student(True)
        self.controller.show_frame("ContractListFrame")

    def open_all_bid(self):
        """Show frame to display all auctions. Only seen by tutors."""
        self.controller.user.set_acting_as_student(False)
        self.controller.show_frame("TutorBidListFrame")

    def open_dashboard(self):
        """ Show the bid monitoring dashboard. Only seen by tutors"""
        self.controller.user.set_acting_as_student(False)
        self.controller.show_frame("MonitorFrame")
