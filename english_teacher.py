# main program
import os
import sys
from kivy.resources import resource_add_path

from frontend.userinterface import UserInterface

type_of_app = 3  # 1 - just voice, 2 - just keyboard, 3 - mixed

""" Run Application """
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    ui = UserInterface(type_of_app)
    ui.run()
