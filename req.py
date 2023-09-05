#! /usr/bin/env python3

import requests
import json

class Entry:
    def __init__(self, index, username, mediaid):
        query = '''

    query($name: String!, $listType: MediaType){
        MediaListCollection(userName: $name, type: $listType){
            lists{
                name
                isCustomList
                entries{
                    ... mediaListEntry
                }
            }
        }
    }

    fragment mediaListEntry on MediaList{
        mediaId
        status
        progress
        repeat
        notes
        startedAt{
            year
            month
            day
        }
        media{
            episodes
            duration
            nextAiringEpisode{episode}
            format
            title{romaji native english}
            tags{name}
            genres
            meanScore
            studios{nodes{isAnimationStudio id name}}
        }
        scoreRaw: score(format: POINT_100)
        '''
        variables = {
            'username': username,
            'type': medium,
            'status': status
        }

        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})
        
        self.raw = json.loads(response.text)["data"]["MediaListCollection"]["lists"][0]["entries"]       

class MediaList:
    def __init__(self, username, medium, status):
        query = '''
    query ($username: String, $type: MediaType, $status: MediaListStatus) {
        MediaListCollection(userName: $username, type: $type, status: $status) {
            lists {
                entries {
                    media {
                        id
                        started
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
        
        return _id_list
    
    def start_list(self):
        _start_list = []
        for i in range(0, len(self.raw)):
            _start_list.append(self.raw[i]["id"]["startedAt"])
        
        return _start_list
    

def main():
    m = MediaList("jreeee", "ANIME", "COMPLETED")
    t = m.title_list("romaji")
    i = m.id_list()
    num = 32
    s = m.start_list()
    print(str(i[num]) + " " + t[num])
    print(s[num])

if __name__ == "__main__":
    main()