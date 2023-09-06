#! /usr/bin/env python3

import os
import sys
import re

class Challenge:
    req = 0
    sym = 'o'
    chl_str = None
    id = 0
    dates = None

    def __init__ (self, challenge):
        # split the challenge string and store the values
        self.req = -1

class ChallengeList:

    chl_str_list = []
    chl_list = []

    def __init__(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r+") as f:
                for _, line in enumerate(f):
                    self.chl_str_list.append(line)
        else:
            print("couldn't find file at " + file_path)
            sys.exit(1)

        print(self.chl_str_list)