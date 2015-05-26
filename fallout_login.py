#! /usr/bin/env python

import curses
import random
import os

################## global "constants" ################

# number of characters for hex digits and spaces
CONST_WIDTH = 16

# position of the attempt squares
SQUARE_X = 19
SQUARE_Y = 3

LOGIN_ATTEMPTS = 4

# amount of time to pause after correct password input
LOGIN_PAUSE = 3000

# amount of time to pause after lockout
LOCKED_OUT_TIME = 5000

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
    for i in xrange(n):
        list.append(num)
        num += 12
    return list

    
def getSymbols(n):
    """
    return n random symbols
    """
    count = len(SYMBOLS)
    result = ""
    for i in xrange(n):
        result += SYMBOLS[random.randint(0, count - 1)]
    return result


def getPasswords():
    """
    Returns an array of strings to be used as the password and the decoys
    """
    # temporarily hard coded for testing
    #TODO - move the passwords out of this file and add more arrays
    passwords = [
        'FEVER',
        'SEVER',
        'SEWER',
        'SEVEN',
        'ROVER',
        'ERROR',
        'HELLO',
        'BOXER'
    ]

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
        maxSkip = length / pwdCount - pwdLen
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
    width = size[1]
    height = size[0] - 5 # - 5 for header lines

    hexes = generateHex(height * 2)

    hexCol1 = hexes[:height]
    hexCol2 = hexes[height:]

    # generate the symbols and passwords
    fillerLength = width / 2 * height
    passwords = getPasswords()
    filler = getFiller(fillerLength, passwords)
    fillerCol1 = filler[:len(filler) / 2]
    fillerCol2 = filler[len(filler) / 2:]
    
    # each column of symbols and passwords should be 1/4 of the screen
    fillerWidth = width / 4

    # print the header stuff
    scr.addstr('ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL\n')
    scr.addstr('ENTER PASSWORD NOW\n\n')
    scr.addstr(str(LOGIN_ATTEMPTS) + ' ATTEMPT(S) LEFT: ')
    for i in xrange(LOGIN_ATTEMPTS):
        scr.addch(curses.ACS_BLOCK)
        scr.addstr(' ')
    scr.addstr('\n\n')

    # print the hex and filler
    for i in xrange(height):
        scr.addstr("0x%X %s 0x%X %s" % (hexCol1[i], fillerCol1[i * fillerWidth: (i + 1) * fillerWidth], hexCol2[i], fillerCol2[i * fillerWidth: (i + 1) * fillerWidth]))
        if i < height - 1:
            scr.addstr('\n')

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
                     height - cursorPos[0] - 1,
                     width / 2 + CONST_WIDTH,
                     height - 1,
                     width - 1)
    

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
    inputPad = curses.newpad(height, width / 2 + CONST_WIDTH)

    attempts = LOGIN_ATTEMPTS

    # randomly pick a password from the list
    pwd = passwords[random.randint(0, len(passwords) - 1)]
    curses.echo()
    
    while attempts > 0:
        # move the curser to the correct spot for typing
        scr.move(height - 1, width / 2 + CONST_WIDTH + 1)

        # scroll user input up as the user tries passwords
        moveInput(scr, inputPad)
        
        guess = scr.getstr()
        cursorPos = inputPad.getyx()

        # write under the last line of text
        inputPad.move(cursorPos[0] - 1, cursorPos[1] - 1)
        inputPad.addstr('>' + guess.upper() + '\n')

        # user got password right
        if guess.upper() == pwd.upper():
            inputPad.addstr('>Exact match!\n')
            inputPad.addstr('>Please wait\n')
            inputPad.addstr('>while system\n')
            inputPad.addstr('>is accessed.\n')

            moveInput(scr, inputPad)

            curses.napms(LOGIN_PAUSE)
            return
            
        # wrong password
        else:
            pwdLen = len(pwd)
            matched = 0
            try:
                for i in xrange(pwdLen):
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
        for i in xrange(LOGIN_ATTEMPTS):
            if i < attempts:
                scr.addch(curses.ACS_BLOCK)
            else:
                scr.addstr(' ')
            scr.addstr(' ')

    # Out of attempts
    scr.erase()
    scr.move(height / 2 - 1, width / 2 - 7)
    scr.addstr('TERMINAL LOCKED')
    scr.move(height / 2 + 1, width / 2 - 16)
    scr.addstr('PLEASE CONTACT AN ADMINISTRATOR')
    curses.curs_set(0)
    scr.refresh()

    curses.napms(LOCKED_OUT_TIME)
        
def runLogin(scr):
    """
    Start the login portion of the terminal
    """
    random.seed()
    passwords = initScreen(scr)
    userInput(scr, passwords)


def beginLogin():
    """
    Initialize curses and start the login process
    """
    scr = curses.initscr()
    curses.wrapper(runLogin)
