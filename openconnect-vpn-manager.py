#!/usr/bin/python3

import os
import math
from pathlib import Path
import curses
from curses import wrapper


#  Base ocserv ssl folder
OCSERV = "../ocserv/ssl"
OCPROFILES = os.path.join(OCSERV, "profiles")


Profiles = []


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
    #  Low-key
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLUE)

    #  Make the main window
    MainWindow = curses.newwin(curses.LINES, curses.COLS, 0, 0)
    MainWindow.bkgd(" ", curses.color_pair(1))
    MainWindow.box()

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
    
    #  Clear the screen
    MainWindow.clear()
    MainScreen.refresh()
    MainWindow.refresh()

    #  Show the main menu and do the main loop
    MainMenu(MainWindow, 3, curses.LINES - 6)


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


def DrawHeader(Window):
    Window.addstr(1, 1, "OpenConnect VPN Manager", curses.A_BOLD)


def ShowExistingProfiles(Window, Line):
    global Profiles
    Profiles = []

    #  Get the base names of all p12 files
    for p in os.listdir(OCPROFILES):
        if p.endswith(".p12"):
            Profiles.append(Path(p).stem)

    Profiles.sort()
    NumberOfProfiles = len(Profiles)

    #  There aren't any to show
    if NumberOfProfiles == 0:
        Window.addstr(Line, 1, "There are no existing profiles.", curses.color_pair(3))
        return False

    Window.addstr(Line, 1, "Profiles:", curses.A_BOLD)
    CurrentIndex = 0    
    for p in Profiles:
        Window.addstr(Line + CurrentIndex + 1, 2, str(CurrentIndex + 1) + ": " + p)
        CurrentIndex += 1

    return True


def MainMenu(Window, ListLine, MenuLine):
    DrawHeader(Window)
    SelectedOption = 1

    while True:
        #  Show the existing clients
        ShowExistingProfiles(Window, ListLine)

        #  Draw the menu
        DrawMenu(Window, MenuLine + 1, SelectedOption)

        MainScreen.refresh()
        Window.refresh()
        Key = MainScreen.getch()

        if Key == curses.KEY_DOWN:
            SelectedOption += 1

            if SelectedOption > 3:
                SelectedOption = 3
        elif Key == curses.KEY_UP:
            SelectedOption -= 1
            
            if SelectedOption < 1:
                SelectedOption = 1
        elif Key == curses.KEY_ENTER or Key == 10 or Key == 13:
            if SelectedOption == 3:
                return
            else:
                ExecuteOption(Window, MenuLine - 4, SelectedOption)

                #  Reset the window
                Window.clear()
                DrawHeader(Window)
                Window.addstr(MenuLine, 1, "What to do?", curses.A_BLINK)


def DrawMenu(Window, Line, SelectedOption):
    Window.addstr(Line, 1, "Add a profile", curses.A_REVERSE if (SelectedOption == 1) else 0)
    Window.addstr(Line + 1, 1, "Remove a profile", curses.A_REVERSE if (SelectedOption == 2) else 0)
    Window.addstr(Line + 2, 1, "Exit", curses.A_REVERSE if (SelectedOption == 3) else 0)
    return


def ExecuteOption(Window, Line, OptionNumber):
    if OptionNumber == 1:
        AddProfile(Window, Line)
    elif OptionNumber == 2:
        RemoveProfile(Window, Line)


def AddProfile(Window, Line):
    return


def RemoveProfile(Window, Line):
    global Profiles
    SelectedProfile = 0
    NumberOfProfiles = len(Profiles)

    if NumberOfProfiles == 0:
        return

    Window.addstr(Line, 1, "Remove which profile?", curses.A_BOLD)
    Window.refresh()

    while SelectedProfile == 0:
        Key = MainScreen.getch()

        if (Key >= ord("1")) and (Key <= ord("9")):
            SelectedProfile = Key - ord("0")

            if SelectedProfile > NumberOfProfiles:
                SelectedProfile = 0

    SelectedName = Profiles[SelectedProfile - 1]
    Window.addstr(Line, 1, "Delete profile: ")
    Window.addstr(Line, 17, SelectedName + "              ", curses.A_BOLD)
    Window.addstr(Line + 1, 1, "Are you sure? (y/n)", curses.color_pair(2) | curses.A_BLINK | curses.A_BOLD)
    Window.refresh()
    Key = 0

    while True:
        Key = MainScreen.getch()

        if (Key == ord("n")) or (Key == ord("N")):
            return
        elif (Key == ord("y")) or (Key == ord("Y")):
            #  Actually do the removal
            return
    

#  Run the main program
wrapper(Main)

