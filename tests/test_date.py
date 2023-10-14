#! /usr/bin/env python3

import os
import sys
# oh no ugly :(
sys.path.append(os.path.abspath(os.path.join('..', 'awccc')))
from awccc import cache
from awccc import logic
from awccc import challenge

import pathlib

def main():
    debug = True
    # setting up paths
    CACHE_PATH = os.path.expanduser("~/.cache/awccc/")
    SCRIPT_PATH = pathlib.Path(__file__).parent.resolve()
    CHALLENGE_FILE = os.path.join(SCRIPT_PATH, "../challenges/test.txt")
    # loading config, user anime cache
    c = cache.Cache(CACHE_PATH, debug)
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
    # print(cls.chl_list[0].toString())
    # print(cls.chl_list[5].toString())
    # print(cls.chl_list[9].toString())
    # cls.chl_list[1].print()
    # cls.chl_list[5].print()

if __name__ == "__main__":
    main()