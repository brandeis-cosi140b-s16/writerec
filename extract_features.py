# -*- coding: utf-8 -*-
"""
Created on Mon May  9 01:46:21 2016

@author: Clay Riley
"""

# modules needed:
import os, sys
from xml.etree.ElementTree import ElementTree as et

# extract features from a file
def extract():
    '''
    Given path to an xml file, extract and return its features.
    '''
    pass

# run script from terminal
if __name__ == '__main__':
    PATH = sys.argv[1] # give the corpus directory in command-line input
    for FILENAME in os.listdir(PATH):
        if FILENAME[-4:].lower() == '.xml':
            extract(os.path.join(PATH,FILENAME))