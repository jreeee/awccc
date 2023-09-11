#! /usr/bin/env python3

# get info about the shows (from anilist and from cache)

# ideally the id of the anime would also be its index, 
# however i'm unsure if that would really be faster, given
# that we don't query a lot of data

# todo user specific lists (not anime.json)

import sys
import os
import json
import requests

class Cache:
    cache_a = {}
    cache_l = {}
    cfg = {}
    user = None
    syms = []
    cache_a_fp = None
    cache_l_fp = None
    cfg_fp = None

    def __init__(self, cache_path):

        self.cache_path = cache_path
        self.syms = [ "X", "W", "O", "*", "!" ]
        self.cfg = {}
        self.cfg_fp = os.path.join(cache_path, "awccc.cfg")     

        if not os.path.exists(cache_path):
            os.mkdir(cache_path)

        if os.path.exists(self.cfg_fp):
            with open(self.cfg_fp, "r+", encoding="utf-8") as f:
                self.cfg = json.loads(f.read())
            self.check_cfg()

        else:
            print(f"please use the setup or manually write yout config to {self.cfg_fp}")
            sys.exit(1)

        self.cache_a = {}
        self.cache_l = {}
        self.cache_a_fp = os.path.join(cache_path, "anime.json")
        self.cache_l_fp= os.path.join(cache_path, f"list-{self.user}.json")

        if os.path.exists(self.cache_a_fp):
            with open(self.cache_a_fp, "r+", encoding="utf-8") as f:
                self.cache_a = json.loads(f.read())

        if os.path.exists(self.cache_l_fp):
            with open(self.cache_l_fp, "r+", encoding="utf-8") as f:
                self.cache_l = json.loads(f.read())
                
        else:
            self._write_caches()

    def _write_caches(self):
        with open(self.cache_a_fp, "w+", encoding="utf-8") as f:
            f.write(json.dumps(self.cache_a, indent=4))
        with open(self.cache_l_fp, "w+", encoding="utf-8") as f:
            f.write(json.dumps(self.cache_l, indent=4))
        with open(self.cfg_fp, "w+", encoding="utf-8") as f:
            f.write(json.dumps(self.cfg, indent=4))

    def check_cfg(self):
        # getting the username
        try:
            if self.cfg["user"] == "":
                print("missing username in config")
                sys.exit(1)
            self.user = self.cfg["user"]
            print("user is " + self.user)
        except:
            print("user attr in config missing")
            sys.exit(1)

        keys = [ "completed", "watching", "notcompl", "notchk", "failchk" ]
        for i in range(len(keys)):
            for j in self.cfg["symbols"]:
                if keys[i] == j and self.cfg["symbols"][j] != "":
                    self.syms[i] = self.cfg["symbols"][j]


    def get_list(self, username, medium, status):
        query = '''
    query ($username: String, $type: MediaType, $status: MediaListStatus) {
        MediaListCollection(userName: $username, type: $type, status: $status) {
            lists {
                entries {
                    media {
                        id
                        title {
                            english
                            romaji
                        }
                        
                    }
                    startedAt{
                        year
                        month
                        day
                    }
                    completedAt{
                        year
                        month
                        day
                    }
                }
            }
        }
    }
        '''
        variables = {
            'username': username,
            'type': medium,
            'status': status
        }

        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})
        
        if not response.status_code == 200:
           print(str(response.status_code) + " could not retrieve data")
           return
        self.cache_l = json.loads(response.text)["data"]["MediaListCollection"]["lists"][0]["entries"]
        self._write_caches()