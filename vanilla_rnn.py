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
def lossFun(inputs, targets, init_h, hidden_layer_size, charVec, Whh, Wxh, bh, Why, by):

    W = Whh
    U = Wxh
    sbias = bh
    V = Why
    ybias = by
    
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