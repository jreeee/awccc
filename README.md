## Disclaimer: this is neither affiliated with [anilist](https://anilist.co/) nor [awc](https://anilist.co/user/AWC/) 

## goal

awccc ("a double-u triple-c"/awc challenge checker) is meant to check entries and fill dates for awc challenges. 

i am developing this as adding and checking the dates manually takes a considerable amount of time especially when only having one monitor.

this is a small personal project to practice my python and graphql understanding as well as being a interesting small project and nice qol thing once its done

after working on it for a while i found out that awc has its own [tool](https://awc.moe/challenges/editor) which is quite nice. i am personally not a huge fan of webapps tho there are some useful features
## script

awccc is written in python and uses [anilist's graphql api v2](https://anilist.gitbook.io/anilist-apiv2-docs/)


## under the hood

### part I challenge
awc challenge requirements are usually structured as follows:

```
[number]) [symbol] [(theme:)] watch an anime [challenge]
https://anilist.co/anime/[id]
start: [yyyy-mm-dd] finish: [yyyy-mm-dd] //[(comment)]
```

- [number] denotes the number of the requirement
- [symbol] the status, i.e. planned, watching, completed
- [theme:] the motto of this entry, can be omitted
- [challenge] the actual challenge
- [id] the id that anime has on anilist
- Dates have to be formatted as noted above
- [comment] some reqs require further info

### part II abstracting
the challenge post must now be abstracted so that we can work with it
- split all the requirements and store them in a list
- match the [challenge] component to their function (if available) otherwise print a comment for manual checking

### part III requesting

- check if the [id]s are in the cache, if they are skip the last step of III
- get the users medialistcollection, recheck and continue
- get the animes entry

### part IV checking

- check if the [challenge] and anime match, update [symbol]
- add start and finish dates if available

### part V done

- overwrite the relevant parts in the input file
- add annotation if the req couldn't be checked

## bits and pieces

fyi: right now all it does is checking the completed list and adding dates

this program will assume, that all challenges use "sharing", i.e. one anime can go on multiple challenges as i don't want to implement a check for that (yet? ever?)
