Fallout Terminal
================

Simulates a computer terminal from fallout.

Currently only implements the login portion.

Usage
================

```
python fallout.py
```

or for hard mode where the user must manually enter the correct input in the
boot script,

```
python fallout.py hard
```

To only use the login in another program:

```
import fallout_login

# returns true if the correct password is entered, false otherwise
fallout_login.beginLogin()
```

Passwords
================

To add your own lists of passwords, check out the passwords.txt file

Notes
================

Check out cool-retro-term
(https://github.com/Swordfish90/cool-retro-term) to make your terminal
look like a fallout terminal
