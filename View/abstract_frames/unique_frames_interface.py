"""
unique_frames_interface.py contains the interface for when a frame
needs to separate its UI into student-only or tutor-only. 
"""

__author__ = "Max Chan, Nick Chua"

from abc import ABC, abstractmethod


class IUniqueFrames(ABC):
    """
    Interface of methods that show different frames for certain users. Not
    intended to be instantiated by anyone else, nor should be used outside
    of the frames package.

    Use this interface only when the frames has certain widgets that are
    only shown to certain users, and override each method to accommodate
    each kind of user.

    eg. the student frame should only be seen by students.
    """

    @abstractmethod
    def load_student_frame(self):
        """ Load frame only seen by students."""

    @abstractmethod
    def load_tutor_frame(self):
        """ Load frame only seen by tutors."""
