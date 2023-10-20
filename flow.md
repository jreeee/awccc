## under the hood

### part I challenge
awc challenge requirements are usually structured as follows:

```
[char/number,number]) [symbol] [(theme:)] watch an anime [challenge]
https://anilist.co/anime/[id]
start: [yyyy-mm-dd] finish: [yyyy-mm-dd] //[(comment)]
```

- [number] denotes the number of the requirement
- [symbol] the status, i.e. planned, watching, completed
- [theme:] the motto of this entry, can be omitted
- [challenge] the actual challenge
- [id] the id that anime has on anilist
- Dates have to be formatted as noted above
- [comment] some reqs require further info ! there can be multiple comments

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

- update the challenge head to use user symbols and set the end date
- overwrite the relevant parts in the input file
- add annotation if the req couldn't be checked

