#! /usr/bin/env python3

import os
import sys
# oh no ugly :(
sys.path.append(os.path.abspath(os.path.join('..', 'awccc')))
from awccc import cache
from awccc import logic
from awccc import challenge

# maybe
import pathlib

def main():
    CACHE_PATH = os.path.expanduser("~/.cache/awccc/")
    SCRIPT_PATH = pathlib.Path(__file__).parent.resolve()
    CHALLENGE_FILE = os.path.join(SCRIPT_PATH, "../challenges/test.txt")
    c = cache.Cache(CACHE_PATH)
    
    cls = challenge.ChallengeList(CHALLENGE_FILE)
    idl = []
    for i in cls.chl_list:
        idl.append(i.id)
    print(idl)
    idxl = logic.checkCaching(c, idl)
    print(idxl)
    cls.addDates(c, idxl)

    cls.save(CHALLENGE_FILE + ".new")
    # print(cls.chl_list[0].toString())
    # print(cls.chl_list[5].toString())
    # print(cls.chl_list[9].toString())
    # cls.chl_list[1].print()
    # cls.chl_list[5].print()

if __name__ == "__main__":
    main()