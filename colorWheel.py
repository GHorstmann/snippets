#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 07:52:11 2017
@author: ghorstmann
This central code piece actually comes from a blog entry by Jonathan Pierce
https://discourse.psychopy.org/t/colour-wheel-implementation/1580
I basically only included the mouse pointing and the display of the selected color
"""
from psychopy import visual, misc, event, tools
import numpy as np

win = visual.Window()

# If texture res if low you can still get a smooth ring by
# turning interpolation on and having a high anuglar res on the stimulus
textureRes = 128


hsv = np.ones([textureRes,textureRes,3], dtype=float)
hsv[:,:,0] = np.linspace(0,360,textureRes, endpoint=False)
hsv[:,:,1] = 1
hsv[:,:,2] = 1
rgb = misc.hsv2rgb(hsv)

#mask gives the fraction of the that is visible
mask = np.zeros([100,1])
mask[-10:] = 1  # 10% of the radius is 1 (visible)
# annoyingly with interpolate=True the mask outer edge can 
# get blended with innermost pixel

stim = visual.RadialStim(win, tex=rgb, 
                        mask = mask,
                        angularRes=64, angularCycles=1, 
                        angularPhase=1,interpolate=True)
stim.draw()
win.flip()
myMouse=event.Mouse()
myMouse.clickReset()
while True:
    mouseIsDown = myMouse.getPressed ()[0]
    if mouseIsDown:
        x,y= myMouse.getPos()
        theta, radius = misc.cart2pol(y,x)  # I have no idea why xy order has to be reversed here
        print x, y                          # please give me a clue if you know
        print theta, radius 
        break

rgbCol = tools.colorspacetools.hsv2rgb([theta,1,1])
print rgbCol
rect = visual.Rect(win, width=0.5, height=0.5, fillColor = rgbCol, fillColorSpace='rgb')
stim.draw()
rect.draw()
win.flip()
event.waitKeys()  
win.close()