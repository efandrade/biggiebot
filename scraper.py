#!/usr/bin/env python3

import json
import lyricsgenius as genius

#Searches and retrives lyrics from genius.com of a particular artist and saves them as a json file
def getlyrics(tokenloc,artistname,songnames=None):
    #tokenloc:      The location of a textfile containing your API clien token for genius.com
    #artistname:    The name of the artist you want lyrics from 
    #songnames:     Th name of the songs of the artist you want lyrics from (retrives a default of 3 songs)
    
    api_token = open(tokenloc,'r').read()                       #Loads client API token for genius.com from text file
    api = genius.Genius(api_token[0:-1])
        
    #Create artist object and populated with specified or unspecified songs and add it to artist object
    if songnames:
        artist = api.search_artist(artistname,max_songs=0)      #create artist onject
        
        for i in range(len(songnames)):
            song = api.search_song(songnames[i],artist.name)
            artist.add_song(song)
    else:
        artist = api.search_artist(artistname,max_songs=3)
    
    artist.save_lyrics()                                        #great json file of the artist object with all the lyrics and metadata    
    return 'Lyrics_' +  ''.join(artist.name.split()) + '.json'  #returns json file name

#Opens json and returns only verses pertaining to the artist
def artistlyrics(filename,numsongs=None,alias=None):
    #filename:      Location of json file
    #numsongs:      Specify if you want to return verse of a particular song, does all the songs by default
    #alias:         Other names the artist goes by

    jsonfile = open(filename,'r').read()                        #open and read json file
    database = json.loads(jsonfile)
    artist = [database['artist']]                               #get artist name
    
    if alias !=None:
        artist = artist + alias                                 #add provided aliases for artist
     
    #goes through all the songs in json file or specified song in numsongs
    if numsongs == None:
        numsongs = range(len(database['songs']))
    else:
        numsongs += 1
    
    artistlyrics = []
    
    #Cycles through all the songs
    for song in numsongs:
        lyrics = database['songs'][song]['lyrics']
        featartist = database['songs'][song]['raw']['featured_artists']
        sections = []
        x1, x2 = 0, 0
        pos = 0
        artistsonglyrics = []
        
        #Identifies position text in square brackets [text], the formating used by genius.com to seperate types of verses and artist in the lyrics
        while x1 != -1:
            x1 = lyrics.find('[',pos)
            x2 = lyrics.find(']',pos)
            if x1 != -1:
                sections.append([lyrics[x1:x2+1],x1,x2])
                pos = x2 + 2

        #Cycle throught the sections identified by the square brackts
        for i in range(len(sections)):
            t = 0
            #Checks to see any of the text in the brackets matches the artist name(s)
            for j in range(len(artist)):
                t += (sections[i][0].lower()[1:-1] == artist[j].lower())

            #Sets sectioin start and ending positions (i.e lyrics between text with square brackets)
            start = sections[i][2]+2
            if i == len(sections)-1:
                end = len(lyrics)
            else:
                end = sections[i+1][1]

            if (sections[i][0].lower().find('verse') != -1):                        #Checks to see if the section is labeled as a 'verse'
                if featartist != []:                                                #Checks if there are other artist listed on this song
                    t=0
                    for j in range(len(artist)):
                        t += (sections[i][0].lower().find(artist[j].lower())==-1)   #Checks to see if section is labeled with desired artist name(s)
                    if t > 0:
                        artistsonglyrics.append(lyrics[start:end])                  #If any name is found then save lyrics in that section
                else:
                        artistsonglyrics.append(lyrics[start:end])                  #If no other artist are in the song, then save lyrics in that section
            elif t > 0:
                artistsonglyrics.append(lyrics[start:end])                          #If section isn't labeled by 'verse' but it matches any or the artist names then save lyrics in that section
                
        artistlyrics.append(''.join(artistsonglyrics))                              #append all lyircs together
    
    #save to file
    newfilename = database['artist'] + ' lyrics.txt'
    savefile = open(newfilename,'w')
    print(''.join(artistlyrics),file=savefile)
    savefile.close()
    
    return(newfilename)                                                             #returns filename of saved file