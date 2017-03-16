#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Posner Cueing Demo 
(to run it as an Experiment, RT measurement has to be added)
Created on Mon Mar  6 19:39:19 2017
@author: ghorstmann
"""

from psychopy import visual, core, event, data

win = visual.Window(size=(1024,768), 
    fullscr=False,  
    screen= 0,  
    color="grey", 
    colorSpace = 'rgb',
    units = 'pix')
myText = visual.TextStim(win, text = 'Initializing Posner Cueing', color='red')       
myText.draw(); win.flip ();core.wait(1)     

myRect = visual.Rect(win, width=80, height=80, units='pix', lineColor='white', lineWidth=2)
myRectLight = visual.Rect(win, width=80, height=80, units='pix', lineColor='white', lineWidth=4)
target = visual.Rect(win, width=10,height=10, units='pix', lineColor='white', fillColor='white')
#myShape = visual.ShapeStim()

design =[]
for cuePos in [-100,0,100]: # cue could be left, middle or right
    for tarPos in [-100,100]: # target could be left or right
        for soa in range (0,5,2): #specified in frames
            design.append({'cuePos': cuePos, 'tarPos':tarPos, 'soa': soa})

trials = data.TrialHandler(design, 1, method='random')
print design

def drawFrames ():
    myRect.pos=(-100,0)
    myRect.draw()
    myRect.pos=(0,0)
    myRect.draw()
    myRect.pos=(100,0)
    myRect.draw()
    
def lightFrame (pos):
    myRectLight.pos=(pos,0)
    myRectLight.draw()
    

for trial in trials:
    #central rect as foreperiod
    myRect.pos=(0,0)
    myRect.draw()
    win.flip()
    #ms precision not necessary for foreperiod
    core.wait(1)
    for frame in xrange(200):                  #remainder of trial lasts 200 flips
        if 0 <=frame < 200:                   #for the first 100 flips only frames
            drawFrames()                      #call function drawFrames()
        if 100 <= frame < 102:                #frames 100-102
            lightFrame(trial['cuePos'])       #call function lightFrame()
        if 100+trial['soa'] <= frame < 100+trial['soa']+2:#variable soa; note: soa is number of frames
            target.pos=(trial['tarPos'],0)    #here is the target
            target.draw()
        win.flip()                            #drawing finished, now flip
    if event.getKeys() == 'space':                       #abort when any key is pressed
        break

event.waitKeys()
win.close()