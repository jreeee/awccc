#!/usr/bin/env python3

## A lot of code originates from https://github.com/jakobbbb/anipresence which does something quite different, 
# but I'll use it as a starting point to hopefully get the hang of it

import os
import re
import requests
import json


class MetaDataCache:
    cache = {}
    cache_path = None

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.cache = {}
        cache_dir = os.path.dirname(self.cache_path)
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r") as f:
                self.cache = json.loads(f.read())
        else:
            self._write_cache()

    def _write_cache(self):
        with open(self.cache_path, "w+") as f:
            f.write(json.dumps(self.cache, indent=4))

    def get_id_info(self, id) -> str:
        key = f"{id}"

        if key not in self.cache.keys():
            self.cache[key] = self._get_id_info(
                id
            )
            self._write_cache()

        return self.cache[key]

    def _get_id_info(self, id) -> str:

        query = """
            query($title: String) {
                media(search: $title, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                    }
                    format
                    genres
                    episodes
                }
            }
        """
        variables = {"id": id}
        url = "https://graphql.anilist.co"

        print("Requesting", variables)
        resp = requests.post(
            url, json={"query": query, "variables": variables}
        )
        print(resp.text)
        if not resp.status_code == 200:
            print("couldnt get data")
            return

class AniCheck:
    anime = None

    CACHE_PATH = os.path.expanduser("~/.cache/awccc/info.json")
    cache: MetaDataCache

    def __init__(self, client_id):
        self.cache = MetaDataCache(self.CACHE_PATH)

    def get_anime(self):
        return None, None


    def update(self):
        anime_new = self.get_anime()
        print(anime_new)

        if anime_new is None:
            return False

        if self.anime == anime_new:
            return True

        self.anime = anime_new

        title, ep, epcount = self.anime

        return True

    def try_update(self):
        try:
            print("Updating")
            return self.update()
        except Exception as e:
            print(e)
            return True

    def try_get_info(id) -> str:
        try:
            return self.cache.get_id_info(id)
        except Exception as e:
            print(e)
            return


def main():
    client_id = "placeholder"
    try:
        if a := AniCheck(client_id):
            a.loop()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()