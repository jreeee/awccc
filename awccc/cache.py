#! /usr/bin/env python3

# get info about the shows (from anilist and from cache)

# ideally the id of the anime would also be its index, 
# however i'm unsure if that would really be faster, given
# that we don't query a lot of data

# todo user specific lists (not anime.json)

import os
import json
import requests

class Cache:
    user = None
    cfg_fp = None
    cache_a = {}
    cache_l = {}
    cache_a_fp = None
    cache_l_fp = None

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.cache_a = {}
        self.cache_l = {}
        self.cache_a_fp = os.path.join(cache_path, "anime.json")
        self.cache_l_fp= os.path.join(cache_path, "list.json")
        self.cfg_fp = os.path.join(cache_path, "awccc.cfg")

        if not os.path.exists(cache_path):
            os.mkdir(cache_path)

        if os.path.exists(self.cache_a_fp):
            with open(self.cache_a_fp, "rb") as f:
                self.cache_a = json.loads(f.read())

        if os.path.exists(self.cache_l_fp):
            with open(self.cache_l_fp, "rb") as f:
                self.cache_l = json.loads(f.read())
            
        if os.path.exists(self.cfg_fp):
            with open(self.cfg_fp, "rb") as f:
                self.cfg = json.loads(f.read())
                
        else:
            self._write_caches()

    def _write_caches(self):
        with open(self.cache_a_fp, "w+", encoding="utf-8") as f:
            f.write(json.dumps(self.cache_a))
        with open(self.cache_l_fp, "w+", encoding="utf-8") as f:
            f.write(json.dumps(self.cache_l))
        with open(self.cfg_fp, "w+", encoding="utf-8") as f:
            f.write(json.dumps(self.cfg))

    # not working at all but along these lines
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