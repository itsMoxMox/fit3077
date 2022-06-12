"""
monitor_frame.py displays a monitoring page that updates the page with
latest bid offers from auctions that they are following.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports

# File imports
from Controller.dashboard_controller import DashboardController
from View.bid_list_frames import TutorBidListFrame

class MonitorFrame(TutorBidListFrame):
    """
    Frame that displays all the bid offers from auctions for tutors to view.
    """
    def __init__(self, parent, controller):
        TutorBidListFrame.__init__(self, parent, controller)
        self.cont = DashboardController()

    def get_bids(self):
        """ Only select monitored bids"""
        self.cont.start_updates(self.controller.user, self)

    def update_frame(self):
        TutorBidListFrame.update_frame(self)
        self.cont.get_subscribed_bids(self.controller.user)
