import curses

from fallout_functions import slowWrite

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
    scr.move(height / 2 - 1, width / 2 - len(LOCKED_1) / 2)
    slowWrite(scr, LOCKED_1)
    scr.move(height / 2 + 1, width / 2 - len(LOCKED_2) / 2)
    slowWrite(scr, LOCKED_2)
    scr.refresh()
    curses.napms(LOCKED_OUT_TIME)

    
def beginLocked():
    """
    Initialize curses and start the locked out process
    """
    curses.wrapper(runLocked)
