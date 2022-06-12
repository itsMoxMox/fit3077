"""
bid_controller.py handles the code logic for bids.
"""
import popups
from Model.bid import Bid
from api_constants import *


class BidController:
    def __init__(self):
        pass

    def new_bid(
        self,
        bid_type,
        initiator_id,
        date_created,
        subject_id,
        add_info
    ):
        """Create a new auction with valid information and post it on the API."""
        Bid(
            bid_type,
            initiator_id,
            date_created,
            subject_id,
            add_info["minutes_per_session"],
            add_info["sessions_per_week"],
            add_info["preferred_hourly_rate"],
            add_info["tutor_competency"],
            add_info["contract_duration"]
        )

    def get_lesson(self, lesson_name):
        """Query the API for lessons based on lesson_name."""

        for lesson in api_get(subject_url):
            if lesson["description"] == lesson_name:
                return lesson

        popups.PopupError("Lesson not found")
