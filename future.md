## TODOs
- check that symbols aren't the same
- fix read-in
- fix chl header stuff
- download anime metadata and store it
- actual logic for checks
- a lot more

## Goals

main features when i am done will be:
- automatically adding start/complete timestamps to the challenge entries [done](except specific edge-case)
- marking anime that do not meet _basic challenge reqs_
- check stuff directly from the website, i.e. get the link to the post, gather relevant data, gather rules from the challenge post, make a new file with checked content

## Ideas

things i might add after that:
- show all anime watched after a certain timestamp to see what might be eligible for a challenge
- give a list of shows that could be used for a requirement, based on completed shows and planning shows
- mark challenges with issues via the symbol and write what went wrong into the challenge tail
- maybe maybe have a option to update/generate and post the posts

### Challenge Managagement
_might be its own program?_
- a overview of all completed and ongoing challenges with progess and stuff
- load new challenge codes
- display non completed reqs


## parameters

once im halfway done [not soon]
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

those will update and change as i go, but mark where i kinda want to arrive at