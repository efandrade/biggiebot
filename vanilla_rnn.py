#/usr/bin/env python

#Generates sequence from an initial input seed using the provided model and
#   length

import numpy as np

#Generates a sequence using the output of the train algorithm
def prediction(h, seed, dim, length, Whh, Wxh, bh, Why, by):
    #h:         Previous hidden state
    #seed:      Initial input to begin squence
    #dim:       Number of features
    #length:    Lenght of sequence to be generated
    
    x = np.zeros([dim,1])
    x[seed,0] = 1
    predic = []
    WhhWxh = np.concatenate((Whh,Wxh),axis=1)
    for i in range(length):
        hx = np.concatenate((h,x),axis=0)
        h = np.tanh(np.dot(WhhWxh,hx) + bh)
        y = np.dot(Why,h) + by
        p = np.exp(y)/np.sum(np.exp(y))
        ix = np.random.choice(range(dim),p=p.ravel())
        x = np.zeros([dim,1])
        x[ix] = 1
        predic.append(ix)
    return predic
    
def pred2str(predic,ind_dict):
    txt = ''.join(ind_dict[ix] for ix in predic)
    return txt

#Calculates the 
def lossFun_old(inputs, targets, init_h, hidden_layer_size, charVec, Whh, Wxh, bh, Why, by):

    ###forward propagation###
    
    #number of inputs
    input_length = len(inputs)
    xs = charVec[inputs].T                              
    #create hidden layer x number of inputs matrix
    hs = np.zeros([hidden_layer_size,input_length])
    #add initial hidden layer to the end of hs matrix for coveience in the for
    #loop below
    hs[:,-1] = init_h[:,0]
    loss = 0
    
    WhhWxhbh = np.concatenate((Whh,Wxh,bh),axis=1)
    for i in range(0,len(inputs)):
        hx1 = np.concatenate((hs[:,i-1],xs[:,i],np.ones(1)),axis=0)
        hs[:,i] = np.tanh(np.dot(WhhWxhbh,hx1))
        
    ys = np.dot(Why,hs) + np.tile(by,input_length)
    ps = np.exp(ys) / np.sum(np.exp(ys),axis=0)
    loss += np.sum(-np.log(ps[targets,range(input_length)]))
    
    y = np.expand_dims(hs[:,-1],axis=1)
    
#back propagation
    dWxh = np.zeros(Wxh.shape)
    dWhh = np.zeros(Whh.shape)
    dWhy = np.zeros(Why.shape)
    
    dbh = np.zeros(bh.shape)
    dby = np.zeros(by.shape)
    dhnext = np.expand_dims(np.zeros(hs[:,0].shape),axis=1)
    
    dy = np.copy(ps) - charVec[targets].T
    dWhy += np.dot(dy,hs.T)
    dby = np.sum(dy,axis=1)[:,np.newaxis]
    hs[:,-1] = init_h[:,0]
    
    for i in range(len(inputs))[::-1]:
        dh = np.dot(Why.T, dy[:,i][:,np.newaxis]) + dhnext
        dhraw = (1 - np.expand_dims(hs[:,i] * hs[:,i],axis=1)) * dh
        dbh += dhraw
        dWxh += np.dot(dhraw, xs[:,i][:,np.newaxis].T)
        dWhh += np.dot(dhraw, hs[:,i-1][:,np.newaxis].T)
        dhnext = np.dot(Whh.T, dhraw)

    for dparam in [dWxh,dWhh,dWhy,dbh,dby]:
        np.clip(dparam,-5,5,out=dparam)

    return loss, dWxh, dWhh, dWhy, dbh, dby, y

def lossFun(inputs, targets, init_h, hidden_layer_size, charVec, Whh, Wxh, bh, Why, by):

    #x = inputs
    outputs = targets
    s_m1 = init_h
    
    
    W = Whh
    U = Wxh
    sbias = bh
    V = Why
    ybias = by
    
    ###forward propagation###
    
    #number of inputs
    sequence_length = len(inputs)
    
    #vectorized inputs
    x = charVec[inputs].T
    #create state matrix
    s_t = np.zeros([hidden_layer_size,sequence_length])
    #add initial state to the end of hs matrix for coveience in the for loop below
    s_t[:,-1] = s_m1[:,0]
    loss = 0
    
    #calculates all the states (s_t) in the rnn
    for i in range(sequence_length):
        #s_t is calculated with previous state s_t-1 and current input x_t
        s_t[:,i] = np.tanh( np.dot(W,s_t[:,i-1]) + np.dot(U,x[:,i]) + sbias )
    
    #calculate unnormalized probability outputs y for each state s_t
    y = np.dot(V,s_t) + np.tile(ybias,sequence_length)
    #normalize probabilities y
    p = np.exp(y) / np.sum(np.exp(y),axis=0)
    #Cost function
    loss += np.sum(-np.log(p[targets,range(sequence_length)]))
    
    next_s_tm1 = np.expand_dims(s_t[:,-1],axis=1)
    
#back propagation
    dU = np.zeros(U.shape)
    dW = np.zeros(W.shape)
    dV = np.zeros(V.shape)
    
    dsbias = np.zeros(sbias.shape)
    #dybias = np.zeros(ybias.shape)
    dhnext = np.expand_dims(np.zeros(s_t[:,0].shape),axis=1)
    
    dy = np.copy(p) - charVec[targets].T
    dV += np.dot(dy,s_t.T)
    dybias = np.sum(dy,axis=1)[:,np.newaxis]
    #hs[:,-1] = init_h[:,0]
    
    for i in range(sequence_length)[::-1]:
        dsbias = np.dot(V.T, dy[:,i][:,np.newaxis]) + dhnext
        dhraw = (1 - np.expand_dims(s_t[:,i] * s_t[:,i],axis=1)) * dsbias
        dsbias += dhraw
        dU += np.dot(dhraw, x[:,i][:,np.newaxis].T)
        dW += np.dot(dhraw, s_t[:,i-1][:,np.newaxis].T)
        dhnext = np.dot(W.T, dhraw)

    for dparam in [dU,dW,dV,dsbias,dybias]:
        np.clip(dparam,-5,5,out=dparam)

    return loss, dU, dW, dV, dsbias, dybias, next_s_tm1

