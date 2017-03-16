# -*- coding: utf-8 -*-
"""
The problem was to generate a list of positions for stimuli such that the stimuli do not overlap.
This is a common requirement for experiments presenting multiple stimuli simultaneously such as 
visual search or VSTM-Experiments. One common solution is to put the stimuli in a matrix and adding 
jitter; this is however not used here.
Here the plan was to simultaneously fill the list with random positions, with each new random position 
being tested for overlap before adding it to the list. The script contains essentially two functions:
overlap() tests for overlap, and makePositions() generates the position list
the rest of the script is just a demonstration that the positions actually do not overlap
Note: Stimuli are squares in this version, but it should be easy to replace them by circles, or 
rectangles.
Note: The script may hang if too many positions are required in an area too small.
It should be easy to include somenting, but this is not implemented here.
Created on Thu Mar 09 14:23:12 2017 @author: GHorstmann
"""


def overlap (s1, s2, size):
    '''
    Tests for overlap between two squares of equal size
    INPUT center coordinates for s1 and s2 and size
    OUTPUT true (overlap exits) or false (no overlap)
    '''
    hoverlap, voverlap = False, False
    if abs(s1[0]-s2[0])<= size: # if x-axis distance smaller than size
        hoverlap = True
    if abs(s1[1]-s2[1])<=size:  # if y-axis distance smaller than size
        voverlap = True
    if hoverlap and voverlap:   # overlap of area only if h and v overlap
        return True
    else:
        return False

import random
    
def makePositions (numberOfPos, size):
    '''
    Generates a list ("posList") of non-overlapping screen regions 
    IN desired number of positions and the size of the non-overlapping area
    OUT List of positions
    '''
    posList = []                            #begin with empty list

    while len(posList) < numberOfPos:       #list is not filled as planned
        x=random.randint(-150,150)          #random x
        y=random.randint(-100,100)          #random y

        if len(posList)==0:                 #if first pos, append to list
            posList.append([x,y])

        else:                               #in any other case

            for pos in posList:             #cycle through pos in posList
                test = overlap(pos, [x,y], size)   #test overlap of pos and new xy
                if test == True:            #overlap = bad
    #                print 'repeat'          #for debugging only
    #                print pos               #for debugging only
    #                print x,y               #for debugging only
                    break                   #break for-loop and try again
            else:                           #thanks Sebastiaan for presenting this...
                posList.append([x,y])       #if no break occurred: append
    return posList


#here the above two functions are used to demonstrate that they work properly

from psychopy import visual, core

posList = makePositions (10,50) # mind: if the number of position do not fit the area, this may run endless.
win = visual.Window(size=(1024,768), fullscr=False, units='pix')
myRect = visual.Rect(win, width=50, height=50, units='pix')

for pos in posList:
    myRect.pos=pos
    myRect.draw()
win.flip()
core.wait(4)
win.close()
              
