# -*- coding: utf-8 -*-
"""
Modified circular display for testing possible display designs
Created in Mar 2017 @author: GHorstmann
"""
#CONSTANTS
screenSize = (1024,768)
SCREENSIZE = screenSize
xM = screenSize[0]/2
yM = screenSize[1]/2
myExtraInfo = {'experiment': 'proSaccade', 'SNo': '1'}

from psychopy import visual, core, event, data, misc, gui
from numpy import random
import os

myDlg = gui.Dlg(title="Search")
myDlg.addText('Subject info')
myDlg.addField('SNo', '')
myDlg.addField('Age:', choices=[16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])
myDlg.addField('Sex', choices=["m","w","x"])
myDlg.addText('Experiment Info')
myDlg.addField('Name',"VS 001")
myDlg.addField('Condition:', choices=["narrow", "wide"])
sessData = myDlg.show()
myExtraInfo = {'SNo': sessData[0],'Age': sessData[1],'Sex': sessData[2], 'ExperimentName' : sessData[3], 'Condition' : sessData[4]}
print myExtraInfo


#START EYETRACKER STUFF
import pylink as pl
el = pl.EyeLink()

def eyeTrackerInit (SCREENSIZE):
    el.sendCommand("screen_pixel_coords = 0 0 %d %d" %(SCREENSIZE[0]-1, SCREENSIZE[1]-1))
    el.sendMessage("DISPLAY_COORDS  0 0 %d %d" %(SCREENSIZE[0]-1, SCREENSIZE[1]-1))
    el.sendCommand("select_parser_configuration 0")
    el.sendCommand("scene_camera_gazemap = NO")
    el.sendCommand("pupil_size_diameter = %s"%("YES"))

def eyeTrackerCalib (el,sp,cd):
    pl.openGraphics(sp,cd)
    pl.setCalibrationColors((255,255,255),(127,127,127))
    pl.setTargetSize(int(sp[0]/70), int(sp[1]/300)) 
    pl.setCalibrationSounds("","","")
    pl.setDriftCorrectSounds("","off","off")
    el.doTrackerSetup()
    pl.closeGraphics()
    el.setOfflineMode()

def eyeTrackerSetup (el):
    if (el.getTrackerVersion()== 2):
        el.sendCommand("select_parser_configuration 0");
    #else:
    #    el.sendCommand("saccade_velocity_threshold = 35");
    #    el.sendCommand("saccade_acceleration_threshold = 9500");
    el.setFileEventFilter("LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON");
    el.setFileSampleFilter("LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS");
    el.setLinkEventFilter("LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON");
    el.setLinkSampleFilter("LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS");
    el.sendCommand("button_function 5 'accept_target_fixation'");    

def reCalibrate(el,sp,cd):
    blockLabel=visual.TextStim(win,text="Press C to begin re-calibration",pos=[0,0], color="white", bold=True,alignHoriz="center",height=0.5)
    blockLabel.draw()
    win.flip()
    core.wait(1)
    win.winHandle.minimize()
    pl.openGraphics(sp,cd)
    eyeTrackerCalib(el,sp,cd)
    pl.closeGraphics()
    win.winHandle.set_visible(True)
    win.winHandle.maximize()
    win.winHandle.activate()

def initializeTracker(sp):
    eyeTrackerInit(sp)
    eyeTrackerCalib(el,sp, 32)
    eyeTrackerSetup(el)
    return el

initializeTracker(SCREENSIZE)

#MAKE DIRECTORIES FOR RESULTS FILES
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
if myExtraInfo['SNo'] == '':
    myExtraInfo['SNo'] = '99999'
resultsPath = _thisDir + os.sep + 'results' + os.sep + '%s' % str(myExtraInfo['SNo'])
if not os.path.exists(resultsPath):
    os.makedirs(resultsPath)

#OPEN EDF ON TRACKER
edfFileName = myExtraInfo['SNo']+".EDF"
el.openDataFile( edfFileName )

#PSYCHOPY VISUALS
#DEFINE WINDOW
win = visual.Window(size=(SCREENSIZE), fullscr=True, units='pix', color='grey')
win.winHandle.activate()

