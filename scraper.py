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
    
def artistlyrics(filename,song=0):

    jsonfile = open(filename,'r').read()
    database = json.loads(jsonfile)
    artist = database['artist']
    lyrics = database['songs'][song]['lyrics']
    
    length = len(lyrics)
    sections = []
    x1, x2 = 0, 0
    pos = 0
    end = len(lyrics)
    
    while x1 != -1:
    x1 = lyrics.find('[',pos)
    x2 = lyrics.find(']',pos)
    if x1 != -1:
        sections.append([lyrics[x1:x2+1],x1,x2])