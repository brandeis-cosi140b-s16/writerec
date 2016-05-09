# -*- coding: utf-8 -*-
"""
Created on Mon May  9 01:46:21 2016

@author: Clay Riley

A script for embedding local features of an attributed graph into vector space,
following J. G. Domingo 2012, "Vector Space Embedding of Graphs via Statistics 
of Labelling Information."

Special thanks to Noa Naaman for guidance.
"""


# modules needed:
import os, sys
from xml.etree.ElementTree import ElementTree
from collections import Counter


# extract features from a file
def extract(path):
    '''
    Given path to an xml file, extract and return its features as a vector.
    '''
    counts = Counter() # initialize counter for features
    with open(path,'r') as f: # open and close file within this method call
        doc = ElementTree().parse(f) # store this document as a parsed xml element tree
        #
        #
        #
        text = doc[0]
        for i in len(doc[1]):
            tag_type = x[1][i].tag # tag type
            atts = doc[1][i].items() # attributes of this tag
            


# run script from terminal
if __name__ == '__main__':
    PATH = sys.argv[1] # give the corpus directory in command-line input
    for FILENAME in os.listdir(PATH):
        if FILENAME[-4:].lower() == '.xml':
            extract(os.path.join(PATH,FILENAME))