#!/usr/bin/env python3

import numpy as np

#Opens and reads text, returns corresponding dictionaries for text file
def bychar(filename):
    #filename:  Name of the text file to open
    
    lyrics = open(filename,'r').read()                                          #read text file
    chars = list(set(lyrics))                                                   #lists used charachters in text file
    char_dict = {char:ind for ind,char in enumerate(chars)}                     #create a dictionary for converting character to corresponding number (index)
    ind_dict = {ind:char for ind,char in enumerate(chars)}                      #create a dictionary for converting number (index) to corresponding character
    num_uniq_chars = len(chars)                                                 #number of unique characters in text file
    num_chars = len(lyrics)                                                     #number of total characters in text file
    charmat = np.identity(num_uniq_chars)                                       #Matrix where the columns correspont to the vectors representation of the each entry (characters) in the dictionary
    
    return charmat, char_dict, ind_dict, num_uniq_chars, num_chars