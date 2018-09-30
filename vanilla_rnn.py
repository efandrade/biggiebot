#/usr/bin/env python

import numpy as np

#Generates a sequence using the output of the train algorithm
def prediction(s_tm1, seed, dim, length, W, U, sbias, V, ybias,random=True):
    #s_tm1:     Previous state
    #seed:      Initial input to begin squence
    #dim:       Dimension of vector space (number of features)
    #length:    Length of sequence to be generated
    #W:         Matrix of coefficients that transforms the previous state (s_t-1) into the current state (s_t)
    #U:         Matrix of coefficients that transforms the current input (x_t) into the current state (s_t)
    #sbias:     Biasies for calculating the current state (s_t)
    #V:         Matrix of coefficients that transforms the current state (s_t) into the predicted output (y_t)
    #ybias:     Biasies for the calculating the predicted output (y_t)
       
    s_t = s_tm1                                                 #Initial previous state
    x = np.zeros([dim,1])   
    x[seed,0] = 1                                               #Seed vector
    predict = []
        
    #start with seed, predicts next vector, then uses that predicted vector as the next 'seed' until sequence length is generated
    for i in range(length):
        s_t = np.tanh( np.dot(W,s_t) + np.dot(U,x) + sbias)     #current state calculation
        y = np.dot(V,s_t) + ybias                               #unnormalized probabilities for predicted output
        p = np.exp(y)/np.sum(np.exp(y))                         #normalized probabilities for predicted output (sofmax)
        if random == True:
            ix = np.random.choice(range(dim),p=p.ravel())       #randomly predicts output with given nomalized probabilities
        else:
            ix = np.argmax(p)                                   #predicts output solely on the highest probability
        x = np.zeros([dim,1])
        x[ix] = 1                                               #new seed vector for next prediction
        predict.append(ix)                                      #sequence
    
    return predict

#Coverts sequence of numbers to the corresponding characters
def pred2str(predict,ind_dict,space=False):
    #predict:       Sequence of numbers
    #ind_dict:      Corresponding numbers to characters
    
    if space == False:
        txt = ''.join(ind_dict[ix] for ix in predict)                #coverts sequence of numbers to the corresponding characters
    else:
        txt = ''.join([ind_dict[ix] + ' '][0] for ix in predict)     #coverts sequence of numbers to the corresponding characters with spaces inbetween
        
    return txt

def CostFun(inputs, targets, s_m1, hidden_layer_size, charVec, W, U, sbias, V, ybias):
    #inputs:            Previous state
    #targets:           Initial input to begin squence
    #s_m1:              Dimension of vector space (number of features)
    #hidden_layer_size: Length of sequence to be generated
    #charVec:           Matrix where the columns correspont to the vectors representation of the each entry in the "dictionary" (letters, word, etc)
    #W:                 Matrix of coefficients that transforms the previous state (s_t-1) into the current state (s_t)
    #U:                 Matrix of coefficients that transforms the current input (x_t) into the current state (s_t)
    #sbias:             Biasies for calculating the current state (s_t)
    #V:                 Matrix of coefficients that transforms the current state (s_t) into the predicted output (y_t)
    #ybias:             Biasies for the calculating the predicted output (y_t)
    
    
    
    #Forward Propagation
    sequence_length = len(inputs)                               #number of inputs
    x = charVec[inputs].T                                       #vectorized inputs
    s_t = np.zeros([hidden_layer_size,sequence_length])         #create state matrix
    s_t[:,-1] = s_m1[:,0]                                       #add initial state to the end of hs matrix for coveience in the for loop below
    loss = 0
    
    #calculates all the states (s_t) in the rnn
    for i in range(sequence_length):
        s_t[:,i] = np.tanh( np.dot(W,s_t[:,i-1]) + np.dot(U,x[:,i]) + np.squeeze(sbias))    #s_t is calculated with previous state s_t-1 and current input x_t
    
    y = np.dot(V,s_t) + np.tile(ybias,sequence_length)          #calculate unnormalized probability outputs y for each state s_t
    p = np.exp(y) / np.sum(np.exp(y),axis=0)                    #normalize probabilities y
    loss += np.sum(-np.log(p[targets,range(sequence_length)]))  #Cost function
    next_s_m1 = np.expand_dims(s_t[:,-1],axis=1)                #current state which will be the initial state for the next iteration
    
    #Backpropagation
    dU = np.zeros(U.shape)
    dW = np.zeros(W.shape)
    dV = np.zeros(V.shape)
    
    dsbias = np.zeros(sbias.shape)
    dhnext = np.expand_dims(np.zeros(s_t[:,0].shape),axis=1)
    
    #Backpropagation into current state through softmax
    dy = np.copy(p) - charVec[targets].T                        #error in predicted output
    dV += np.dot(dy,s_t.T)                                      #rate of change in cost function with respect to V (dL/dV) for softmax
    dybias = np.sum(dy,axis=1)[:,np.newaxis]                    #rate of change in cost function with respect to bias coefficients (dL/dybias) for softmax
    
    #Backpropagation into previous states
    for i in range(sequence_length)[::-1]:
        dsbias = np.dot(V.T, dy[:,i][:,np.newaxis]) + dhnext
        dhraw = (1 - np.expand_dims(s_t[:,i] * s_t[:,i],axis=1)) * dsbias
        dsbias += dhraw
        dU += np.dot(dhraw, x[:,i][:,np.newaxis].T)
        dW += np.dot(dhraw, s_t[:,i-1][:,np.newaxis].T)
        dhnext = np.dot(W.T, dhraw)

    for dparam in [dU,dW,dV,dsbias,dybias]:
        np.clip(dparam,-5,5,out=dparam)

    return loss, dU, dW, dV, dsbias, dybias, next_s_m1

