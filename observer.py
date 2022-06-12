"""
observer.py outlines the abstract and concrete classes for an observer,
which will be able to subscribe to observed objects and be updated once
an event is triggered in the observed object
"""

__author__ = "Max Chan, Nick Chua"

from abc import ABC, abstractmethod


class AbstractObserver(ABC):
    """
    This is the abstract class for an observing object, who will have its update method called
    when the observed object sees some change.
    """

    @abstractmethod
    def update(self):
        """
        An observer will have this method run once an observed subject has
        its state updated
        :return: None
        """
        pass

class BidObserver(AbstractObserver):
    """
    Concrete Observer for checking for updates to the subscribed bids.
    This will then notify the dashboard controller to refresh the bids with new data
    from the server.
    """
    def __init__(self, dashboard_cont, user):
        self.bids = []
        self.dashboard_cont = dashboard_cont
        self.user = user

    def update(self):
        """Call the dashboard controller to get new subcribed bids"""
        self.dashboard_cont.get_subscribed_bids(self.user)
