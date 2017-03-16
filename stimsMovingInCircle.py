# -*- coding: utf-8 -*-
"""
Stims moving on circluar pathways.
The motion aftereffect is clearly visible when the movement stops  
@author: GHorstmann
"""

from psychopy import visual, core, event

win = visual.Window(size=(1024,768), 
    fullscr=False,  
    screen= 0,  
    color="grey", 
    colorSpace = 'rgb',
    units = 'pix')
myText = visual.TextStim(win, text = 'Initializing', color='red')       
myText.draw(); win.flip ();core.wait(.1)     
myRect = visual.Rect(win, height=410, width=410, fillColor='lightgrey', opacity=.30, lineColor=None)
myCircle =visual.Circle(win, size=22, lineColor='blue')
myFix=visual.TextStim(win, text='+', color='black')
elements = 20

from psychopy import tools

xysCircle=[]
for i in range(elements):
    myTheta = 360/elements*(i)+10
    myCoord = tools.coordinatetools.pol2cart(myTheta, 100)
    xysCircle.append(myCoord)

myDisks = visual.ElementArrayStim(win, units = 'pix', nElements=elements, elementTex=None, 
                                  elementMask='circle', sizes=20, colors='yellow',xys=xysCircle)


myDisks.draw()
myRect.draw()
win.flip()
event.waitKeys()
for i in range (360*2):
    rotatingCoords=[]
    for j in range (elements):
        myTheta =360/elements*(j)+i
        myCoord= tools.coordinatetools.pol2cart(myTheta, 100)
        rotatingCoords.append(myCoord)
    myDisks.xys=rotatingCoords
    myDisks.draw()
    myFix.draw()
    win.flip()
event.waitKeys()
win.close()

"""
I see 5 optical illusions
1. a blue afterimage following the circles
2. the circles seem to rotate themselves in the opposite directection
    in partciular with low set sizes (try 6)
3. with higher set sizes, an inner yellow circle appears
4. when the movement stops, there is apparent movement in other direction
5. at higher set sizes, groups of 4-5 circles become stable
"""