fix = visual.GratingStim(win, tex='none', size=(20,20), mask="gauss")
tar = visual.GratingStim(win, tex='none', size=(20,20), mask="gauss")
emptyScreen = visual.GratingStim(win, size=(0,0))
instr = visual.TextStim(win, text='Initialize', color = "white")
instr.draw; win.flip(); core.wait(1)
ms = event.Mouse(win=win)
ms.setVisible(False)

# PSYCHOPY CLOCKS
trialClock = core.Clock()
responseClock = core.Clock()
event.waitKeys()

#DEFINE VISUAL STIMULI
myPatch = visual.Rect(win,  width=30, height=60, ori=0, fillColor = "white", lineWidth=0)      #the patch
myFix = visual.GratingStim(win, tex=None, mask="raisedCos", ori=45, color="white", size=10)    #the fix
myCircleO=visual.Circle(win, radius=10,edges=32,fillColor='grey')                              #outer circle of ring
myCircleI=visual.Circle(win, radius=5,edges=32,fillColor='white')                              #inner circle of ring
myGap=visual.Rect(win, width=8, height=5, fillColor='white',lineWidth=0)                       #the gap; it is a rectangle to account for pixel errors
myEmptyScreen= visual.Rect(win, width=8, height=5, fillColor='grey',lineWidth=0)                      

#INITIALIZE VISUALS
visual.TextStim(win, text = 'Initializing Visual Search', color='red').draw()                  #draw nameless "Hi There" text
win.flip ()
core.wait(1)

#MAKE DESIGN
design =[]
for repetition in range(4):
    for i, j in zip(['pres', 'abs'], ['left', 'down']): #absent and present
        for k in [1,3,5,7]: #the number of sings
            myList = list(random.choice(8,size=k,replace=False)) # returns a list of "sing" positions
            tarPos = random.choice(8) # target position is random, avoiding combinational explosion
            design.append({'AbsPres': i, 
                           'TarPos': tarPos, 
                           'SingPos': myList, 
                           'NumberSings': k, 
                           'RequiredKey': j,
                           'Surprise': 0
                           })
#MAKE SURPRISE TRIAL
random.shuffle(design)
design.append({'AbsPres': 'abs', 'TarPos': 0, 'SingPos': [0], 'NumberSings': 1, 'RequiredKey': 'down', 'Surprise': 1})

#MAKE TRIALS
trials = data.TrialHandler(design, 1, method='sequential', extraInfo = myExtraInfo)
trials.data.addDataType('trialNum')
trials.data.addDataType('rt')
trials.data.addDataType('givenKey')
trials.data.addDataType('cor')
print design # for debugging


def drawColorPatch (x,y):
    myPatch.pos=(x,y)
    myPatch.draw()

def drawRing (x,y):
    myCircleO.pos=(x,y) #outer circle of ring (the visible part)
    myCircleO.draw()
    myCircleI.pos=(x,y) #inner circle of ring (the bg-color part)
    myCircleI.draw()

def drawGap (x,y,gapOrientation):
    [k,l] = misc.pol2cart(gapOrientation, 8) # x,y position of the gap relative to annulus
    myGap.ori=-gapOrientation # mind the minus - polar coordinates go cc, ori goes clockwise
    myGap.pos=(x+k,y+l) #x,y position of the gap relative to screen center
    myGap.draw()

def makeDisplay (singPosList, patchOri, tarPos, absPres, gapOrientations):
    radius = 150
    for stimIndex in range (8):      # for each of the eight stimuli do
        if stimIndex in singPosList: # check whether stimIndex is "sing"
            myPatch.ori=patchOri     # if so, set ori accordingly
            oriFlag = 'sing'
        else: 
            myPatch.ori=0
            oriFlag = 'stan'
        alpha = 360/8*stimIndex      # polar coordinate of this stimulus
        [x,y] = misc.pol2cart(alpha, radius)  #cartesian (x,y) coordiante of stimulus
        drawColorPatch(x,y)
        drawRing(x,y)
        if absPres == 'pres' and stimIndex == tarPos:
            tarFlag = 'target'
        else:
            gapOrientation = gapOrientations[stimIndex]
            drawGap(x,y,gapOrientation)
            tarFlag = 'notarg'
        stimText = oriFlag + tarFlag
        xEL, yEL = xyPP2EL (x,y)
        msg = "!V IAREA ELLIPSE\t %i \t %i \t %i \t %i \t %i \t %s \n" % (stimIndex, xEL-55, yEL-55, xEL+55, yEL+55, stimText)
        el.sendMessage(msg)

