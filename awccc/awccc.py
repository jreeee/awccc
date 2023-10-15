#! /usr/bin/env python3

# main script

import os
import logic
import cache
import challenge

import pathlib

def main():
    CACHE_PATH = os.path.expanduser("~/.cache/awccc/")
    CONFIG_PATH = os.path.expanduser("~/.config/awccc/")
    SCRIPT_PATH = pathlib.Path(__file__).parent.resolve()
    CHALLENGE_FILE = os.path.join(SCRIPT_PATH, "../challenges/test.txt")

    c = cache.Cache(CACHE_PATH, CONFIG_PATH)
    cls = challenge.ChallengeList(CHALLENGE_FILE)
    idl = []
    for i in cls.chl_list:
        idl.append(i.id)
    idxl = logic.checkCaching(c, idl)
    cls.addDates(c, idxl)
    cls.updateHead(c.syms)
    cls.save(CHALLENGE_FILE + ".new")
    print("saved updated file")

if __name__ == "__main__":
    main()
    