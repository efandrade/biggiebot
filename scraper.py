#!/usr/bin/env python3

import json
import lyricsgenius as genius

def getlyrics(artistname,songnames=None,tokenloc):
    
    api_token = open(tokenloc,'r').read()

    api_token = '9LwgN2hR6Cb7BAFikCIoKPixM7rfBUIT4M8iwAc3mAOAl7QhdN2obGwcl7Galy3_'
    api = genius.Genius(api_token)
    
    if songnames:
        artist = api.search_artist(artistname,max_songs=0)
        
        for i in range(len(songnames)):
            song = api.search_song(songnames[i],artist.name)
            artist.add_song(song)
    else:
        artist = api.search_artist(artistname,max_songs=3)
        
    artist.save_lyrics()
    