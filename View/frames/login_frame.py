"""
login_screen.py handles all the processes related to the login screen.
"""

__author__ = "Max Chan, Nick Chua"

# Library imports
from tkinter import *

# File imports
from View.abstract_frames import AbstractFrame
from Controller.login_controller import LoginHandler


class LoginFrame(AbstractFrame):
    """
    Control the processes and elements shown on the login screen. Typically
    the first frame shown upon starting the program.
    """

    def __init__(self, parent, controller):
        AbstractFrame.__init__(self, parent, controller)
        self.cont = LoginHandler()
        self.load_base_ui()

    def load_base_ui(self):
        # Create the title label
        label_login = Label(self, text="Login")
        label_login.grid(row=0, column=2, pady=10)

        # Create input clusters
        _, username = self.grid_input_cluster("username", "Username: ", (1, 1))
        _, password = self.grid_input_cluster("password", "Password: ", (2, 1), "*")

        button_login = Button(
            self,
            text="Login",
            command=lambda: self.cont.login(self, username.get(), password.get(), self.controller),
        )
        button_login.grid(row=3, column=2, pady=20)

        # Bindings
        def enter(event):
            """Event function for when user presses enter"""
            self.cont.login(self, username.get(), password.get())

        username.bind("<Return>", enter)
        password.bind("<Return>", enter)

    def update_frame(self):
        # Login Frame does not need to handle updates
        pass

