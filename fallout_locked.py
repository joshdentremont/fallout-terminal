import curses

from fallout_functions import slowWrite
from fallout_functions import centeredWrite

################## text strings ######################

LOCKED_1 = 'TERMINAL LOCKED'
LOCKED_2 = 'PLEASE CONTACT AN ADMINISTRATOR'

################## global 'constants' ################

# amount of time to pause after lockout
LOCKED_OUT_TIME = 5000

################## functions #########################

def runLocked(scr):
    """
    Start the locked out portion of the terminal
    """
    curses.use_default_colors()
    size = scr.getmaxyx()
    width = size[1]
    height = size[0]
    # set screen to initial position
    scr.erase()
    curses.curs_set(0)
    scr.move(int(height / 2 - 1), 0)
    centeredWrite(scr, LOCKED_1)
    scr.move(int(height / 2 + 1), 0)
    centeredWrite(scr, LOCKED_2)
    scr.refresh()
    curses.napms(LOCKED_OUT_TIME)

    
def beginLocked():
    """
    Initialize curses and start the locked out process
    """
    curses.wrapper(runLocked)
