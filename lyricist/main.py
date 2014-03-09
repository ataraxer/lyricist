#!/usr/bin/env python

import sys

import requests
from HTMLParser import HTMLParser


API_KEY  = 'a4f0745b66edb795cab22c4f0911ff'
API_HOST = 'http://api.lyricsnmusic.com/songs'


class SongHTMLParser(HTMLParser):
    def __init__(self):
        self.song = None
        self.start = False
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.start = True

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.start = False

    def handle_data(self, data):
        if self.start:
            self.song = data


def list_songs(artist):
    params = {
        'api_key': API_KEY,
        'artist': artist,
    }

    req = requests.get(API_HOST, params=params)
    return req.json()


def parse_song(html):
    parser = SongHTMLParser()
    parser.feed(html)
    return parser.song


def get_song(url):
    req = requests.get(url)
    html_content = req.text
    return parse_song(html_content)


def main(artist):
    song_list = list_songs(artist)

    available, not_available = {}, []

    for song_info in song_list:
        viewable, title, url = map(
                song_info.get, ['viewable', 'title', 'url'])
        if viewable:
            available[title] = get_song(url)
        else:
            not_available.append(title)

    for song_name, song_text in available.items():
        f = open(song_name.lower().replace(' ', '-') + '.txt', 'w')
        f.write(song_text.encode('utf8'))
        f.close()


if __name__ == '__main__':
    artist = sys.argv[1]
    main(artist)

