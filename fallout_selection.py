import curses
from fallout_functions import slowWrite
from fallout_functions import centeredWrite
from fallout_functions import NEWLINE

####################### text strings ########################

CENTERED_HEADERS = (
    'ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM',
    'COPYRIGHT 2075-2077 ROBCO INDUSTRIES',
    '-SERVER 6-',
    ''
)

OTHER_HEADERS = (
    '\tSoftLock Solutions, Inc',
    '"Your Security is Our Security"',
    '>\\ Welcome, USER',
    ''
)

SELECTIONS = (
    'Disengage Lock',
    'Deactivate Turrets',
    'Read Log'
)

###################### Functions ############################

def makeSelection(scr):
    """
    ALlow the user to select an option
    Returns the line number of the users selection starting at 0
    """
    inchar = 0
    selection = 0
    selection_count = len(SELECTIONS)
    selection_start_y = scr.getyx()[0]
    width = scr.getmaxyx()[1]
    
    while inchar != NEWLINE:
        # move to start of selections and hightlight current selection
        scr.move(selection_start_y, 0)
        line = 0
        for sel in SELECTIONS:
            whole_line = '> ' + SELECTIONS[line]
            space = width - len(whole_line) % width
            whole_line += ' ' * space
            
            if line == selection:
                scr.addstr(whole_line, curses.A_REVERSE)
            else:
                scr.addstr(whole_line)
            line += 1
            scr.refresh()

        inchar = scr.getch()

        # move up and down
        if inchar == curses.KEY_UP and selection > 0:
            selection -= 1
        elif inchar == curses.KEY_DOWN and selection < selection_count - 1:
            selection += 1

    return selection
        

def runSelection(scr):
    """
    Print the selections and allow the user to select one
    """
    curses.use_default_colors()
    scr.erase()
    scr.move(0, 0)
    curses.curs_set(0)
    curses.noecho()

    width = scr.getmaxyx()[1]

    for header in CENTERED_HEADERS:
        centeredWrite(scr, header + '\n')

    for header in OTHER_HEADERS:
        slowWrite(scr, header + '\n')

    for i in range(width):
        scr.addch(curses.ACS_BSBS)
    scr.refresh()

    return makeSelection(scr)

def beginSelection():
    """
    Initialize curses and start the boot process
    """
    res = curses.wrapper(runSelection)
    return res
