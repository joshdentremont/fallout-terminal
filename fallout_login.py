import curses
from fallout_functions import slowWrite
from fallout_functions import INPUT_PAUSE
from fallout_functions import TYPE_DELAY
from fallout_functions import upperInput
from fallout_functions import HIDDEN_MASK
################## text strings ######################

HEADER_TEXT = 'WELCOME TO ROBCO INDUSTRIES (TM) TERMLINK'

PASSWORD_PROMPT = 'ENTER PASSWORD NOW'

PASSWORD_ERROR = 'INCORRECT PASSWORD, PLEASE TRY AGAIN'

################## global "constants" ################

ENTRY = 'LOGON '

################## functions #########################

def runLogin(scr, hardMode, username, password):
    """
    Start the login process

    hardMode - boolean indicating whether the user has to enter the username 
               and password or if they are entered automatically
    username - the username to log in
    password - the password to log in
    Returns true if hardMode == false or if the user entered the correct string
    """
    curses.use_default_colors()
    scr.erase()
    scr.move(0, 0)

    curses.noecho()
    scr.scrollok(True)

    slowWrite(scr, HEADER_TEXT + '\n\n')

    if hardMode:
        # use must enter the correct text to proceed
        entry = ''
        while entry.upper() != ENTRY.upper() + username.upper():
            slowWrite(scr, '> ')
            entry = upperInput(scr)
    else:
        # input is entered for them
        slowWrite(scr, '> ')
        curses.napms(INPUT_PAUSE)
        slowWrite(scr, ENTRY + username.upper() + '\n', TYPE_DELAY)

    slowWrite(scr, '\n' + PASSWORD_PROMPT + '\n\n')

    if hardMode:
        # use must enter the correct text to proceed
        entry = ''
        while entry.upper() != password.upper():
            if entry:
                slowWrite(scr, PASSWORD_ERROR + '\n\n')
            
            slowWrite(scr, '> ')
            entry = upperInput(scr, True)
    else:
        # input is entered for them
        slowWrite(scr, '> ')
        curses.napms(INPUT_PAUSE)
        password_stars = HIDDEN_MASK * len(password)
        slowWrite(scr, password_stars + '\n', TYPE_DELAY)

    curses.napms(500)


def beginLogin(hardMode, username, password):
    """
    Initialize curses and start the login process

    hardMode - boolean indicating whether the user has to enter the username
               and password or if they are entered automatically
    username - the username to log in
    password - the password to log in
    Returns true if hardMode == false or if the user entered the correct string
    """
    res = curses.wrapper(runLogin, hardMode, username, password)
    return res
