# -*- coding: utf-8 -*-
"""
Demo of a circular search display with color patches and rings /landolt-c as stimuli
similar to those in Horstmann & Herwig (2016), Horstmann, Becker, & Ernst (2016), with
eight positions and target present /absent judgements. 
Non-targets are landolt-c, target is ring.
the GUI at the beginning is not used because it crashes when using spyder/anaconda
All stimuli are drawn as needed, avoiding external image files, beginning with the 
color patch, then the ring, than the gap, and on top, if needed, the target.
Created on Mon Mar 2017 @author: GHorstmann
"""
### showing a welcome screen
from psychopy import visual, core
win = visual.Window(size=(800,600), 
    fullscr=False,  
    screen= 1,  
    color="grey", 
    colorSpace = 'rgb',
    units = 'pix')
textScreen = visual.TextStim(win, text = 'Initializing Visual Search', color='red')
for frame in range (10): textScreen.draw(); win.flip ()

### getting info about experiment
from psychopy import gui

myDlg = gui.Dlg(title="Scaling")
myDlg.addText('Subject info')
myDlg.addField('Subject Number', choices=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
myDlg.addField('Age:', choices=[16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])
myDlg.addField('Sex:', choices=["m","w","x"])
myDlg.addText('Experiment Info')
myDlg.addField('Name:',"VS 001")
myDlg.addField('Group:', choices=["Test", "Control"])
#sessData = myDlg.show()
#essionInfo = {'SubjectNo': sessData[0],'Age': sessData[1],'Sex': sessData[2], 'ExperimentName' : sessData[3]}
sessionInfo = {'SubjectNo': 0,'Age': 0,'Sex': 0, 'ExperimentName' : 0} # for debugging
print sessionInfo

# warn of commencing first trial
textScreen.setText(text='Achtung, der erste Trial beginnt gleich')
for frame in range (20): textScreen.draw(); win.flip ()

# generating design
design =[]
for i in range(2): #absent and present
    for j in range (8): #target position
        design.append({'AbsPres': i, 'TarPos': j})

from psychopy import event, data

trials = data.TrialHandler(design, 1, method='random', extraInfo=sessionInfo)
trials.data.addDataType('TrialNum')
print design


# stim presentation
from numpy import random
from psychopy import misc
radius = 150
myPatch = visual.GratingStim(win, tex=None, mask="raisedCos", ori=45, size=50, color = "white") #the patch
myFix = visual.GratingStim(win, tex=None, mask="raisedCos", ori=45, color="white", size=10)    #the fix
myCircleO=visual.Circle(win, radius=10,edges=32,fillColor='grey')                              #outer circle of ring
myCircleI=visual.Circle(win, radius=5,edges=32,fillColor='white')                              #inner circle of ring
myRect=visual.Rect(win, width=8, height=5, fillColor='white',lineWidth=0)                      #the gap; it is a rectangle to account for pixel errors

for trial in trials:

    myGapOrientation = [0,45,90,135,180,225,270,315]
    random.shuffle(myGapOrientation)

    trialOn = True

    while trialOn:

        for frame in range(1000):

            if 0 <=frame<=50:
                myFix.draw()

            if 50<=frame<=1000:

                for i in range (8): # 8 stimuli
                    #at which stimulus position are we?
                    alpha = 360/8*i # polar coordinate of ith stimulus
                    [x,y] = misc.pol2cart(alpha, radius)  #cartesian (x,y) coordiante of stimulus
                    #draw the color patch
                    myPatch.pos=(x,y)
                    myPatch.draw()
                    
                    #draw the ring
                    myCircleO.pos=(x,y) #outer circle of ring (the visible part)
                    myCircleO.draw()
                    myCircleI.pos=(x,y) #inner circle of ring (the bg-color part)
                    myCircleI.draw()
                    
                    #draw the gap
                    [k,l] = misc.pol2cart(myGapOrientation[i], 8) # x,y position of the gap relative to annulus
                    myRect.ori=-myGapOrientation[i] # the tilt of the rectangular gap; mind the minus - polar coordinates go cc, ori goes clockwise
                    myRect.pos=(x+k,y+l) #x,y position of the gap relative to stimulus center
                    myRect.draw()
                    
                    #draw the target, if at target position and in a target trial
                    if i == trial['TarPos']:    #are we with the correct position?

                       if trial['AbsPres']== 1: #are we in a target trial?

                           myCircleO.pos=(x,y)  #put just anonther annulus on top of the previous
                           myCircleO.draw()     #yes: the if clause could have been made before
                           myCircleI.pos=(x,y)  #gap drawing
                           myCircleI.draw()
            if 1000<=frame:
                break
            if event.getKeys():
                break
            win.flip()
            #print frame #for debugging
        trialOn = False
trials.printAsText(dataOut='all_raw')
win.close()



