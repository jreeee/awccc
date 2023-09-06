#! /usr/bin/env python3

import os
import sys
import re

class Challenge:
    req = 0
    id = 0
    sym = 'o'
    date_s = "YYYY-MM_DD"
    date_f = "YYYY-MM_DD"
    add_str = None
    chl_str = None

    def __init__ (self, challenge, regex):
        # split the challenge string and store its values
        # atm it won't work if it isn't in the 3-line format
        
        l1 = regex[0].search(challenge[0])
        l2 = regex[1].search(challenge[1])
        l3 = regex[2].search(challenge[2])
  
        self.req = l1.group(1)
        self.sym = l1.group(2)
        self.chl_str = l1.group(3)
        self.id = l2.group(0)

        if l3:
            self.add_str = l3.group(3)
        else:
            l3 = regex[3].search(challenge[2])

        self.date_s = l3.group(1)
        self.date_f = l3.group(2)

    def print(self):
        print("requirement: " + self.req)
        print("id: " + str(self.id))
        print("symbol: " + self.sym)
        print("dates: " + self.date_s + ", " + self.date_f)
        print("challenge: " + self.chl_str)
        if self.add_str != None:
            print("additional: " + self.add_str)

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
        # none except the first regex are used in this class, however since we
        # use them a lot the challenge class this should be more efficient
        re_list = []
        re_list.append(re.compile("^([0-9A-Z]\d)\)\s+\[(.*?)\]\s+__(.*?)__"))
        re_list.append(re.compile("^https://anilist.co/anime/(\d+)/"))
        re_list.append(re.compile("^Start:\s+(.*?)\s+Finish:\s+(.*?)\s+//(.*)"))
        re_list.append(re.compile("^Start:\s+(.*?)\s+Finish:\s+(.*)"))

        # sorting entries into lists
        with open(file_path, "r+") as f:
            entry = []
            state = 0
            for _, line in enumerate(f):
                if re_list[0].match(line) and state != -2:
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
            self.chl_list.append(Challenge(i, re_list))