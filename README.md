## Disclaimer I: this is neither affiliated with [anilist](https://anilist.co/) nor [awc](https://anilist.co/user/AWC/)

## Disclaimer II: it's barely functional and i don't really intend continuing the development of this _however_ i do plan to completely rewrite the whole thing in cpp _properly_ when i have enough time

## goal

awccc ("a double-u triple-c"/awc challenge checker) is meant to check entries and fill dates for awc challenges. 

i am developing this as adding and checking the dates manually is too tedious for me.

this is a small personal project to practice my python and graphql understanding as well as being a slight qol improvement thing once its done

after working on this for a while i found out that awc has its own [tool](https://awc.moe/challenges/editor) which is quite nice. however since i personally am not a huge fan of webapps this won't deter me (tho its a good reference for some features needed i'd otherwise forget about)
## script

awccc is written in python and uses [anilist's graphql api v2](https://docs.anilist.co/reference/)

### setup.py
please run this the first time before using the script, it will generate relevant files the script needs. 

can also be used to clear the cache or config as well as uninstalling the whole script

### running

currently the script reads _challenges/test.txt_ and writes the new file to _challenges/test.txt.new_ from where it can be copied to the comment

you can also check challenges via link, using the `-l` argument like `./awccc.py -l https://anilist.co/forum/thread/NUMBER/comment/NUMBER` which will download the challenge and create a `.new` file with filled in dates

by default the script assumes you are filling in anime challenges, for manga challenges you have to add the `-m` argument

**for linux:** if you have `xclip`, you can use `cat path/to/challenge/Some-Challenge.txt.new | xclip -selection clipboard` to copy the challenge to your clipboard, letting you replace the text in AL using `Ctrl + V`

### structure

- . contains this git repo
  - _awccc_ the python files that make it work
  - _challenges_ the original and updated challenges as txt files
  - _presets_ two different configurations to show what's possile for setting status indicators in the config file 

- _~/.cache/awccc/_ contains a list of the shows watched by each user who has locally used the script and a general list containing more specific information to each show
- _~/.config/awccc/_ contains the configuration file

### config file

written in .json, if this is not in valid json the script won't work

contains username

optional: symbols to use, note: not all sybols have to be set

for examples see _presets/_


## bits

fyi: right now all it does is checking the completed list and adding dates, updating the status indicators as needed.

works for anime, manga (-m), and both card links and title links.

this program will assume, that all challenges use "sharing", i.e. one anime can go on multiple challenges as i don't want to implement a check for that (yet? ever?)

also your profile needs to be set to (semi-)public since i want to avoid dealing with auth stuff (and the challenges require that profile vis anyway)

although the program caches quite a bit of info, it is still a good idea to have a working internet connection when using it
