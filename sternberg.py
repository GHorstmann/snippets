# -*- coding: utf-8 -*-
"""
Sternberg type of iconic memory experiment
- presents letter matrix
- presents high, middle, or low tone
- following a variable SOA
- gives a feedback on the correct answer
Created on Tue Mar 07 15:50:07 2017

@author: GHorstmann
"""
from psychopy import visual, core, event, data

win = visual.Window(size=(1024,768), 
    fullscr=False,  
    screen= 0,  
    units = 'pix',
    color = 'grey')
myText = visual.TextStim(win, text = 'Initializing', color='red')       
myText.draw(); win.flip ();core.wait(.8) 

 #letters
letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
myLetter = visual.TextStim(win, text = 'Z', color='white', height=25)

 #positions
xys =[]
xs = range (-60,61, 40)
ys = range (-60,61, 60)
ys.reverse()                                #begin in top row, then middle, then low
for y in ys:                                #no error - begin with ys
    for x in xs:                            #xys should be ordered rowwise
        xys.append([x,y])                   #not columnwise

 #sounds
from psychopy import prefs
prefs.general['audioLib'] = ['sounddevice']         #pyo makes a problem in this release
from psychopy import sound
mySound = sound.Sound(value="c", secs=0.05, octave=4)
mySound.setVolume(0.2)

def playSounds ():
    for tone in ['c','e','g']:
        mySound.setSound(value=tone)
        mySound.play()
        core.wait(.2)
        mySound.stop()                     #for some reason, behaves very weird, unless the stop() method is applied
        

def drawFixation ():
    myLetter.text='+'
    myLetter.pos=(0,0)
    myLetter.draw()

def drawLetters ():
    for i in range(len(xys)):                #for each position
        myLetter.text=letters[i]             #set letter
        myLetter.pos=xys[i]                  #set position
        myLetter.draw()                      #draw letter

def drawEmpty ():
    myLetter.text=' '
    myLetter.draw()

design = []
for soa in [0,2,4,8,16]:
    for tone in ['c','e','g']:
        design.append({'soa':soa,'tone':tone})
        
trials=data.TrialHandler(design, 1, method='random')
import random

for trial in trials:
    random.shuffle(letters)
    if event.getKeys('space'):
        break
    for frame in range (300):
        if 0 <= frame < 150:
            drawFixation()
        else:
            if 150 <= frame < 158:
                drawLetters()
            if 158+trial['soa'] == frame:
                mySound.setSound(value=trial['tone'],secs=0.1)
                mySound.play()
            if 158 <= frame < 300:
                drawEmpty()
        win.flip()
        if frame == 0:                      #important to play the sound after
            playSounds()                    #win.flip() otherwise flip is delayed on Mac

    ##give corrects
    if trial['tone']=='g':                  #something odd here
        answer = letters[0:4]               #program behaves as required
    if trial['tone']=='e':                  #but since letters are filled 
        answer = letters[4:8]               #from top, 'c' should 
    if trial['tone']=='c':                  #contain letters[0:4]
        answer = letters[8:12]              #if you find out, give me a clue
    myLetter.text = answer
    myLetter.pos = (0,0)
    myLetter.draw()
    win.flip()
    core.wait(3)
core.wait(.01)


win.close()

