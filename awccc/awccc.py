#! /usr/bin/env python3

# main script

import os
import cache

def main():
    CACHE_PATH = os.path.expanduser("~/.cache/awccc/")
    c = cache.Cache(CACHE_PATH)
    c.get_list("jreeee", "ANIME", "COMPLETED")


if __name__ == "__main__":
    main()
    