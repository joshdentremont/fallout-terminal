import curses
import time
import sys

LETTER_PAUSE = 5

INPUT_PAUSE = 500 # ms

TYPE_DELAY = 30

HIDDEN_MASK = '*'

NEWLINE = 10

DELETE = 127

def slowWrite(window, text, pause = LETTER_PAUSE):
    """
    wrapper for curses.addstr() which writes the text slowely 
    """
    for i in xrange(len(text)):
        window.addstr(text[i])
        window.refresh()
        curses.napms(pause)

def upperInput(window, hidden = False, can_newline = True):
    """
    Reads user input until enter key is pressed. Echoes the input in upper case

    hidden - if true the output will be masked
    can_newline - if true the input is followed by a newline and the screen is
                  scrolled if necessary
    """
    inchar = 0
    instr = ''
    while inchar != NEWLINE:
        inchar = window.getch()
        # convert lower case to upper
        if inchar > 96 and inchar < 123:
            inchar -= 32
        # deal with backspace
        if inchar == DELETE:
            if len(instr) > 0:
                instr = instr[:-1]
                cur = window.getyx()
                window.move(cur[0], cur[1] - 1)
                window.clrtobot()
            else:
                continue
        elif inchar > 255:
            continue
        # output the character
        elif inchar != NEWLINE:
            instr += chr(inchar)
            if hidden:
                window.addch(HIDDEN_MASK)
            else:
                window.addch(inchar)
        elif can_newline:
            window.addch(NEWLINE)
    return instr
