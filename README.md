## Disclaimer: this is neither affiliated with [anilist](https://anilist.co/) nor [awc](https://anilist.co/user/AWC/) 


**also at this point in time basically none of the things described below are working**

## goal

awccc (awc challenge checker) is meant to check entries and fill dates for awc challenges. 

i am developing this as adding and checking the dates manually takes a considerable amount of time especially when only having one monitor.

this is a small personal project to practice my python and graphql understanding as well as being a nice qol thing once its done

## script

awccc is written in python and uses [anilist's graphql api v2](https://anilist.gitbook.io/anilist-apiv2-docs/)

main features when i am done will be:
- automatically adding start/complete timestamps to the challenge entries
- marking anime that do not meet _basic challenge reqs_

things i might add after that:
- show all anime watched after a certain timestamp to see what might be eligible for a challenge
- give a list of shows that could be used for a requirement, based on completed shows and planning shows
- maybe maybe check stuff directly from the website, i.e. get the link to the post, gather relevant data, gather rules from the challenge post, make a new file with checked content

## parameters
par | val | default val | desc
--- | --- | --- | ---
-h | - | - | help message
-c | - | - | check if reqs are met
-d | - | - | add dates
-m | [int] | 3 | denotes for how many reqs an anime can be used
-r | [int] | 0 | minimum runtime in minutes
-t | [int] | 0 | minimum combined runtime
-p | [int] | 0 | minimum combined popularity
-u | - | - | update the cached medialistcollection
-u | [int] | - | update a specific cached anime
-n | - | - | write the output in a new file
-a | [str] | - | use account name else the one in the config
-o | [str] | - | overwrites account namein config
## under the hood

### part I challenge
awc challenge requirements are usually structured as follows:

```
[number]) [symbol] [(theme:)] watch an anime [challenge]
https://anilist.co/anime/[id]
start: [yyyy-mm-dd] finish: [yyyy-mm-dd]
```

- [number] denotes the number of the requirement
- [symbol] the status, i.e. planned, watching, completed
- [theme:] the motto of this entry, can be omitted
- [challenge] the actual challenge
- [id] the id that anime has on anilist
- Dates have to be formatted as noted above

### part II abstracting
the challenge post must now be abstracted so that we can work with it
- split all the requirements and store them in a list
- match the [challenge] component to their function (if available) otherwise print a comment for manual checking

### part III requesting

- check if the [id]s are in the cache, if they are skip the next step
- get the users medialistcollection, recheck and continue
- get the animes entry

### part IV checking

- check if the [challenge] and anime match, update [symbol]
- add start and finish dates if available

### part V done

- overwrite the relevant parts in the input file
- add annotation if the req couldn't be checked

## bits and pieces

this program will assume, that all challenges use "sharing", i.e. one anime can go on multiple challenges as i don't want to implement a check for that (yet? ever?)