"""
observable.py outlines the abstract and concrete classes for a Subject/Observable
object.
"""

from abc import ABC, abstractmethod

from api_constants import *
from updater import Updater


class AbstractObservable(ABC):
    """
    Abstract Observable is the abstract superclass for an observed object, whose state change
    calls for an update call for the subscriber of observer objects observing this (its child)
    subject.
    """

    @abstractmethod
    def attach(self, observer):
        """
        Attaches an observer to the subject
        :param observer: the observer to attach to the subject
        :return: None
        """
        pass

    @abstractmethod
    def detach(self, observer):
        """
        detaches an observer from the subject
        :param observer: the observer to detach
        :return: None
        """
        pass

    @abstractmethod
    def notify(self):
        """
        Notify all subscribed observers about some event
        :return: None
        """
        pass

class Observable(AbstractObservable):
    """
    A concrete implementation of the AbstractObservable,
    This subject monitors any changes from the local copy of subscribed bids with the version
    that is stored on the user's data on the server.
    """

    _state = None
    _observers = []
    subscribed_bids = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for obs in self._observers:
            obs.update()

    def start_listening(self):
        Updater(1, self.check_for_changes)

    def check_for_changes(self, user):
        if not user:
            return
        out = []
        for b in api_get(bid_url):
            if b["id"] in user.subscribed_bids:
                out.append(b)

        compare = [x for x in out + self.subscribed_bids if x not in out or x not in self.subscribed_bids]
        if not compare:
            return

        self.notify()
