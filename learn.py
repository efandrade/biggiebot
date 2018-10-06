#!/usr/bin/env python3

import vanilla_rnn as vrnn
import numpy as np
from IPython.display import clear_output

def train_rnn(lyrics, charVec, char_dict, ind_dict, num_uniq_chars, num_chars, sequence_length, hidden_layer_size=10, learning_rate=1e-1, loss_goal=1, printiteration=3000):

    W,U,V,sbias,ybias = vrnn.initmat(hidden_layer_size,num_uniq_chars)

    mW = np.zeros(W.shape)
    mU = np.zeros(U.shape)
    mV = np.zeros(V.shape)
    msbias = np.zeros(sbias.shape)
    mybias = np.zeros(ybias.shape)

    loss_track = []
    loss = loss_goal + 1

    n = 0
    p = 0
    iteration= 0

    while loss > loss_goal:
   
        if p+sequence_length+1 >= num_chars or n == 0:
            init_h = np.zeros([hidden_layer_size,1])
            p = 0
            inputs = [char_dict[i] for i in lyrics[p:p+sequence_length]]
            targets = [char_dict[i] for i in lyrics[p+1:p+sequence_length+1]]

        loss, dU, dW, dV, dsbias, dybias, init_h = vrnn.CostFun(inputs, targets, init_h, hidden_layer_size,charVec,W,U,sbias,V,ybias)
        loss_track.append(loss)
    
        if n % printiteration == 0:
            clear_output()
            sample_ix = vrnn.prediction(init_h, inputs[0], num_uniq_chars, 100, W, U, sbias, V, ybias, random=True)
            print(vrnn.pred2str(sample_ix, ind_dict,space=True))
            print('=============================')
        if n % printiteration == 0:
            iteration = n
            print( 'Iteration %d, loss %f\n' % (n,loss))
            printProgressBar(0, printiteration, prefix = 'Next ' + str(printiteration) + 'th Iteration', length = 35)
        if n % 1000 == 0:
            printProgressBar(n-iteration, printiteration, prefix = 'Next ' + str(printiteration) + 'th Iteration', length = 35)
    
        for param, dparam, mem in zip([U, W, V, sbias, ybias], [dU, dW, dV, dsbias, dybias], [mU, mW, mV, msbias, mybias]):
            mem += dparam * dparam
            param += -learning_rate * dparam / np.sqrt(mem + 1e-8)
            
        p = p + sequence_length
        n = n + 1

# Print iterations progress        
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()