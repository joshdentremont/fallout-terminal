from fallout_functions import slowWrite
from fallout_functions import INPUT_PAUSE
from fallout_functions import TYPE_DELAY
from fallout_functions import upperInput
import curses

######################## global 'constants' ##############

ENTRY_1 = 'SET TERMINAL/INQUIRE'

ENTRY_2 = 'SET FILE/PROTECTION=OWNER:RWED ACCOUNTS.F'

ENTRY_3 = 'SET HALT RESTART/MAINT'

ENTRY_4 = 'RUN DEBUG/ACCOUNTS.F'


######################## text strings ####################

MESSAGE_1 = 'WELCOME TO ROBCO INDUSTRIES (TM) TERMLINK'

MESSAGE_2 = 'RIT-V300'

MESSAGE_3 = 'Initializing Robco Industries(TM) MF Boot Agent v2.3.0\n' \
            'RETROS BIOS\n' \
            'RBIOS-4.02.08.00 52EE5.E7.E8\n' \
            'Copyright 2201-2203 Robco Ind.\n' \
            'Uppermem: 64 KB\n' \
            'Root (5A8)\n' \
            'Maintenance Mode'


######################## functions #######################

def runBoot(scr, hardMode):
    """
    Start the boot portion of the terminal

    hardMode - boolean indicating whether the user has to enter the ENTRY
               constants, or if they are entered automatically
    """
    curses.use_default_colors()
    scr.erase()
    scr.move(0, 0)

    curses.noecho()
    scr.scrollok(True)
    
    slowWrite(scr, MESSAGE_1 + '\n\n')

    if hardMode:
        # use must enter the correct text to proceed
        entry = ''
        while entry.upper() != ENTRY_1.upper():
            slowWrite(scr, '>')
            entry = upperInput(scr)
    else:
        # input is entered for them
        slowWrite(scr, '>')
        curses.napms(INPUT_PAUSE)
        slowWrite(scr, ENTRY_1 + '\n', TYPE_DELAY)

    slowWrite(scr, '\n' + MESSAGE_2 + '\n\n')

    if hardMode:
        entry = ''
        while entry.upper() != ENTRY_2.upper():
            slowWrite(scr, '>')
            entry = upperInput(scr)
        while entry.upper() != ENTRY_3.upper():
            slowWrite(scr, '>')
            entry = upperInput(scr)
    else:
        slowWrite(scr, '>')
        curses.napms(INPUT_PAUSE)
        slowWrite(scr, ENTRY_2 + '\n', TYPE_DELAY)
        slowWrite(scr, '>')
        curses.napms(INPUT_PAUSE)
        slowWrite(scr, ENTRY_3 + '\n', TYPE_DELAY)

    slowWrite(scr, '\n' + MESSAGE_3 + '\n\n')

    if hardMode:
        entry = ''
        while entry.upper() != ENTRY_4.upper():
            slowWrite(scr, '>')
            entry = upperInput(scr)
    else:
        slowWrite(scr, '>')
        curses.napms(INPUT_PAUSE)
        slowWrite(scr, ENTRY_4 + '\n', TYPE_DELAY)
        
    curses.napms(INPUT_PAUSE)
    return True

def beginBoot(hardMode):
    """
    Initialize curses and start the boot process

    hardMode - boolean indicating whether the user has to enter the ENTRY
               constants, or if they are entered automatically
    Returns true if hardMode == false or if the user entered the correct string
    """
    res = curses.wrapper(runBoot, hardMode)
    return res
