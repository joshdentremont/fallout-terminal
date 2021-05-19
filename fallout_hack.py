import curses
import random
import time
import os
from fallout_functions import slowWrite
from fallout_functions import upperInput

################## text strings ######################

HEADER_TEXT = 'ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL'

################## global "constants" ################

# number of characters for hex digits and spaces
CONST_CHARS = 16

# position of the attempt squares
SQUARE_X = 19
SQUARE_Y = 3

LOGIN_ATTEMPTS = 4

HEADER_LINES = 5

# amount of time to pause after correct password input
LOGIN_PAUSE = 3000

# starting number for hex generation
START_HEX = 0xf650

# list of possible symbols for password hiding
SYMBOLS = '!@#$%^*()_-+={}[]|\\:;\'",<>./?'

################## functions #########################

def generateHex(n):
    """
    generates n numbers starting at START_HEX and increasing by 12 each time
    """
    num = START_HEX
    list = []
    for i in range(n):
        list.append(num)
        num += 12
    return list

    
def getSymbols(n):
    """
    return n random symbols
    """
    count = len(SYMBOLS)
    result = ""
    for i in range(int(n)):
        result += SYMBOLS[random.randint(0, count - 1)]
    return result


def getPasswords():
    """
    Returns an array of strings to be used as the password and the decoys
    """
    groups = []

    # script file / password file location
    __location__ = os.path.realpath(os.path.join(os.getcwd(),
                                                 os.path.dirname(__file__)))
    
    # read from passwords.txt
    with open(os.path.join(__location__, "passwords.txt")) as pwfile:
        for line in pwfile:
            if not line.strip():
                groups.append([])
            elif len(groups) > 0:
                groups[len(groups) - 1].append(line[:-1])

    passwords = groups[random.randint(0, len(groups) - 1)]

    random.shuffle(passwords)
    return passwords


def getFiller(length, passwords):
    """
    Return a string of symbols with potential passwords mixed in

    length - the length of the string to create
    passwords - an array of passwords to hide in the symbols
    """
    filler = getSymbols(length)
    
    # add the passwords to the symbols
    pwdLen = len(passwords[0])
    pwdCount = len(passwords)
    i = 0
    for pwd in passwords:
        # skip a distance based on total size to cover then place a password
        maxSkip = int(length / pwdCount - pwdLen)
        i += random.randint(maxSkip - 2, maxSkip)
        filler = filler[:i] + pwd + filler[i + pwdLen:]
        i += pwdLen
    return filler
    