def xyPP2EL (xPsychoPy,yPsychoPy):
    xEyeLink = xPsychoPy+xM
    yEyeLink = -yPsychoPy+yM
    return (int(round(xEyeLink)), int(round(yEyeLink)))


def runBlock (trials):
    for trialNum, trial in enumerate(trials):
        #INITIATE EYELINK FOR THIS TRIAL
        el.sendMessage("TRIALID "+str(i))
        el.startRecording(1, 1, 1, 1)
        el.sendMessage("DISPLAY_COORDS 0, 0, %d %d" %(SCREENSIZE[0]-1, SCREENSIZE[1]-1))
        el.sendMessage("FRAMERATE "+str(win.getActualFrameRate()))
        el.sendMessage("SYNCTIME "+str(trialClock.getTime()))
        el.sendMessage("trackerVersion %s" % el.getTrackerVersionString())
        el.flushKeybuttons(0)
        
        event.clearEvents()

        gapOrientations = [0,45,90,135,180,225,270,315]
        random.shuffle(gapOrientations)
        mySingOrientations = [-30,-20,-10,10,20,30]
        if myExtraInfo['Condition']=='narrow':
            mySingOrientations = [-15,-10,-5,5,10,15]
        random.shuffle(mySingOrientations)
        patchOri = mySingOrientations[0]

        singPosList = trial['SingPos']
        tarPos = trial['TarPos']
        absPres = trial['AbsPres']
        surprise = trial['Surprise']
    
        myEmptyScreen.draw()
        win.flip()
        core.wait(1,hogCPUperiod=0.2)

        myFix.draw()
        win.flip()
        core.wait(1,hogCPUperiod=0.2)
       
        if surprise == 1:
            #singPosList = [0]
            singPosList = list(random.choice(8, size=1))
            patchOri = 90
            
        makeDisplay (singPosList, patchOri, tarPos, absPres, gapOrientations)
        win.flip()
        el.sendMessage('DISPLAY_ON')
        responseClock.reset()
        res = event.waitKeys(['left','right'],timeStamped=True)
        el.sendMessage('KEYPRESS')
        el.sendMessage('ENDBUTTON')
        el.sendMessage('TRIAL OK')
        key, rt = res[0]
        if key in trial['RequiredKey']:
            cor = 1
        else:
            cor = 0
        #WRITING STUFF TO PSYCHOPY OUT    
        trials.data.add('cor', cor)
        trials.data.add('givenkey', key)
        trials.data.add('rt', int(round(rt)))
        trials.data.add('trialNum', trialNum)
        #from PIL import ImageGrab
        #screenshot = ImageGrab.grab()
        #screenshotName = 'scs'+str(trialNum)+'.png'
        #screenshot.save(screenshotName)

        #WRITING STUFF TO EYELINK
        el.sendMessage("!V TRIAL_VAR TrialNum %s" % str(trialNum))
        el.sendMessage("!V TRIAL_VAR SingPosList %s" % str(singPosList))
        el.sendMessage("!V TRIAL_VAR TarPos %s" % str(tarPos))
        el.sendMessage("!V TRIAL_VAR AbsPres %s" % str(absPres))
        el.sendMessage("!V TRIAL_VAR Surprise %s" % str(surprise))
        el.sendMessage("!V TRIAL_VAR Correct %s" % str(cor))
        el.sendMessage("!V TRIAL_VAR RT %s" % str(int(round(rt))))
        el.sendMessage("!V TRIAL_VAR patchOri %s" % str(patchOri))
        el.sendMessage("!V TRIAL_VAR Key %s" % str(key))
        el.sendMessage("!V TRIAL_VAR NumberSings %s" % trial['NumberSings'])
        el.sendMessage("!V TRIAL_VAR RequiredKey %s" % trial['RequiredKey'])
        core.wait(0.2)
        el.stopRecording()

runBlock(trials)

#TIDY UP AFTER EXPERIMENT
core.wait(0.01)
el.setOfflineMode()
el.closeDataFile()
el.receiveDataFile(edfFileName, resultsPath+ os.sep+edfFileName)
el.close()
win.mouseVisible=True
win.close()
trials.printAsText(dataOut='all_raw')
df = trials.saveAsWideText('proSaccade.csv', delim=';')
core.quit()


