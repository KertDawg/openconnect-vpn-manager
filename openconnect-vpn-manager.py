#!/usr/bin/python3

import os
import math
import curses
from curses import wrapper


#  Base ocserv ssl folder
OCSERV = "../ocserv/ssl"
OCPROFILES = os.path.join(OCSERV, "profiles")

#  Create window object
MainScreen = curses.initscr()

#  Turn off key echo
curses.noecho()

#  React to keys instantly without buffering
curses.cbreak()

#  Turn off the blinking cursor
curses.curs_set(False)

#  Enable color
if curses.has_colors():
    curses.start_color()

#  Set keypad mode
MainScreen.keypad(True)

def Main(MainScreen):
    #  Clear the screen
    MainScreen.clear()
    MainScreen.refresh()

    #  Set the colors

    #  Normal
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    #  Error
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)
    #  Error dialog
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)

    #  Make the main window
    MainWindow = curses.newwin(curses.LINES, curses.COLS, 0, 0)
    MainWindow.bkgd(" ", curses.color_pair(1))
    MainWindow.box()
    MainWindow.addstr(1, 1, "OpenConnect VPN Manager", curses.A_BOLD)

    #  Check the data folders
    if (not ConfigureData(MainWindow)):
        ErrorWindow = curses.newwin(5, 40, (math.floor(curses.LINES / 2) - 3), (math.floor(curses.COLS / 2) - 20))
        ErrorWindow.bkgd(" ", curses.color_pair(3))
        ErrorWindow.box()
        ErrorWindow.addstr(2, 8, "Press any key to exit.")
        MainWindow.refresh()
        ErrorWindow.refresh()
        MainScreen.getkey()
        return

    #  Show the existing clients

    MainWindow.refresh()
    MainScreen.refresh()
    MainScreen.getkey()


def ConfigureData(Window):
    #  Ensure base folder exists
    if (os.path.exists(OCSERV)):
        Window.addstr(3, 1, 'The ocserv folder exists: ' + OCSERV)
    else:
        #  Create the folder
        try:
            os.mkdir(OCSERV)
        except OSError as error:
            Window.addstr(3, 1, 'Error creating the folder: ' + OCSERV, curses.A_BOLD | curses.color_pair(1))
            Window.addstr(4, 1, error)
            return False

        Window.addstr(3, 1, 'Created the folder:' + OCSERV)

    #  Ensure profile folder exists
    if (os.path.exists(OCPROFILES)):
        Window.addstr(4, 1, 'The profiles folder exists: ' + OCPROFILES)
    else:
        #  Create the folder
        try:
            os.mkdir(OCPROFILES)
        except OSError as error:
            Window.addstr(4, 1, 'Error creating the folder: ' + OCPROFILES, curses.A_BOLD | curses.color_pair(1))
            Window.addstr(5, 1, error)
            return False

        Window.addstr(4, 1, 'Created the folder:' + OCPROFILES)

    #  Ensure we have read/write access
    if (os.access(OCPROFILES, os.R_OK | os.W_OK)):
        Window.addstr(5, 1, 'We have read/write access: ' + OCPROFILES)
    else:
        #  Error out
        Window.addstr(5, 1, 'We do not have read/write access: ' + OCPROFILES, curses.A_BOLD | curses.color_pair(1))
        return False
    
    return True


#  Run the main program
wrapper(Main)

