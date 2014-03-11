#!/usr/bin/env python

import sys, re
from time import sleep

import requests
from HTMLParser import HTMLParser

HOST = 'http://www.azlyrics.com'


class ListHTMLParser(HTMLParser):
    def __init__(self, band):
        self.songs = []
        self.band  = band
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'href' in attrs:
            href = attrs['href']
            song_ref_prefix = '../lyrics/{}/'.format(self.band)
            if href.startswith(song_ref_prefix):
                self.songs.append(href.replace(song_ref_prefix, ''))


class SongHTMLParser(HTMLParser):
    def __init__(self):
        self.song = ''
        self.start = False
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_comment(self, raw):
        data = raw.lstrip()
        if data.rstrip() == 'start of lyrics':
            self.start = True
        if data.rstrip() == 'end of lyrics':
            self.start = False

    def handle_data(self, data):
        if self.start:
            self.song += data.encode('utf8')


def list_songs(band):
    req = requests.get('{}/{}/{}.html'.format(HOST, band[0], band))
    html_content = req.text
    parser = ListHTMLParser(band)
    parser.feed(html_content)
    for song in parser.songs:
        parse_song(band, song)
        sleep(5)


def parse_song(band, song):
    req = requests.get('{}/lyrics/{}/{}'.format(HOST, band, song))
    html_content = req.text
    f = open(song.replace(' ', '-'), 'w')
    f.write(html_content.encode('utf8'))
    f.close()
    parser = SongHTMLParser()
    parser.feed(html_content)
    f = open(song.lower().replace(' ', '-').replace('.html', '.txt'), 'w')
    f.write(parser.song)
    f.close()


def main(band):
    list_songs(band)


if __name__ == '__main__':
    raw_band = sys.argv[1]
    band = re.sub('^the ', '', raw_band.lower()).replace(' ', '')
    main(band)

