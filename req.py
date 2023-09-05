#! /usr/bin/env python3

import requests
import json

# class Entry:
#     def __init__(self, index, username, mediaid):
#         query = '''

#     query($name: String!, $listType: MediaType){
#         MediaListCollection(userName: $name, type: $listType){
#             lists{
#                 name
#                 isCustomList
#                 entries{
#                     ... mediaListEntry
#                 }
#             }
#         }
#     }

#     fragment mediaListEntry on MediaList{
#         mediaId
#         status
#         progress
#         repeat
#         notes
#         startedAt{
#             year
#             month
#             day
#         }
#         media{
#             episodes
#             duration
#             nextAiringEpisode{episode}
#             format
#             title{romaji native english}
#             tags{name}
#             genres
#             meanScore
#             studios{nodes{isAnimationStudio id name}}
#         }
#         scoreRaw: score(format: POINT_100)
#         '''
#         variables = {
#             'username': username,
#             'type': medium,
#             'status': status
#         }

#         url = 'https://graphql.anilist.co'

#         response = requests.post(url, json={'query': query, 'variables': variables})
        
#         self.raw = json.loads(response.text)["data"]["MediaListCollection"]["lists"][0]["entries"]       

class MediaList:
    def __init__(self, username, medium, status):
        query = '''
    query ($username: String, $type: MediaType, $status: MediaListStatus) {
        MediaListCollection(userName: $username, type: $type, status: $status) {
            lists {
                entries {
                    startedAt{
                        year
                        month
                        day
                    }
                    completedAt{
                        year
                        month
                        day
                    }
                    media {
                        id
                        title {
                            english
                            romaji
                        }
                        
                    }
                }
            }
        }
    }
        '''
        variables = {
            'username': username,
            'type': medium,
            'status': status
        }

        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})
        
        self.raw = json.loads(response.text)["data"]["MediaListCollection"]["lists"][0]["entries"]
        
    def title_list(self, format):
        _title_list = []
        for i in range(0,len(self.raw)):
            _title_list.append(self.raw[i]["media"]["title"][format])
        
        return _title_list
    
    def id_list(self):
        _id_list = []
        for i in range(0, len(self.raw)):
            _id_list.append(self.raw[i]["media"]["id"])
            # print(str(self.raw[i]["startedAt"]["year"]) + "-" + str(self.raw[i]["startedAt"]["month"]) + "-"  + str(self.raw[i]["startedAt"]["day"]))
        
        return _id_list
    
    def start_list(self):
        _start_list = []
        for i in range(0, len(self.raw)):
            # formatting
            month = self.raw[i]["startedAt"]["month"]
            month = str(month) if month > 10 else "0" + str(month)
            day = + self.raw[i]["startedAt"]["day"]
            day = str(day) if day > 10 else "0" + str(day)
            date = str(self.raw[i]["startedAt"]["year"]) + "-" + month + "-" + day
            _start_list.append(date)

        return _start_list
    
    def end_list(self):
        _end_list = []
        for i in range(0, len(self.raw)):
            # formatting
            month = self.raw[i]["completedAt"]["month"]
            month = str(month) if month > 10 else "0" + str(month)
            day = + self.raw[i]["completedAt"]["day"]
            day = str(day) if day > 10 else "0" + str(day)
            date = str(self.raw[i]["completedAt"]["year"]) + "-" + month + "-" + day
            _end_list.append(date)

        return _end_list
    

def main():
    m = MediaList("jreeee", "ANIME", "COMPLETED")
    t = m.title_list("romaji")
    i = m.id_list()
    num = 238
    s = m.start_list()
    e = m.end_list()
    print("id: " + str(i[num]) + ", title: " + t[num] + ", start: " + s[num] + ", end: " + e[num])

if __name__ == "__main__":
    main()