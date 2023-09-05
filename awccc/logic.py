#! /usr/bin/env python3

def checkCaching(cache, list):
    
    newlist = createIdxList(cache, list)
    req = False

    for i in newlist:
        if i == -1:
            req = True
            break

    # update cache
    if req == False:
        return newlist
    else:
        cache.get_list(cache.user, "ANIME", "COMPLETED")
        return createIdxList(cache, list)
    
    
def createIdxList(cache, list):
    newlist = []
    for i in list:
        idx = 0
        app = -1
        for j in cache.cache_l:
            if j["media"]["id"] == i:
                print("id: " + str(i) + " idx: " + str(idx) + " found " + j["media"]["title"]["romaji"])
                app = idx
                break
            idx += 1
        newlist.append(app)
    return newlist

def addDate(idx):  
    print("Start: " + str(idx["startedAt"]["year"]) + "-" 
        + str(idx["startedAt"]["month"]) + "-" + str(idx["startedAt"]["day"]) 
        + " Finish: " + str(idx["completedAt"]["year"]) + "-" 
        + str(idx["completedAt"]["month"]) + "-" + str(idx["completedAt"]["day"]))

# parse and eval the challenges