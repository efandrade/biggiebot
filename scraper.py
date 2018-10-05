#!/usr/bin/env python3

import json
import lyricsgenius as genius

#Searches and retrives lyrics from genius.com of a particular artist and saves them as a json file
def getlyrics(tokenloc,artistname,songnames=None):
    #tokenloc:      The location of a textfile containing your API clien token for genius.com
    #artistname:    The name of the artist you want lyrics from 
    #songnames:     Th name of the songs of the artist you want lyrics from (retrives a default of 3 songs)
    
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
    return 'Lyrics_' +  ''.join(artist.name.split()) + '.json'

#Opens json and returns only verses pertaining to the artist
def artistlyrics(filename,numsongs=None,alias=None):
    #filename:      Location of json file
    #numsongs:      Specify if you want to return verse of a particular song, does all the songs by default

    jsonfile = open(filename,'r').read()
    database = json.loads(jsonfile)
    artist = [database['artist']]
    
    if alias !=None:
        artist = artist + alias
        
    if numsongs == None:
        numsongs = len(database['songs'])
    else:
        numsongs += 1
    
    artistlyrics = []
    
    for song in range(numsongs):
        lyrics = database['songs'][song]['lyrics']
        featartist = database['songs'][song]['raw']['featured_artists']
        sections = []
        x1, x2 = 0, 0
        pos = 0
        artistsonglyrics = []
    
        while x1 != -1:
            x1 = lyrics.find('[',pos)
            x2 = lyrics.find(']',pos)
            if x1 != -1:
                sections.append([lyrics[x1:x2+1],x1,x2])
                pos = x2 + 2

        for i in range(len(sections)):
            t = 0
            for j in range(len(artist)):
                t += (sections[i][0].lower()[1:-1] == artist[j].lower())

            start = sections[i][2]+2
            if i == len(sections)-1:
                end = len(lyrics)
            else:
                end = sections[i+1][1]

            if (sections[i][0].lower().find('verse') != -1):
                if featartist != []:
                    t=0
                    for j in range(len(artist)):
                        t += (sections[i][0].lower().find(artist[j].lower())==-1)
                    if t > 0:
                        artistsonglyrics.append(lyrics[start:end])
                else:
                        artistsonglyrics.append(lyrics[start:end])
            elif t > 0:
                artistsonglyrics.append(lyrics[start:end])
                
        artistlyrics.append(''.join(artistsonglyrics))
    
    newfilename = database['artist'] + ' lyrics.txt'
    savefile = open(newfilename,'w')
    print(''.join(artistlyrics),file=savefile)
    savefile.close()
    
    return(newfilename)