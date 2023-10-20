#! /usr/bin/env python3

import sys
import os
import pathlib
import getopt
import requests
import json
from shutil import rmtree

CACHE_PATH = os.path.expanduser("~/.cache/awccc/")
CONFIG_PATH = os.path.expanduser("~/.config/awccc/")
CONFIG_FILE = os.path.expanduser("~/.config/awccc/awccc.cfg")
SCRIPT_PATH = pathlib.Path(__file__).parent.resolve()
CHALLENGE_PATH = os.path.join(SCRIPT_PATH, "challenges/")
PRESET_PATH = os.path.join(SCRIPT_PATH, "presets/")

def usage():
    print("setup/managing script for awccc")
    print("without arguments: create a config file if not present")
    print("-u | username [string]")
    print("-c | copy config preset [int]")
    print("-d | delete ['cache'/'list'/'users'/'config'/'program'/]")
    print("-f | force (no confirmation)")
    print("-h | help message")
    print("example calls:")
    print("./setup.py -u 'test' -c 1 | creates/modifies the config to use the username 'test' using the first preset")
    print("./setup.py -d list | removes the cached animelist")
    print("./setup.py -d users | removes the cached users")
    print("./setup.py -d cache | removes the cache")
    print("./setup.py -d cache -u test | removes the cache of user test")
    print("./setup.py -d program | removes config-, cache- and program files")
    sys.exit(0)

def confirmation(str, force):
    if force:
        return
    res = input("do you want to delete " + str + "? [y/N]")
    if res == '' or res[0] != 'Y' and res[0] != 'y':
        sys.exit(0)

# delete the specified user (or more)
def rmcache(user, force=False):
    # sanity check
    if not os.path.exists(CACHE_PATH):
        print("no cache directory, nothing to remove")
        sys.exit(1)
    
    mode = 0
    str = user + "'s cached list"
    filepath = ""
    if user == "/list/":
        str = "the list of cached titles"
        mode = 1
        filepath = os.path.join(CACHE_PATH, "anime.json")
    elif user == "/all/":
        str = "all the cached content"
        mode = 2
    elif user == "/exlist/":
        str = "all cached users"
        mode = 3

    if mode == 0:
        filepath = os.path.join(CACHE_PATH, f"list-{user.lower()}.json")
        if not os.path.exists(filepath):
            print("cache file not found")
            sys.exit(1)
    
    # are you sure?
    confirmation(str, force)

    if mode < 2:
        os.remove(filepath)
    else:
        for fn in os.listdir(CACHE_PATH):
            filepath = os.path.join(CACHE_PATH, fn)
            if mode == 3 and fn == "anime.json":
                continue
            try:
                if os.path.isfile(filepath) or os.path.islink(filepath):
                    os.unlink(filepath)
            except Exception as e:
                print(f'Failed to delete {filepath}. Reason: {e}')

def rmconfig(force=False):
    if not os.path.exists(CONFIG_FILE):
        if force:
            print("no config directory, skipping")
            return
        else:
            print("no config directory, nothing to remove")
            sys.exit(1)
    confirmation("the config file", force)
    rmtree(CONFIG_PATH)

def rmscript(force=False):
    confirmation("the program", force)
    if not os.path.exists(CONFIG_FILE):
        print("no cache directory, skipping")
    else:
        rmtree(CACHE_PATH)
    rmconfig(True)
    rmtree(SCRIPT_PATH)
    print("removed script")
    sys.exit(0)

def checkvalidity(username, force=False):
    if force:
        return
    
    query = '''
    query ($name: String) {
        User (name: $name) {
            id
        }
    }
    '''
    var = {
        'name': username
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': var})
    if not response.status_code == 200:
        print(str(response.status_code) + " could not retrieve data")
        sys.exit(1)
    id = json.loads(response.text)["data"]["User"]["id"]
    print(f"found user {username} with id {id}")

def createUser(username, preset, force=False):
    file = {}
    if not os.path.exists(CONFIG_PATH):
        os.mkdir(CONFIG_PATH)
    elif os.path.exists(CONFIG_FILE) and not force:
        res = input("do you want to override your config file? [y/N]")
        if res == '' or res[0] != 'Y' and res[0] != 'y':
            sys.exit(0)
        if preset == -1:    
            with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
                file = json.loads(f.read())
        else:
            if os.path.isfile(CONFIG_FILE) or os.path.islink(CONFIG_FILE):
                os.unlink(CONFIG_FILE)

    if preset != -1:
        presetlist = sorted(os.listdir(PRESET_PATH))
        found = False
        for i in range(len(presetlist)):
            if i == int(preset):
                found = True
                with open(os.path.join(PRESET_PATH, presetlist[i]), "r", encoding="utf-8") as f:
                    file = json.loads(f.read())
                break
        if not found:
            print("preset not found, continuing with default preset")

    file["user"] = username
    with open(CONFIG_FILE, "w+", encoding="utf-8") as f:
        f.write(json.dumps(file, indent=4))
    if not os.path.exists(CHALLENGE_PATH):
        os.mkdir(CHALLENGE_PATH)
        with open(os.path.join(CHALLENGE_PATH, "test.txt"), "a", encoding="utf-8") as f:
            f.write("Your Challenge here")

def main():
    arg_list = sys.argv[1:]
    opts = "u:c:d:fh"

    username = ""
    preset = -1
    delete = ""
    force = False

    try:
    # parsing args
        args, _ = getopt.getopt(arg_list, opts)
        # checking each
        for curr_arg, curr_val in args:
            if curr_arg == "-h":
                usage()
            elif curr_arg == "-u":
                username = curr_val
            elif curr_arg in "-c":
                preset = curr_val
            elif curr_arg in "-d":
                delete = curr_val
            elif curr_arg in "-f":
                force = True
            else:
                print("arg not recognized")
                usage()

    except getopt.error as err:
        print(err)

    # rough syntax check
    if preset != -1 and delete != "":
        print("wrong usage, exiting")
        sys.exit(1)

    # deleting stuff
    if delete != "":
        if delete == "cache":
            if username != "":
                rmcache(username, force)
            else:
                rmcache("/all/", force)
        elif delete == "list":
            rmcache("/list/", force)
        elif delete == "users":
            rmcache("/exlist/", force)
        elif delete == "config":
            rmconfig(force)
        elif delete == "script":
            rmscript(force)
        else:
            print("arg not found, exiting")
            sys.exit(1)

    # create user stuff
    if username == "":
        username = input("please enter your anilist username: ")

    checkvalidity(username, force)
    createUser(username, preset, force)

if __name__ == "__main__":
    main()