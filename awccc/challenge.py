#! /usr/bin/env python3

import os
import sys
import re
import logic

class Challenge:
    req = 0
    id = 0
    sym = 'o'
    date_s = "YYYY-MM-DD"
    date_f = "YYYY-MM-DD"
    add_str = ""
    chl_str = None

    def __init__ (self, challenge, regex):
        # split the challenge string and store its values
        # atm it won't work if it isn't in the 3-line format
        # TODO for-loop and proper checking

        l1 = regex[0].search(challenge[0])
        l2 = regex[1].search(challenge[1])
        l3 = regex[2].search(challenge[2])

        self.req = l1.group(1)
        self.sym = l1.group(2)
        self.chl_str = l1.group(3)
        self.id = l2.group(1)

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
        if self.add_str != "":
            print("additional: " + self.add_str)

    def toString(self):
        l = []
        l.append(self.req + ") [" + self.sym + "] __" + self.chl_str + "__\n")
        l.append("https://anilist.co/anime/" + self.id + "/\n")
        l.append("Start: " + self.date_s + " Finish: " + self.date_f + " " + self.add_str + "\n")
        return l

class ChallengeList:

    chl_head = []       # contains name, symbol legend and dates
    finish_date = ''    # automatically generated via latest req finish
    start_date = ''     # start date sould be manually set, TODO get via link
    chl_tail = None     # usually unimportant
    chl_str_list = []   # contains lists with the entries
    chl_list = []       # contains the challenge class
    re_list = []

    def __init__(self, file_path):

        # parsing the file

        # opening
        if not os.path.exists(file_path):
            print("couldn't find file at " + file_path)
            sys.exit(1)

        # the script assumes that all challenges follow the "[int/char][int])" format
        # none except the first regex are used in this class, however since we
        # use them a lot the challenge class this should be more efficient
        self.re_list.append(re.compile("^([0-9A-Z]\d)\)\s+\[(.*?)\]\s+__(.*?)__"))
        self.re_list.append(re.compile("^https://anilist.co/anime/(\d+)/*"))
        self.re_list.append(re.compile("^Start:\s+(.*?)\s+Finish:\s+(.*?)\s+(//.*)"))
        self.re_list.append(re.compile("^Start:\s+(.*?)\s+Finish:\s+(.*)"))
        self.re_list.append(re.compile("^Challenge Start Date:\s+(.*)")) 
        self.re_list.append(re.compile("^Challenge Finish Date:\s+(.*)"))
        # there's got to be a better / smarter way to do this...
        self.re_list.append(re.compile("^Legend:\s+\[(.*?)\]\s+=\s+(.*?)\s+\[(.*?)\]\s+=\s+(.*)"))
        self.re_list.append(re.compile("^Legend:\s+\[(.*?)\]\s+=\s+(.*?)\s+\[(.*?)\]\s+=\s+(.*?)\s+\[(.*?)\]\s+=\s+(.*)"))
        self.re_list.append(re.compile("^Legend:\s+\[(.*?)\]\s+=\s+(.*?)\s+\[(.*?)\]\s+=\s+(.*?)\s+\[(.*?)\]\s+=\s+(.*?)\s+\[(.*?)\]\s+=\s+(.*)"))

        # sorting entries into lists
        with open(file_path, "r+", encoding="utf-8") as f:
            entry = []
            state = 0
            for _, line in enumerate(f):
                if state != -2 and self.re_list[0].match(line):
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
                        if self.chl_tail == None:
                            self.chl_tail = []
                        state = -2
                    else:
                        entry.append(line)
            # the last entry can't be added like the others
            self.chl_str_list.append(entry)

        # making challenge objects
        for i in self.chl_str_list:
            self.chl_list.append(Challenge(i, self.re_list))


    def addDates(self, cache, idxl, debug=False):
        idx = 0
        compl = 0
        finish = "YYYY-MM-DD"
        for i in idxl:
            date = logic.dateToString(i, cache.cache_l)
            self.chl_list[idx].date_s = date[0]
            self.chl_list[idx].date_f = date[1]
            # setting according symbols TODO rewatch
            if date[1] == "YYYY-MM-DD":
                if date[0] == "YYYY-MM-DD":
                    self.chl_list[idx].sym = cache.syms[2]
                else:
                    self.chl_list[idx].sym = cache.syms[1]
            else:
                if finish == "YYYY-MM-DD" or finish < date[1]:
                    finish = date[1]
                self.chl_list[idx].sym = cache.syms[0]
                compl += 1
            idx += 1
        if compl != idx:
            print("! not all reqs have been finished")
        # setting the date anyway (basically only applies to seasonals tho)
        self.finish_date = finish
        if debug:
            print("finish date: " + str(self.finish_date) + " latest entry: " + finish)

    def updateHead(self, symlist, debug):
        for i in range(len(self.chl_head)):
            if self.re_list[4].match(self.chl_head[i]):
                start = self.re_list[4].search(self.chl_head[i])
                if start.group(1) != "YYYY-MM-DD":
                    self.start_date = start.group(1)
                else:   
                    # TODO search for post age
                    print("no start date set")
            elif self.re_list[5].match(self.chl_head[i]):
                end = self.re_list[5].search(self.chl_head[i])
                if end.group(1) == "YYYY-MM-DD" or end.group(1) != self.finish_date:
                    self.chl_head[i] = f"Challenge Finish Date: {self.finish_date}\n"
            # bad parser part
            elif self.re_list[6].match(self.chl_head[i]):
                if self.re_list[7].match(self.chl_head[i]):
                    if self.re_list[8].match(self.chl_head[i]):
                        self.chl_head[i] = self.updateSymbols(self.re_list[8].search(self.chl_head[i]), symlist, 4)
                    else:
                        self.chl_head[i] = self.updateSymbols(self.re_list[7].search(self.chl_head[i]), symlist, 3)
                else:
                    self.chl_head[i] = self.updateSymbols(self.re_list[6].search(self.chl_head[i]), symlist, 2)

    # beautiful, innit? the order does not matter
    def updateSymbols(self, symbols, symlist, num):
        keys = [ "Completed", "Not Completed", "Watching", "Rewatching" ]
        mapping = [ 0, 2, 1, 5 ]
        res = "Legend:"
        for i in range(len(keys)):
            for j in range(num):
                # the replace is horrible imho but the easiest fix i could think of
                if keys[i].replace(' ', '') == symbols.group((j+1)*2).replace(' ', ''):
                    res +=  " [" + symlist[mapping[i]] + "] = " + keys[i]
                    break
        return res + "\n"

    def save(self, file_path):
        # todo: checks if not empty
        with open(file_path, "w", encoding="utf-8") as out:
            out.writelines(self.chl_head)
            for i in self.chl_list:
                out.writelines(i.toString())
                out.write("\n")
            if self.chl_tail != None:
                out.write("<hr>\n")
                out.writelines(self.chl_tail)