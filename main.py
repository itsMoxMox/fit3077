"""
main.py handles the main processes of the program.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from tkinter import Frame

# File imports
from View.bid_list_frames.monitor_frame import MonitorFrame
from View.frames.contract_list_frame import ContractListFrame
from abstract_window import AbstractWindow
from View.frames import *
from View.bid_frames import *
from View.bid_list_frames import *


class Program(AbstractWindow):
    """
    Handle the main outer "shell" window, where its elements are frames which
    represent different screens such as the login, bidding, etc.
    """

    def __init__(self, *args, **kwargs):
        AbstractWindow.__init__(self, *args, **kwargs)

        # Create the main container for the window
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Frames for the program
        self.frames = {
            "LoginFrame": LoginFrame(parent=container, controller=self),
            "MainFrame": MainFrame(parent=container, controller=self),
            "BidSetupFrame": BidSetupFrame(parent=container, controller=self),
            "StudentBidListFrame": StudentBidListFrame(
                parent=container, controller=self
            ),
            "TutorBidListFrame": TutorBidListFrame(
                parent=container, controller=self
            ),
            "OpenBidFrame": OpenBidFrame(parent=container, controller=self),
            "ClosedBidFrame": ClosedBidFrame(parent=container, controller=self),
            "MonitorFrame": MonitorFrame(parent=container, controller=self),
            "ContractListFrame": ContractListFrame(parent=container, controller=self)
        }
        for _, frame in self.frames.items():
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the first frame, i.e. the login frame
        self.show_frame("LoginFrame")


if __name__ == "__main__":
    program = Program()
    program.geometry("1080x720")
    program.title("epic gamers - FIT3077 A2")
    program.mainloop()
