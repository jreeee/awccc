#!/usr/bin/env python3

import os
from pathlib import Path
import json

class Cache:
    cfg = {}
    cfg_fp = None
    cache_a = {}
    cache_l = {}
    cache_a_fp = None
    cache_l_fp = None

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.cache_a = {}
        self.cache_l = {}
        self.cache_a_fp = os.path.join(cache_dir, "anime.json")
        self.cache_l_fp= os.path.join(cache_dir, "list.json")
        self.cfg_fp = os.path.join(cache_dir, "awccc.cfg")


        # base dir
        cache_dir = os.path.dirname(self.cache_path)
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

        if os.path.exists(self.cache_a_fp):
            with open(self.cache_a_fp, "r") as f:
                self.cache_a = json.loads(f.read())

        if os.path.exists(self.cache_l_fp):
            with open(self.cache_l_fp, "r") as f:
                self.cache_l = json.loads(f.read())
            
        if os.path.exists(self.cfg_fp):
            with open(self.cfg_fp, "r") as f:
                self.cfg = json.loads(f.read())
                
        else:
            self._write_caches()

    def _write_caches(self):
        with open(self.cache_a_fp, "w+") as f:
            f.write(json.dumps(self.cache_a))
        with open(self.cache_l_fp, "w+") as f:
            f.write(json.dumps(self.cache_l))
        with open(self.cfg_fp, "w+") as f:
            f.write(json.dumps(self.cfg))

    # not working at all but along these lines
    def get_dates(self, id):
        if id not in self.cache_a.keys():
            #retry 
            print("retrying")
            self._write_caches()
        return self.cache_a[id]

def main():
    CACHE_PATH = os.path.expanduser("~/.cache/awccc/")
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)


if __name__ == "__main__":
    main()