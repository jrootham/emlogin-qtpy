import sys
import sqlite3

from Controller import Controller
import view

"""
noPassword is an application designed to make it easier to login to sites that support the noPassword 
protocal.


"""
def fileName():
    """File name constant"""
    return ".emsignon.sqlite"

        
if __name__ == "__main__":
    view.run(Controller(fileName()))
