#! /usr/bin/env python3

import os
import sys
import re
import logic
import requests
import json

class Challenge:
    req = 0
    id = 0
    sym = 'o'
    name = ""
    date_s = "YYYY-MM-DD"
    date_f = "YYYY-MM-DD"
    add_str = ""
    chl_str = None
    var = "anime"
    card = True

    def __init__ (self, challenge, regex, variant):
        # split the challenge string and store its values
        # atm it won't work if it isn't in the 3-line format
        # TODO for-loop and proper checking

        l1 = regex[0].search(challenge[0])
        l2 = regex[1].search(challenge[1])
        l3 = regex[2].search(challenge[2])

        self.req = l1.group(1)
        self.sym = l1.group(2)
        self.chl_str = l1.group(3)
        self.var = variant

        # card link
        if l2 != None:
            self.id = l2.group(1)

        # MD link !!NOT CHECKING FOR CORRECT TITLE!!
        else:
            l2 = regex[9].search(challenge[1])
            if l2 != None:
                self.card = False
                self.name = l2.group(1)
                self.id = l2.group(2)
            else:
                self.id = 0

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
        if self.card:
            l.append(f"https://anilist.co/{self.var}/{self.id}\n")
        else:
            l.append(f"[{self.name}](https://anilist.co/{self.var}/{self.id})\n")
        l.append(f"Start: {self.date_s} Finish: {self.date_f} {self.add_str}\n")
        return l

class ChallengeList:

    chl_head = []       # contains name, symbol legend and dates
    finish_date = ''    # automatically generated via latest req finish
    start_date = ''     # start date sould be manually set, TODO get via link
    chl_tail = None     # usually unimportant
    chl_str_list = []   # contains lists with the entries
    chl_list = []       # contains the challenge class
    re_list = []

    def __init__(self, file_path, is_manga):

        # parsing the file

        # opening
        if not os.path.exists(file_path):
            print("couldn't find file at " + file_path)
            sys.exit(1)
        if is_manga:
            variant = "manga"
        else:
            variant = "anime"

        # this does currently not work with Tarot and Collection Challenges!

        # the script assumes that all challenges follow the "[int/char][int])" format
        # none except the first regex are used in this class, however since we
        # use them a lot the challenge class this should be more efficient
        self.re_list.append(re.compile("^([0-9A-Z]\\d)\\)\\s+\\[(.*?)\\]\\s+__(.*?)__"))
        self.re_list.append(re.compile("^https://anilist.co/" + variant + "/(\\d+)/*"))
        self.re_list.append(re.compile("^Start:\\s+(.*?)\\s+Finish:\\s+(.*?)\\s+(//.*)"))
        self.re_list.append(re.compile("^Start:\\s+(.*?)\\s+Finish:\\s+(.*)"))
        self.re_list.append(re.compile("^Challenge Start Date:\\s+(.*)")) 
        self.re_list.append(re.compile("^Challenge Finish Date:\\s+(.*)"))

        # there's got to be a better / smarter way to do this...
        self.re_list.append(re.compile("^Legend:\\s+\\[(.*?)\\]\\s+=\\s+(.*?)\\s+\\[(.*?)\\]\\s+=\\s+(.*)"))
        self.re_list.append(re.compile("^Legend:\\s+\\[(.*?)\\]\\s+=\\s+(.*?)\\s+\\[(.*?)\\]\\s+=\\s+(.*?)\\s+\\[(.*?)\\]\\s+=\\s+(.*)"))
        self.re_list.append(re.compile("^Legend:\\s+\\[(.*?)\\]\\s+=\\s+(.*?)\\s+\\[(.*?)\\]\\s+=\\s+(.*?)\\s+\\[(.*?)\\]\\s+=\\s+(.*?)\\s+\\[(.*?)\\]\\s+=\\s+(.*)"))

        # oh no
        self.re_list.append(re.compile("^\\[(.*?)\\]\\(https://anilist.co/" + variant + "/(\\d+)/*\\)"))


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
            self.chl_list.append(Challenge(i, self.re_list, variant))


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

    def updateHead(self, symlist, debug=False):
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

class ChallengeComment:

    file_path = ""

    def __init__(self, link, path, debug=False):
        info = re.compile("^https://anilist.co/forum/thread/(\\d+)/comment/(\\d+)*")
        ids = info.search(link)
        query = '''
query ($threadId: Int, $id: Int) {
    ThreadComment (threadId: $threadId, id: $id) {
        comment
        user {
            id
        }
        childComments
        user {
            id
        }
    }
}
'''
        variables = {
            'threadId': ids.group(1),
            'id': ids.group(2)
            }
        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})

        if not response.status_code == 200:
            print(str(response.status_code) + " could not retrieve data")
            print(json.loads(response.text)["errors"][0]["message"])
            print(json.loads(response.text)["errors"][0]["locations"])
            sys.exit(1)
        
        resp = json.loads(response.text)["data"]
        #get the id
        uid = resp["ThreadComment"][0]["user"]["id"]
        #print(uid)
        content = resp["ThreadComment"][0]["comment"]
        if resp["ThreadComment"][0].get("childComments") != None:
            for i in resp["ThreadComment"][0]["childComments"]:
                if uid == i["user"]["id"]:
                    content = content + "\n\n---------------------------\n\n"
                    content = content + i["comment"]

        file_name = resp["ThreadComment"][0]["comment"].partition("\n")[0].strip("#_ ").strip("_").replace(" ", "-")
        self.file_path = os.path.join(path, file_name + ".txt")
        if debug:
            print(content)

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(content)