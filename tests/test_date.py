#! /usr/bin/env python3

import os
import sys
import pathlib

# oh no ugly :(
sys.path.append(os.path.abspath(os.path.join('..', 'awccc')))
from awccc import cache
from awccc import logic
from awccc import challenge


def main():
    debug = True
    # setting up paths
    CACHE_PATH = os.path.expanduser("~/.cache/awccc/")
    CONFIG_PATH = os.path.expanduser("~/.config/awccc/")
    SCRIPT_PATH = pathlib.Path(__file__).parent.parent.resolve()
    CHALLENGE_FILE = os.path.join(SCRIPT_PATH, "challenges/test.txt")
    # loading config, user anime cache
    c = cache.Cache(CACHE_PATH, CONFIG_PATH, debug)
    # loading the challenge file
    cls = challenge.ChallengeList(CHALLENGE_FILE)
    idl = []
    for i in cls.chl_list:
        idl.append(i.id)
    if debug:
        print(idl)
    idxl = logic.checkCaching(c, idl, debug)
    if debug:
        print(idxl)
    cls.addDates(c, idxl, debug)
    cls.updateHead(c.syms, debug)
    cls.save(CHALLENGE_FILE + ".new")
    print("saved updated challenge post to " + CHALLENGE_FILE + ".new")

if __name__ == "__main__":
    main()