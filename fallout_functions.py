import curses

LETTER_PAUSE = 20

def slowWrite(window, text, pause = LETTER_PAUSE):
    """
    wrapper for curses.addstr() which writes the text slowely 
    """
    for i in xrange(len(text)):
        window.addstr(text[i])
        window.refresh()
        curses.napms(pause)
