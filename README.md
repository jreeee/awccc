## Disclaimer: this is neither affiliated with [anilist](https://anilist.co/) nor [awc](https://anilist.co/user/AWC/) 

## goal

awccc ("a double-u triple-c"/awc challenge checker) is meant to check entries and fill dates for awc challenges. 

i am developing this as adding and checking the dates manually takes a considerable amount of time.

this is a small personal project to practice my python and graphql understanding as well as being a slight qol improvement thing once its done

after working on this for a while i found out that awc has its own [tool](https://awc.moe/challenges/editor) which is quite nice. however since i personally am not a huge fan of webapps this won't deter me (tho its a good reference for some features needed i'd otherwise forget about)
## script

awccc is written in python and uses [anilist's graphql api v2](https://anilist.gitbook.io/anilist-apiv2-docs/)

### setup.py
please run this the first time before using the script, it will generate relevant files the script needs. 

can also be used to clear the cache or config as well as uninstalling the whole script

### running

currently the script reads _challenges/test.txt_ and writes the new file to _challenges/test.txt.new_ from where it can be copied to the comment

at this point in time there are no args to specify anything

### structure

- . contains this git repo

- _~/.cache/awccc/_ contains a list of the shows watched by each user who has locally used the script and a general list containing more specific information to each show
- _~/.config/awccc/_ contains the configuration file

### config file

written in .json, if this is not in valid json the script won't work

contains username

optional: symbols to use, note: not all sybols have to be set

for examples see _presets/_


## bits

fyi: right now all it does is checking the completed list and adding dates

this program will assume, that all challenges use "sharing", i.e. one anime can go on multiple challenges as i don't want to implement a check for that (yet? ever?)

also your profile needs to be set to (semi-)public since i want to avoid dealing with auth stuff (and the challenges require that profile vis anyway)

although the program caches quite a bit of info, it is still a good idea to have a working internet connection when using it