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

    chl_head = []
    chl_tail = [] # usually unimportant
    chl_str_list = [] # contains lists with the entries
    chl_list = [] # contains the challenge class

    def __init__(self, file_path):

        # parsing the file

        # opening
        if not os.path.exists(file_path):
            print("couldn't find file at " + file_path)
            sys.exit(1)

        # the script assumes that all challenges follow the "[int][int])" format 
        cs = re.compile("^\d\d")

        # sorting entries into lists
        with open(file_path, "r+") as f:
            entry = []
            state = 0
            for _, line in enumerate(f):
                if cs.match(line) and state != -2:
                    state += 1
                    if state > 1:
                        self.chl_str_list.append(entry)
                        entry = []
                if state == 0:
                    self.chl_head.append(line)
                elif state == -2:
                    self.chl_tail.append(line)
                else:
                    if re.match("^<hr>", line):
                        state = -2
                    else:
                        entry.append(line)
            # the last entry can't be added like the others
            self.chl_str_list.append(entry)
        
        # making challenge objects

        for i in self.chl_str_list:
            print(i)
        # print(int(cs.search(self.chl_str_list[0][0]).group(0)))
        # print(self.chl_head)
        # print(self.chl_str_list)
        # print(self.chl_tail)