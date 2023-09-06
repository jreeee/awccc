#! /usr/bin/env python3

# main script

import os
import logic
import cache
import challenge

import pathlib

def main():
    CACHE_PATH = os.path.expanduser("~/.cache/awccc/")
    SCRIPT_PATH = pathlib.Path(__file__).parent.resolve()
    CHALLENGE_FILE = os.path.join(SCRIPT_PATH, "../challenges/test.txt")
    c = cache.Cache(CACHE_PATH)
    c.user = "jreeee"
    # c.get_list(c.user, "ANIME", "COMPLETED")
    # idlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    # newlist = logic.checkCaching(c, idlist)
    # print(newlist)
    print(c.cache_l[0]["media"]["title"]["romaji"])
    cls = challenge.ChallengeList(CHALLENGE_FILE)
    print(cls)

if __name__ == "__main__":
    main()
    