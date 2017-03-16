# -*- coding: utf-8 -*-
"""
Just a Demo on object movement, that may be exteded to a multi-object-tracking experiment.
'Task' in this demo is to track the dot that is presented in the first screen with a blue outline.
A key press starts the motion for 360*2 frames. A post-motion display shows the blue outline again,
so that you can check whether you followed the target.
The demo requires a full psychopy install including all dependencies
Created in Feb 2017
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

elements = 50                               # number of elements in the ElementArrayStim
xLow = yLow = -200                          # bounds left and down
xHigh = yHigh = 200                         # bounds up and right

import random                               # numpy.random is better, but anyway

ran_xy =[]                                  # initializing the starting position list
for i in range(elements):                   # repeat for each element
    ran_x = random.uniform(xLow,xHigh)      # draw random x position withing bounds
    ran_y = random.uniform(yLow,yHigh)      # draw random y position with bounds
    ran_xy.append([ran_x, ran_y])           # append (x,y) to list of starting positions

myDisks = visual.ElementArrayStim(win, units = 'pix', nElements=elements, elementTex=None, 
                                  elementMask='circle', sizes=20, colors='yellow',xys=ran_xy)

                                            # produces arrays for x and y increments, here
ran_dx = []                                 # called dx and dy. Each element gets its own
ran_dy = []                                 # direction in speed, randomly determined
for i in range (elements):                  # Note: the reason why xs and ys come in separate
    ran_x = random.uniform(-3.5,3.5)        # vectors rather than in (x,y) pairs is that below
    ran_y = random.uniform(-3.5,3.5)        # the vectors are needed
    ran_dx.append(ran_x)
    ran_dy.append(ran_y)

myDisks.draw()                              # this draws the elements at their initial 
myRect.draw()                               # locations, and marks one of the elements 
myCircle.pos=ran_xy[0]                      # (the 1st) with a blue circle. then waits for a 
myCircle.draw()                             # keypress to start the movement
win.flip()                                  #    
event.waitKeys()

for frame in range (3000):                  # here the movement part starts
    myDisks.xys+=zip(ran_dx,ran_dy)         # vectors of x, y increments are added
    myDisks.draw()                          # to the vector of present positions
    myRect.draw()   
    win.flip()
    xys = myDisks.xys                       # get current positions of elements
    xs,ys =zip(*xys)                        # get lists of x pos, and list of y pos
    for x in range(len(xs)):                # test each x position
        if xs[x] < xLow:                    # is x beyond lower x-bounds?
            ran_dx[x] = -ran_dx[x]          # then reverse movement direction
        elif xs[x] > xHigh:                 # is x beyond higher x-bounds?
            ran_dx[x] = -ran_dx[x]          # then reverse movement direction
    for y in range(len(ys)):                # note that as vectors are implenented as lists
        if ys[y] < yLow:                    # it is possible to address and change single
            ran_dy[y] = -ran_dy[y]          # elements within the vector
        elif ys[y] > yHigh:
            ran_dy[y] = -ran_dy[y]
    if event.getKeys():                     # stop if any key is pressed
        break

myDisks.draw()                              # post display: presents blue circle again
myRect.draw()                               # so that you can check wether you accurately
myCircle.pos=xys[0]                         # tracked the circle
myCircle.draw()
win.flip()
event.waitKeys()

win.close()
