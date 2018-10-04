#!/usr/bin/env python3

import json
import lyricsgenius as genius

def getlyrics(tokenloc,artistname,songnames=None):
    
    api_token = open(tokenloc,'r').read()

    api = genius.Genius(api_token[0:-1])
    
    if songnames:
        artist = api.search_artist(artistname,max_songs=0)
        
        for i in range(len(songnames)):
            song = api.search_song(songnames[i],artist.name)
            artist.add_song(song)
    else:
        artist = api.search_artist(artistname,max_songs=3)
        
    artist.save_lyrics()