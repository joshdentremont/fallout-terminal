#! /usr/bin/env python
import fallout_login as login
import fallout_boot as boot
import fallout_locked as locked

if boot.beginBoot(False):
    if login.beginLogin():
        print 'Login successful'
    else:
        locked.beginLocked()
        print 'Login failed'
