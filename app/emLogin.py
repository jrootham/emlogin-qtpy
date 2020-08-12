import sys
import sqlite3
import pathlib

from Controller import Controller
import view

"""
EMLogin is an application designed to make it easier to login to sites that support the EMLogin 
protocal.


"""
def fileName():
    """File name constant"""
    return str(pathlib.Path.home()) + "/.config/emlogin.sqlite"

        
if __name__ == "__main__":
    view.run(Controller(fileName()))
