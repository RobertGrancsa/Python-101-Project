#! /usr/bin/env python3

"""
Checks the version of the python the user is running, only allows python 3.8+
"""

import sys


if __name__ == "__main__":
    # Checking if the user is using the correct version of Python
    # Reference:
    #  If Python version is 3.6.5
    #               major --^
    #               minor ----^
    #               micro ------^
    major = sys.version_info[0]
    minor = sys.version_info[1]

    python_version = str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2])

    if major != 3 or major == 3 and minor < 8:
        print("This game requires Python 3.8+\nYou are using Python %s, which is not supported by our game" % (python_version))
        sys.exit(1)

    import game
    game.main()