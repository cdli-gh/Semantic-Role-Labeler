#Usage : python make_word_vectors.py INPUT_FILE OUTPUT_MODEL_DIR

import gensim
import os, sys, codecs

INPUT_FILE = sys.argv[1]
OUTPUT_DIR = sys.argv[2]

# Create a Sentences iterator over the file
class MySentences(object):
    def __init__(self, filename):
        self.filename = filename
 
    def __iter__(self):
    	with codecs.open(self.filename, 'r') as f:
            for line in f:
                yield line.strip().split()
 

# Call the sentences iterator
'''
sentences = []
with codecs.open(INPUT_FILE, 'r', encoding='utf-8') as f:
	for line in f:
		sentences.append(line.strip())
'''
sentences = MySentences(INPUT_FILE) # a memory-friendly iterator, so we can generalise for huge data later even on lesser-RAM PCs.
print (sentences)

# Define the skipgram and cbow models for training word2vec
# min_count is set to 1 as the data we have is anyway less, for now.
model_skipgram = gensim.models.Word2Vec(sentences, min_count = 1, size = 100, sg = 1, window = 5)
print ("Training skipgram done...")

model_cbow = gensim.models.Word2Vec(sentences, min_count = 1, size = 100, sg = 0, window=5)
print ("Training cbow done...")


#Save the models to disk
if OUTPUT_DIR[-1] == '/':
	OUTPUT_DIR=OUTPUT_DIR[:-1]

model_skipgram.wv.save_word2vec_format(OUTPUT_DIR+'/skipgram_w5_100.txt', binary=False)
model_cbow.wv.save_word2vec_format(OUTPUT_DIR+'/cbow_w5_100.txt', binary=False)

#model_skipgram.save(OUTPUT_DIR+'/skipgram_w5_100')
#model_cbow.save(OUTPUT_DIR+'/cbow_w5_100')

new_model = gensim.models.KeyedVectors.load_word2vec_format('./skipgram_w5_100.txt')
print (new_model['lugal'])



