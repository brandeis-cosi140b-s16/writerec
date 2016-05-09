# -*- coding: utf-8 -*-
"""
Created on Mon May  9 19:09:49 2016

@author: Clay Riley

A script for creating a k-Means Clusterer using unary word featuresin a document.

Special thanks to Keigh Rim for guidance.

"""

import numpy, nltk
from xml.etree.ElementTree import ElementTree


# initialize vocabulary
VOCAB = set()

# get vocabulary
def get_V(path):
    with open(path,'r') as f:
        et = ElementTree().parse(f)
        VOCAB.update([word for word in nltk.tokenize.word_tokenize(et[0].text)])

feature_vectors = []   # a |documents| X |features| matrix
    
def bow_vector_binarized(path):
    v = numpy.zeros(len(feature_indices)) # initialize document vector
    with open(path,'r') as f:
        et = ElementTree().parse(f)
        for w_type in set(nltk.tokenize.word_tokenize(et[0].text)):
            v[feature_indices.index(w_type)] = 1
    return v                     
                                      
PATH = '/media/clay/SHARED/acad/brandeis/2015_2016-spring/NLAML/writerec_corpus/annotations/gold_standard/'
for f in sorted(os.listdir(PATH)):
    if f[-4:].lower() == '.xml':
        get_V(os.path.join(PATH,f))
feature_indices = sorted(list(VOCAB)) # indexed feature names
for f in sorted(os.listdir(PATH)):
    if f[-4:].lower() == '.xml':
        v = bow_vector_binarized(os.path.join(PATH,f))
        feature_vectors.append(v)

# clusterer
#
# number of clusters
k = 5
# number of times to repeat the algorithm; 
# the most common assignment per document out of this number of runs is kept
tries = 20
# creates the clustering architecture
kmc = nltk.cluster.kmeans.KMeansClusterer(k, nltk.cluster.cosine_distance, repeats=tries)
# assigns each document to one of k clusters
clustered = kmc.cluster(feature_vectors,True)
# pseudo-classifier:
classify_this = '/media/clay/SHARED/acad/brandeis/2015_2016-spring/NLAML/writerec_corpus/annotations/gold_standard/American_Gods-goldstandard.xml'
kmc.classify(numpy.array(bow_vector_binarized(classify_this)))
