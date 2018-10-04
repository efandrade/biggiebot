# biggiebot

While initially I wanted to create a natural language processing algorithm to learn and mimic the lyrical style of The Notorious B.I.G (also known as Biggie hence the project name), in principle the algorithms should be able to learn and mimic an artist with a enough songs to data mind and compare to.

First I’ll code and use a vanilla recurrent neural network (VRNN) with 1 hidden layer. Using this VRNN, I’ll train this algorithms using lyrics from different songs both by vectorizing the lyrics by characters, by words, and by syllables. Then I plan to code a long term short term memory recurrent neural network (LTSM) and again train the algorithm using the same vectorization methods as previously mentioned.
