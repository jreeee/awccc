#! /usr/bin/env python3

# main script

import os
import logic
import cache
import challenge
import argparse
import pathlib

def main():
    # setup paths
    CACHE_PATH = os.path.expanduser("~/.cache/awccc/")
    CONFIG_PATH = os.path.expanduser("~/.config/awccc/")
    SCRIPT_PATH = pathlib.Path(__file__).parent.resolve()
    CHALLENGE_PATH = os.path.join(SCRIPT_PATH, "../challenges/")
    CHALLENGE_FILE = os.path.join(CHALLENGE_PATH, "test.txt")
    # handle input
    parser = argparse.ArgumentParser(prog="awccc", 
                                     description="tool to update awc challenge entries",
                                     epilog="more info: https://github.com/jre/awccc")
    parser.add_argument("-l", "--link", type=str, required=False)
    args = parser.parse_args()
    if args.link is not None:
        
        comment = challenge.ChallengeComment(args.link, CHALLENGE_PATH)
        CHALLENGE_FILE = os.path.join(comment.file_path)
    # check
    print(CHALLENGE_FILE)
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
    