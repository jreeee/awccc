#! /usr/bin/env python3

def checkCaching(cache, list, debug=False):
    
    if debug:
        print("round one: checking cached anime")
    idl = [-1]*len(list)
    newlist = createIdxList(cache, list, idl, debug)
    req = False

    for i in newlist:
        if i == -1:
            req = True
            break

    # update cache
    if req == False:
        return newlist
    else:
        if debug:
            print("round two: update cache to get missing shows")
        cache.get_list(cache.user, "ANIME", "COMPLETED")
        return createIdxList(cache, list, newlist, debug)
    
# force would be set to true if you want to update a cached anime which should happen rarely    
def createIdxList(cache, list, idl, debug, force=False):
    newlist = []
    for i in range(len(list)):
        # this is used on the second run when the list presumably has some entries
        # would work if adding stuff were to not affect the indices
        # if not force and idl[i] != -1:
        #     newlist.append(idl[i])
        # else:
        idx = 0
        app = -1
        for j in cache.cache_l:
            if j["media"]["id"] == int(list[i]):
                if debug:
                    print("> id: " + str(list[i]) + " idx: " + str(idx) + " found " + j["media"]["title"]["romaji"])
                app = idx
                break
            idx += 1
        if app == -1:
            print("! id: " + str(list[i]) + " idx : - could not find in list")
        newlist.append(app)
    return newlist

def dateToString(id, cache_l):
    if id == -1:
        return [ "YYYY-MM-DD" ] * 2
    idx = cache_l[id]
    l = []
    l.append(str(idx["startedAt"]["year"]) + "-" 
             + pad(idx["startedAt"]["month"]) 
             + "-" + pad(idx["startedAt"]["day"]))
    l.append(str(idx["completedAt"]["year"]) + "-" 
             + pad(idx["completedAt"]["month"]) 
             + "-" + pad(idx["completedAt"]["day"]))
    return l    

def pad(num):
    if num < 10:
        return "0" + str(num)
    return str(num)

def addDate(idx):
    if idx == -1:
        return
    print("Start: " + str(idx["startedAt"]["year"]) + "-" 
        + str(idx["startedAt"]["month"]) + "-" + str(idx["startedAt"]["day"]) 
        + " Finish: " + str(idx["completedAt"]["year"]) + "-" 
        + str(idx["completedAt"]["month"]) + "-" + str(idx["completedAt"]["day"]))

# parse and eval the challenges