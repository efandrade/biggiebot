#!/usr/bin/env python3

import numpy as np

#Opens and reads text, returns character dictionaries for text file
def bychar(filename):
    #filename:  Name of the text file to open
    
    lyrics = open(filename,'r').read()                          #read text file
    chars = list(set(lyrics))                                   #lists charachters in text file
    char_dict = {char:ind for ind,char in enumerate(chars)}     #create a dictionary for converting characters to corresponding numbers (index)
    ind_dict = {ind:char for ind,char in enumerate(chars)}      #create a dictionary for converting numbers (index) to corresponding characters
    num_uniq_chars = len(chars)                                 #number of unique characters in text file
    num_chars = len(lyrics)                                     #number of total characters in text file
    charmat = np.identity(num_uniq_chars)                       #Matrix where the columns correspont to the vectors representation of the each entry (characters) in the dictionary
    
    return lyrics, charmat, char_dict, ind_dict, num_uniq_chars, num_chars

#Opens and reads text, returns word dictionaries for text file
def byword(filename):
    #filename:  Name of the text file to open
    
    lyrics = open(filename,'r').read()                          #read text file
    lyrics = lyrics.split()                                     #creates array of words
    words = list(set(lyrics))                                   #lists words in text file
    word_dict = {word:ind for ind,word in enumerate(words)}     #create a dictionary for converting words to corresponding number (index)
    ind_dict = {ind:word for ind,word in enumerate(words)}      #create a dictionary for converting numbers (index) to corresponding characters
    num_uniq_words = len(words)                                 #number of unique words in text file
    num_words = len(lyrics)                        #number of total words in text file
    wordmat = np.identity(num_uniq_words)                       #Matrix where the columns correspont to the vectors representation of the each entry (words) in the dictionary
    
    return lyrics, wordmat, word_dict, ind_dict, num_uniq_words, num_words