#! /usr/bin/env python
import fallout_login as login
import fallout_boot as boot
import fallout_locked as locked
import sys

hard = False
if len(sys.argv) == 2 and sys.argv[1].lower() == 'hard':
    hard = True

if boot.beginBoot(hard):
    if login.beginLogin():
        print 'Login successful'
    else:
        locked.beginLocked()
        print 'Login failed'
