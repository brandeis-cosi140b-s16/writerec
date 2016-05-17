# -*- coding: utf-8 -*-
"""
Created on Mon May 16 19:01:32 2016

@author: clay
"""

import os, random, xml

PATH = '/media/clay/SHARED/acad/brandeis/2015_2016-spring/NLAML/writerec_corpus/annotations/gold_standard/'

# define the desired clusters
k = 5
ann_clusters = [3, 3, 4, 2, 2, 3, 4, 4, 1, 2, 2, 2, 3, 0, 4, 2, 4, 1, 0, 2, 2, 1, 2, 0, 0, 1, 2, 0, 2, 1, 2, 4, 2, 2, 2, 0, 4, 4, 1, 4, 4, 1, 3, 3, 1, 4, 4, 4, 2, 2, 4, 3, 3, 4, 3, 0, 2, 2, 2, 4, 2, 0, 3, 4, 1, 2, 2, 0, 1, 3, 2, 4, 4, 1, 2, 2, 2, 3, 1, 1, 2, 1, 1, 3, 4, 1, 3, 0, 4, 0, 4, 1, 2, 4, 1, 2, 1, 4, 0, 0, 1, 4, 2, 4, 2, 3, 4, 1, 1, 1, 1, 4, 4, 1, 1, 2, 3, 0, 1, 2, 4, 1, 1, 4, 1, 4, 1, 1, 0, 1, 1, 2, 2, 1, 1, 0]
bow_clusters = [3, 2, 0, 4, 4, 0, 4, 0, 0, 3, 2, 3, 3, 0, 4, 4, 4, 3, 2, 0, 4, 3, 4, 3, 2, 3, 0, 2, 0, 2, 0, 0, 4, 0, 0, 2, 4, 4, 2, 0, 4, 4, 4, 4, 2, 2, 0, 0, 4, 4, 3, 0, 4, 2, 3, 1, 0, 0, 0, 3, 4, 0, 4, 4, 0, 2, 2, 4, 0, 0, 0, 1, 0, 0, 4, 1, 1, 4, 4, 0, 4, 2, 0, 4, 3, 4, 4, 4, 2, 0, 0, 0, 3, 2, 4, 4, 4, 4, 0, 2, 0, 0, 4, 2, 4, 3, 0, 4, 4, 2, 1, 4, 4, 3, 3, 2, 4, 2, 4, 4, 3, 3, 0, 4, 1, 2, 4, 0, 0, 0, 4, 4, 4, 4, 4, 2]
ann = {}
bow = {}
for i in range(k):
    ann[i] = set()
    bow[i] = set()
for i in range(len(ann_clusters)):
    ann[ann_clusters[i]].update([i])
    if len(ann_clusters) != len(bow_clusters):
        print ('WARNING:\nMake sure the ann_clusters and bow_clusters lists are the same length!')
    else:
        bow[bow_clusters[i]].update([i])
    
TEXTS = []
i=0
for f in sorted(os.listdir(PATH)):
    with open(os.path.join(PATH, f),'r') as a:
        et = xml.etree.ElementTree.ElementTree().parse(a)
        t = et[0].text
        TEXTS.append(t)
        
def get_like(text, b=False):
    ''' returns a random text in the given text's cluster, given an index '''
    if bow:    
        c = bow_clusters[text]
        cs = bow
    else:
        c = ann_clusters[text]
        cs = ann
    done = False
    while not done:
        pick = random.sample(cs[c],1)[0]
        if pick != text:
            done = True
    print( TEXTS[pick] )
    
def get_unlike(text, b=False):
    if bow:
        c = bow_clusters[text]
        cs = bow
    else:
        c = ann_clusters[text]
        cs = ann
    done = False
    while not done:
        finished = False
        while not finished:
            othercluster = random.sample(xrange(5),1)[0]
            if othercluster != c:
                finished = True
        pick = random.sample(cs[othercluster],1)[0]
        if pick != text:
            done = True
    print( TEXTS[pick] )
    
def rand():
    return random.sample(xrange(len(ann_clusters)),1)[0]
    
def get_all(r=None):
    if r == None:
        r = rand()
    print(r)
    print('1.\n'+TEXTS[r])
    print('\n2.')
    get_unlike(r)
    print('\n3.')
    get_like(r)
    print('\n4.')
    get_unlike(r,b=True)
    print('\n5.')
    get_like(r,b=True)