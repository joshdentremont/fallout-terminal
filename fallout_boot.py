import curses
from fallout_functions import slowWrite

######################## global 'constants' ##############

ENTRY_1 = 'set terminal/inquire'

######################## text strings ####################

MESSAGE_1 = 'WELCOME TO ROBCO INDUSTRIES (TM) TERMLINK'

MESSAGE_2 = 'RIT-V300'

######################## functions #######################

def runBoot(scr):
    """
    Start the boot portion of the terminal
    """
    curses.use_default_colors()
    # set screen to initial position
    scr.erase()
    scr.move(0, 0)
    
    slowWrite(scr, MESSAGE_1 + '\n\n>')

    curses.napms(500)

    return True

def beginBoot(hardMode):
    """
    Initialize curses and start the boot process

    hardMode - boolean indicating whether the user has to enter the ENTRY
               constants, or if they are entered automatically
    Returns true if hardMode == false or if the user entered the correct string
    """
    res = curses.wrapper(runBoot)
    return res