def initScreen(scr):
    """
    Fill the screen to prepare for password entry
    
    scr - curses window returned from curses.initscr()
    """
    size = scr.getmaxyx()
    height = size[0]
    width = size[1]
    fillerHeight = height - HEADER_LINES

    hexes = generateHex(fillerHeight * 2)

    hexCol1 = hexes[:fillerHeight]
    hexCol2 = hexes[fillerHeight:]

    # generate the symbols and passwords
    fillerLength = width / 2 * fillerHeight
    passwords = getPasswords()
    filler = getFiller(fillerLength, passwords)
    fillerCol1, fillerCol2 = filler[0:len(filler)//2], filler[len(filler)//2:]
	
    #print(fillerCol1)
    #time.sleep(15)
    #print(fillerCol2)
    #time.sleep(15)
    
    # each column of symbols and passwords should be 1/4 of the screen
    fillerWidth = int(width / 4)

    # print the header stuff
    slowWrite(scr, HEADER_TEXT)
    slowWrite(scr, '\nENTER PASSWORD NOW\n\n')
    slowWrite(scr, str(LOGIN_ATTEMPTS) + ' ATTEMPT(S) LEFT: ')
    for i in range(LOGIN_ATTEMPTS):
        scr.addch(curses.ACS_BLOCK)
        slowWrite(scr, ' ')
    slowWrite(scr, '\n\n')

    # print the hex and filler
    t = 0
    for i in range(fillerHeight):
        slowWrite(scr, "0x%X %s" % (hexCol1[i], fillerCol1[t:t + 28]), 1)
        if i < fillerHeight - 1:
            scr.addstr('\n')
        t= t+28

    t = 0
    for i in range(fillerHeight):
        scr.move(HEADER_LINES + i, int(CONST_CHARS / 2 + fillerWidth))
        slowWrite(scr, '0x%X %s' % (hexCol2[i], fillerCol2[t:t + 28]), 1)
        t= t+28

    scr.refresh()

    return passwords


def moveInput(scr, inputPad):
    """
    moves the input pad to display all text then a blank line then the cursor
    """
    size = scr.getmaxyx()
    height = size[0]
    width = size[1]
    
    inputPad.addstr('\n>')

    # cursor position relative to inputPad
    cursorPos = inputPad.getyx()

    inputPad.refresh(0, 0,
                     int(height - cursorPos[0] - 1),
                     int(width / 2 + CONST_CHARS),
                     int(height - 1),
                     int(width - 1))
    

def userInput(scr, passwords):
    """
    let the user attempt to crack the password

    scr - curses window returned from curses.initscr()
    passwords - array of passwords hidden in the symbols
    """
    size = scr.getmaxyx()
    height = size[0]
    width = size[1]
    
    # set up a pad for user input
    inputPad = curses.newpad(height, int(width / 2 + CONST_CHARS))

    attempts = LOGIN_ATTEMPTS

    # randomly pick a password from the list
    pwd = passwords[random.randint(0, len(passwords) - 1)]
    curses.noecho()
    
    while attempts > 0:
        # move the curser to the correct spot for typing
        scr.move(int(height - 1), int(width / 2 + CONST_CHARS + 1))

        # scroll user input up as the user tries passwords
        moveInput(scr, inputPad)
        
        guess = upperInput(scr, False, False)
        cursorPos = inputPad.getyx()

        # write under the last line of text
        inputPad.move(cursorPos[0] - 1, cursorPos[1] - 1)
        inputPad.addstr('>' + guess.upper() + '\n')

        debug = "newvegas"

        # user got password right
        if guess.upper() == pwd.upper() or guess.upper() == debug.upper():
            inputPad.addstr('>Exact match!\n')
            inputPad.addstr('>Please wait\n')
            inputPad.addstr('>while system\n')
            inputPad.addstr('>is accessed.\n')

            moveInput(scr, inputPad)

            curses.napms(LOGIN_PAUSE)
            return pwd
            
        # wrong password
        else:
            pwdLen = len(pwd)
            matched = 0
            try:
                for i in range(pwdLen):
                    if pwd[i].upper() == guess[i].upper():
                        matched += 1
            except IndexError:
                pass # user did not enter enough letters
                
            inputPad.addstr('>Entry denied\n')
            inputPad.addstr('>' + str(matched) + '/' + str(pwdLen) +
                            ' correct.\n')
        
        attempts -= 1
        # show remaining attempts
        scr.move(SQUARE_Y, 0)
        scr.addstr(str(attempts))
        scr.move(SQUARE_Y, SQUARE_X)
        for i in range(LOGIN_ATTEMPTS):
            if i < attempts:
                scr.addch(curses.ACS_BLOCK)
            else:
                scr.addstr(' ')
            scr.addstr(' ')

    # Out of attempts
    return None
        
def runLogin(scr):
    """
    Start the login portion of the terminal
    Returns the password if the user correctly guesses it
    """
    curses.use_default_colors()
    size = scr.getmaxyx()
    width = size[1]
    height = size[0]
    random.seed()
    # set screen to initial position
    scr.erase()
    scr.move(0, 0)
    passwords = initScreen(scr)
    return userInput(scr, passwords)


def beginLogin():
    """
    Initialize curses and start the login process
    Returns the password if the user correctly guesses it
    """
    return curses.wrapper(runLogin)
