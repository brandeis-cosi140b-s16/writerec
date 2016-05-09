# -*- coding: utf-8 -*-
"""
Created on Mon May  9 01:46:21 2016

@author: Clay Riley

A script for embedding local features of an attributed graph into vector space,
following J. G. Domingo 2012, "Vector Space Embedding of Graphs via Statistics 
of Labelling Information."

Special thanks to Noa Naaman for guidance.


Our DTD specifies the following possible tags and their attributes:

+ Protagonist
--- id (prefix="p")
--- subtype (underdoghero | antihero | otherhero | traitor | sidekick | mentor | other)
--- number (group | individual) 
--- spans ("###~###")
--- text 
+ Antagonist
--- id (prefix="a")
--- subtype (mainbadguy | bossbadguy | traitor | underling | other)
--- number (group | individual)
--- spans ("###~###")
--- text 
+ Unkown [sic]
--- id (prefix="U")
--- spans ("###~###")
--- text 
+ Other
--- id (prefix="otr")
--- number (group | individual)
--- spans ("###~###")
--- text 
+ Object
--- id (prefix="o")
--- number (group | individual)
--- spans ("###~###")
--- text 
+ Trigger
--- id (prefix="T")
--- subtype (romantic | familial | leadership | conflict | other)
--- spans ("###~###")
--- text 
+ Relations
--- id (prefix="R")
--- toID, toText
--- fromID, fromText
--- triggerID, triggerText
--- benefits (to | from | both | neither | unknown)
--- harms (to | from | both | neither | unknown)

"""


# modules needed:
import os, sys
from xml.etree.ElementTree import ElementTree
from collections import Counter


# variables specific to our current annotation specification
''' 
A great deal of care needs to be taken in selecting how narrowly the 
Relations will be vectorized.  All combinations of attributes of all 
combinations of the to, from, and trigger could be taken into account;
but this will produce an exponentially long and unusably sparse vector.

Alternatively, only the Relation's own attributes might be counted,
resulting in a |V_r| = 5x5=25.  Domingo 2012's approach involves counting 
local graph features to develop a sense of the graph's overall structure 
without counting every possible combination of features.

As we would like a degree of detail in our edges, the best approach is 
likely somewhere in the middle.

The current implementation counts relationships that are:

1   in the plot summary;
2   caused by antagonists, 
3   -   benefitting selves, 
4   -   benefitting others, ...
5   -   benefitting none or unable to assess, ...
6   -   harming selves;
7   -   harming others;
8   -   harming none or unable to assess;
9   caused by protagonists, ...
16  caused by others and unknowns, ...
23  caused by objects,
24  -   benefitting antagonists;
25  -   benefitting protagonists;
26  -   benefitting other character types;
27  -   benefitting none or unable to assess;
28  -   harming antagonists;
29  -   harming protagonists;
30  -   harming other character types;
31  -   harming none or unable to assess.

This set of counts will generate a less sparse vector with more local information
through overlap and double-counting, for example in a mutually beneficial 
relationship.  It is also blunt regarding complex situations caused by objects; 
instead of considering their specifics, the benefits and harms of the relationships 
are separated.  For characters this is not the case, and the more particular and 
complex relationships are recorded.  

This set also highlights the difference between self-service and mutually
beneficial relationships as well as neutral and self-harmful ones, as
opposed to paying closer attention to the particulars of who is doing 
what to whom.

This set of counts should reflect which character groups are
affected by a relationship and in what ways, along with some of the 
details of the agency of the relationship.  It doesn't capture all of
the details.  It leaves the type of relationship to the local trigger 
counts rather than incorporating them here.  Certain combinations are 
underspecified if they are not likely to be relevant--for example an 
object benefitting itself.  It emphasizes characters' actions while 
de-emphasizing things that happen to them.

The number of dimensions, 31, is much reduced from the thousands that could arise 
from capturing every detail of the edge.

Similarly, rather than getting highly specific and non-overlapping counts for 
characters, counts are collected for each of:
- the type of character or entity
- the type and number (if it has one)
- the type and subtype (if it has one)
This overlapping will enrich the vector and serve to further localize the graph
features being embedded.
'''
DIMS = [# antagonist counts
        ('a',),('a','group',),('a','individual',),
        ('a','bossbadguy'),('a','mainbadguy'),('a','other'),('a','traitor'),
        ('a','underling'),
        # object counts
        ('o',),('o','group',),('o','individual',),
        # other counts
        ('otr',),('otr','group'),('otr','individual'),
        # protagonist counts
        ('p',),('p','group',),('p','individual',),
        ('p','antihero'),('p','mentor'),('p','other'),('p','otherhero'),
        ('p','sidekick'),('p','traitor'),('p','underdoghero'),
        # trigger counts
        ('T',),('T','conflict'),('T','familial'),('T','leadership'),
        ('T','other'),('T','romantic'),
        # unknown counts
        ('U',),
        # relationship counts
        ('R',),
        ('R','a',),
        ('R','a','bs',),('R','a','bo',),('R','a','bn',),
        ('R','a','hs',),('R','a','ho',),('R','a','hn',),
        ('R','p',),
        ('R','p','bs',),('R','p','bo',),('R','p','bn',),
        ('R','p','hs',),('R','p','ho',),('R','p','hn',),
        ('R','?',),
        ('R','?','bs',),('R','?','bo',),('R','?','bn',),
        ('R','?','hs',),('R','?','ho',),('R','?','hn',),
        ('R','o',),
        ('R','o','ba',),('R','o','bp',),('R','o','b?',),('R','o','bn',),
        ('R','o','ha',),('R','o','hp',),('R','o','h?',),('R','o','hn',),
        ]



