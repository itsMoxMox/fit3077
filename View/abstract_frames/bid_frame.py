"""
bid_frame.py represents the abstract frame for different types of auctions.
"""

__author__ = "Max Chan, Nick Chua"

# Library import
from tkinter import *
from datetime import datetime
from abc import ABC

# File import
from Controller.bid_controller import BidController
from View.abstract_frames import AbstractFrame
from popups import *
from api_constants import *


class BidFrame(AbstractFrame, ABC):
    """
    Not meant to be initiated. Only inherited by frames for different types of auctions.
    """

    def __init__(self, parent, controller):
        AbstractFrame.__init__(self, parent, controller)
        self.cont = BidController()
        self.text_welcome = StringVar()

    def load_base_ui(self):
        frame_base_ui = Frame(self)
        self.label_welcome = Label(self, textvariable=self.text_welcome)
        self.label_welcome.grid(row=0, column=2)

        self.button_back = Button(
            frame_base_ui,
            text="Back",
            command=lambda: self.controller.show_frame("BidSetupFrame"),
        )
        self.button_back.grid(row=1, column=4, padx=20)

        frame_base_ui.grid(row=0, column=0)

    def setup_request_form(self, bid_type):
        """Create labels and entries for the auction information form.

        This method is separated to declutter from the constructor.
        """
        self.disclaimer_label = \
            Label(self, text="DISCLAIMER:\nBy submitting a bid, you consent to signing a contract\n"
                             "between you and a prospecting tutor.")
        self.disclaimer_label.place(x=500, y=200)

        _, lessonEntry = self.grid_input_cluster("lessonName", "Lesson: ", (1, 0))

        self.grid_input_cluster(
            "minsPerSession", "Preferred minutes per session: ", (2, 0)
        )
        self.grid_input_cluster("numSessions", "Number of sessions: ", (3, 0))
        self.grid_input_cluster("sessionRate", "Rate per session: ", (4, 0))
        self.grid_input_cluster("tutorCompetency", "Tutor competency", (5, 0))
        self.grid_input_cluster("contractDuration", "Contract Duration", (6, 0))

        self.button_new_request = Button(
            self, text="Create Auction", command=lambda: self.cont.new_bid(
                bid_type,
                self.controller.user.get_id(),
                str(datetime.utcnow().isoformat() + "Z"),
                self.get_lesson(lessonEntry.get())["id"],
                {
                    "minutes_per_session": self.entries["minsPerSession"].get(),
                    "sessions_per_week": self.entries["numSessions"].get(),
                    "preferred_hourly_rate": self.entries["sessionRate"].get(),
                    "tutor_competency": self.entries["tutorCompetency"].get(),
                    "contract_duration": self.entries["contractDuration"].get(),
                }
            )
        )
        self.button_new_request.grid(pady=10)

        self.create_lesson_list(lessonEntry)

    def create_lesson_list(self, lessonEntry):
        """Create and set up listbox filled with lesson names."""

        def update_list(given_list):
            """Update listbox based on items in given_list."""
            lesson_list.delete(0, END)
            for item in given_list:
                lesson_list.insert(END, item)

        def fillout_box(event):
            """Fill in the lesson entry box based on item selected in
            listbox
            """
            lessonEntry.delete(0, END)
            lessonEntry.insert(0, lesson_list.get(ANCHOR))

        def check_list(event):
            """Update listbox based on input in the lesson entry box."""
            user_input = lessonEntry.get()

            if user_input == "":
                # Reset to the beginning
                data = lesson_names
            else:
                data = []
                for item in lesson_names:
                    if user_input.lower() in item.lower():
                        data.append(item)
            update_list(data)

        # Loading list of existing lessons
        lessons_data = requests.get(
            url=subject_url, headers={"Authorization": my_api_key}
        ).json()

        lesson_names = []
        for lesson in lessons_data:
            lesson_names.append(lesson["description"])

        # Creating Listbox
        lesson_list = Listbox(self, height=5, width=50)
        lesson_list.grid(row=1, column=2, rowspan=3)
        # Instantiate every lesson name
        update_list(lesson_names)

        # Fill in the Lesson Entry based on selected item in Listbox
        lesson_list.bind("<<ListboxSelect>>", fillout_box)
        # Update Listbox based on user input
        lessonEntry.bind("<KeyRelease>", check_list)

    def get_lesson(self, lesson_name):
        """ Calls the controller to get the lesson from the API given a lesson name"""
        return BidController.get_lesson(self, lesson_name)

    def is_positive_integer(self, key, value):
        """Assess whether given value is a positive numerical integer."""
        if not value.isdigit():
            PopupError(key + " must be a number.")
            raise Exception()
        elif not int(value) > 0:
            PopupError(key + " must be positive.")
            raise Exception()
