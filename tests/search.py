#! /usr/bin/env python3

import os
import sys
import requests
import json
import re
#import pathlib

# oh no ugly :(
# sys.path.append(os.path.abspath(os.path.join('..', 'awccc')))
# from awccc import cache
# from awccc import logic
# from awccc import challenge

query = '''
query ($threadId: Int, $id: Int) {
    ThreadComment (threadId: $threadId, id: $id) {
        comment
        user {
            id
        }
        childComments
        user {
            id
        }
    }
}
'''
# https://anilist.co/forum/thread/61944/comment/2283844
variables = {
    'threadId': 61944,
    'id': 2283844
}

url = 'https://graphql.anilist.co'

response = requests.post(url, json={'query': query, 'variables': variables})

if not response.status_code == 200:
    print(str(response.status_code) + " could not retrieve data")
    print(json.loads(response.text)["errors"][0]["message"])
    print(json.loads(response.text)["errors"][0]["locations"])

resp = json.loads(response.text)["data"]
#get the id
uid = resp["ThreadComment"][0]["user"]["id"]
#print(uid)
content = resp["ThreadComment"][0]["comment"]
if resp["ThreadComment"][0].get("childComments") != None:
    for i in resp["ThreadComment"][0]["childComments"]:
        if uid == i["user"]["id"]:
            content = content + "\n\n---------------------------\n\n"
            content = content + i["comment"]

filename = resp["ThreadComment"][0]["comment"].partition("\n")[0].strip("#_ ").strip("_").replace(" ", "-")
print(content)

with open(filename + ".txt", "w", encoding="utf-8") as f:
    f.write(content)


# url = 'https://awc.moe/challenger/jreeee'
# response = requests.get(url)
# tst = re.compile("href=\"https://anilist.co/forum/thread/\d+/comment/\d+\"")
# name = re.compile("meta\ content=(.*?)\ property")
# ls = tst.findall(response.text)
# meta = name.findall(response.text)
# print(len(ls))
# print(meta)
# thread = []
# comment = []
# for i in range(len(ls)):
#     tmp = ls[i].split("/")
#     threadid = tmp[5]
#     if threadid not in thread:
#         thread.append(tmp[5])
#         comment.append(tmp[7][:-1])

# for i in range(len(comment)):
#     print(str(i) + ": " + thread[i] + " " + comment[i])


# query = '''
# query ($id: Int, $page: Int, $perPage: Int, $search: String) {
#     Page (page: $page, perPage: $perPage) {
#         pageInfo {
#             total
#             currentPage
#             lastPage
#             hasNextPage
#             perPage
#         }
#         media (id: $id, search: $search) {
#             id
#             title {
#                 romaji
#             }
#         }
#     }
# }
# '''
# variables = {
#     'search': 'Mushishi',
#     'page': 1,
#     'perPage': 30
# }