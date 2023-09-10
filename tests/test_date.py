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
    c.user = "jreeee"
    # c.get_list(c.user, "ANIME", "COMPLETED")
    #idl= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    #newlist = logic.checkCaching(c, idlist)
    #print(newlist)
    #print("cache test:")
    #print("-------")
    cls = challenge.ChallengeList(CHALLENGE_FILE)
    idl = []
    for i in cls.chl_list:
        idl.append(i.id)
    print(idl)
    idxl = logic.checkCaching(c, idl)
    #print(c.cache_l[0]["media"]["title"]["romaji"])
    print(idxl)
    idx = 0
    for i in idxl:
        if i != -1:
            date = logic.dateToString(c.cache_l[i])
            cls.chl_list[idx].date_s = date[0]
            cls.chl_list[idx].date_f = date[1]
        else:
            cls.chl_list[idx].date_s = "YYYY-MM-DD"
            cls.chl_list[idx].date_f = "YYYY-MM-DD"
        idx += 1

    cls.save(CHALLENGE_FILE + ".new")
    # print(cls.chl_list[0].toString())
    # print(cls.chl_list[5].toString())
    # print(cls.chl_list[9].toString())
    # cls.chl_list[1].print()
    # cls.chl_list[5].print()

if __name__ == "__main__":
    main()