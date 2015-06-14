#! /usr/bin/env python
import fallout_login as login
import fallout_boot as boot
import fallout_locked as locked
import fallout_hack as hack
import sys

hard = False
if len(sys.argv) == 2 and sys.argv[1].lower() == 'hard':
    hard = True

if boot.beginBoot(hard):
    pwd = hack.beginLogin()
    if pwd != None:
        login.beginLogin(hard, 'ADMIN', pwd)
        print 'Login successful'
    else:
        locked.beginLocked()
        print 'Login failed'