# extract features from a file
def extract(path):
    '''
    Given path to an xml file, extract and return its features as a vector.
    
    Essentially we are counting up all instances of each node or edge with a 
    particular set of attribute values in the graph of characters and 
    relationships for the given document, and returning a sparse vector space
    embedding of these counts.
    
    The size of this vector is ~70, the number of chosen combinations of tags 
    and their attributes.
    '''
    
    # initialize counter for features
    counts = Counter() 
    for dim in DIMS:
        counts[dim] = 0
        
    with open(path,'r') as f: # open and close file within this method call
        et = ElementTree().parse(f) # store this document as a parsed xml element tree
        for t in et[1]: 
            tag = t.get('id').strip('1234567890') 
            
            counts.update([(tag,)]) # count the tag type 
            
            #TODO function first, refactoring second.
            if tag == 'p':
                # update type+subtype count
                sub = t.get('subtype')
                counts.update([(tag,sub,)])
                # update type+number count
                num = t.get('number')
                counts.update([(tag,num,)])
                
            elif tag == 'a':
                # update type+subtype count
                sub = t.get('subtype')
                counts.update([(tag,sub,)])
                # update type+number count
                num = t.get('number')
                counts.update([(tag,num,)])
                
            elif tag == 'o':
                # update type+number count
                num = t.get('number')
                counts.update([(tag,num,)])
                
            elif tag == 'otr':
                # update type+number count
                num = t.get('number')
                counts.update([(tag,num,)])
                
            elif tag == 'U': # [sic]
                pass # nothing more to count
                
            elif tag == 'T':
                # update type+subtype count
                sub = t.get('subtype')
                counts.update([(tag,sub,)])
                
            elif tag == 'R':
                agent = t.get('fromID').strip('1234567890') 
                ben = t.get('benefits')
                mal = t.get('harms')
                if (agent == 'a') or (agent == 'p'):
                    counts.update([(tag,agent,)])  # update agent counts
                    # update agent+benefittee
                    if (ben == 'from') or (ben == 'both'):
                        counts.update([(tag,agent,'bs',)])
                    if (ben == 'to') or (ben == 'both'):
                        counts.update([(tag,agent,'bo',)])
                    if (ben == 'neither') or (ben == 'unknown'):
                        counts.update([(tag,agent,'bn',)])
                    # update agent+harmee 
                    if (mal == 'from') or (mal == 'both'):
                        counts.update([(tag,agent,'hs',)])
                    if (mal == 'to') or (mal == 'both'):
                        counts.update([(tag,agent,'ho',)])
                    if (mal == 'neither') or (mal == 'unknown'):
                        counts.update([(tag,agent,'hn',)])
                    
                elif (agent == 'U') or (agent == 'otr'):
                    counts.update([(tag,'?',)])  # update agent counts
                    # update agent+benefittee
                    if (ben == 'from') or (ben == 'both'):
                        counts.update([(tag,agent,'bs',)])
                    if (ben == 'to') or (ben == 'both'):
                        counts.update([(tag,agent,'bo',)])
                    if (ben == 'neither') or (ben == 'unknown'):
                        counts.update([(tag,agent,'bn',)])
                    # update agent+harmee 
                    if (mal == 'from') or (mal == 'both'):
                        counts.update([(tag,agent,'hs',)])
                    if (mal == 'to') or (mal == 'both'):
                        counts.update([(tag,agent,'ho',)])
                    if (mal == 'neither') or (mal == 'unknown'):
                        counts.update([(tag,agent,'hn',)])
                        
                elif (agent == 'o'):
                    counts.update([(tag,agent,)])  # update agent counts
                    # update with benefittees
                    if (ben == 'to') or (ben == 'both'):
                        ben_type = t.get('toID').strip('1234567890')
                        if (ben_type == 'a') or (ben_type == 'p'):
                            counts.update([(tag,agent,'b'+ben_type,)]) # caused by object, helped protagonist or antagonist
                        elif (ben_type == 'otr') or (ben_type == 'U'):
                            counts.update([(tag,agent,'b?',)]) # caused by object, helped someone else
                    elif (ben == 'neither') or (ben == 'unknown'):
                        counts.update([(tag,agent,'bn',)]) # caused by object, helped none/unknown
                    # update with harmees  
                    if (mal == 'to') or (mal == 'both'):
                        mal_type = t.get('toID').strip('1234567890')
                        if (mal_type == 'a') or (mal_type == 'p'): 
                            counts.update([(tag,agent,'h'+mal_type,)]) # caused by object, harmed protagonist or antagonist
                        elif (mal_type == 'otr') or (mal_type == 'U'):
                            counts.update([(tag,agent,'h?,')]) # caused by object, harmed someone else
                    elif (mal == 'neither') or (mal == 'unknown'):
                        counts.update([(tag,agent,'hn',)]) # caused by object, harmed none/unknown
                    # we don't care about benefits/harms 'from'.
            else:
                print ('Something is rotten in the state of Denmark')
    
    # set up the output vector
    vector = [] 
    for dim in sorted(counts.keys()): # ensure order of dimensions is always identical!
        vector.append(counts[dim]) # update vector with counts
    return vector
            

# run extraction
PATH = '/media/clay/SHARED/acad/brandeis/2015_2016-spring/NLAML/writerec_corpus/annotations/gold_standard/'
for f in sorted(os.listdir(PATH)):
    if f[-4:].lower() == '.xml':
        v = extract(os.path.join(PATH,f))
        print (f, v)


'''#TODO remove quotes

# run script from terminal
if __name__ == '__main__':
    PATH = sys.argv[1] # give the corpus directory in command-line input
    for FILENAME in os.listdir(PATH):
        if FILENAME[-4:].lower() == '.xml':
            extract(os.path.join(PATH,FILENAME))
            
'''