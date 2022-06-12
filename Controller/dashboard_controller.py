"""
dashboard_controller.py contains the logic code for controlling the monitor frame
UI.
"""

__author__ = "Max Chan, Nick Chua"

from Controller.bid_list_controller import BidListController
from api_constants import *
from observable import Observable
from observer import BidObserver
from updater import Updater


class DashboardController(BidListController):
    """
    Controller class that assists in displaying bids that are being monitored
    by the current tutor user.
    """
    def __init__(self):
        BidListController.__init__(self)
        self.updater = None
        self.dashboard = None
        self.subscribed_bids = []
        self.observer = BidObserver()
        self.observable = Observable()
        self.observable.attach(self.observer)

    def get_subscribed_bids(self, user):
        """ Pull all bids from the API and trims it to only the subscribed bids"""
        if not user:
            return
        out = []
        bids = api_get(bid_url)
        for b in bids:
            if b["id"] in user.subscribed_bids:
                out.append(b)

        compare = [x for x in out + self.subscribed_bids if x not in out or x not in self.subscribed_bids]
        if not compare:
            return

        self.subscribed_bids = out
        self.dashboard.bids = out
        self.dashboard.update_bids()
        return out

    def start_updates(self, user, dash):
        """Initiate updating the dashboard for followed bids."""
        self.dashboard = dash
        if self.updater:
            return
        self.updater = Updater(1, self.get_subscribed_bids, user)  # updates every 10 seconds

