from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
import numpy as np                                                              # Whole numpy lib is available, prepend 'np.'
from numpy.random import random, randint, normal, shuffle
import random
import os                                                                       # Handy system and path functions
import sys                                                                      # to get file system encoding
import csv

#Written by Vin Somasundaram

_thisDir = (os.path.dirname(
            os.path.abspath(__file__)))

expName = 'Memory_script'                                                          # From the Builder filename that created this script
expInfo = {'participant':'','session':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()                                                                 # User pressed cancel during popout
expInfo['date'] = data.getDateStr()                                             # Add a simple timestamp
expInfo['expName'] = expName

pathExtension = _thisDir + "/data/" + expInfo['participant']
dataSetFileName = "memoryDataSet" + expInfo['participant'] + ".csv"
oldDataSetFileName = "dataSet" + expInfo['participant'] + ".csv"
blockDataFileName = "blockData" + expInfo['participant'] + ".txt"

#initializing window
win = visual.Window(
    size=(1280, 800), fullscr=True, allowGUI=False,
    monitor='testMonitor', color=[1,1,1], useFBO=True
)

frameRate = win.getActualFrameRate()                                              #gets FrameRate
framelength = win.monitorFramePeriod                                              #gets frameLength
expInfo['frameRate'] = frameRate

expInfo['image'] = ""
expInfo['seenBefore'] = False

expInfo['MemResponse'] = ""
expInfo['Remembered'] = False
expInfo['MemRespTime'] = -10.0

setLeft = [['A', 'a'],['S', 's']]
setRight = [['K', 'k'],['L', 'l']]
PossKeys = [setLeft, setRight]
shuffle(PossKeys)

ordering = [0,1]
shuffle(ordering)
chosenFirst = ordering[0]
chosenSecond = ordering[1]
#print(PossKeys[0])

expInfo['defOldKeys'] = PossKeys[0][chosenFirst]
expInfo['probOldKeys'] = PossKeys[0][chosenSecond]
expInfo['defNewKeys'] = PossKeys[1][chosenFirst]
expInfo['probNewKeys'] = PossKeys[1][chosenSecond]


#initialization of fixation
fixation = visual.TextStim(
    win = win,
    text = "+",
    color = (-1, -1, -1),
    autoLog = False
)

#initialization of prompt
prompt = visual.TextStim(
    win = win,
    text = "Respond Faster!",
    font = 'Arial',
    units = 'pix',
    height = 50,
    color = (-1, -1, -1),
)

#initialization of blank
blank = visual.TextStim(
    win = win,
    text = "",
    color = (-1, -1, -1),
    autoLog = False
)

"""
#initialization of initial directions
directions = visual.TextStim(
    win = win,
    text = "" + expInfo['OldKeys'][0] + " for Old or previously seen stimuli. " + expInfo['NewKeys'][0] + " for New or never seen stimuli.",
    color = (-1, -1, -1),
    autoLog = False,
)
"""

#initialization of constantly presented directions
consDir = visual.TextStim(
    win = win,
    text = "\t     = Definitely Old;\t\t\t= Probably Old \n\t     = Definitely New;\t\t= Probably New",
    font = 'Arial',
    units = 'pix',
    height = 40,
    wrapWidth = 1100,
    color = (-1, -1, -1),
    pos = (0, 270),
    autoLog = False
)

#initialization of colored directions
"""
coloredButtons = visual.TextStim(
    win = win,
    text = "" + expInfo['defOldKeys'][1] + "/" + expInfo['defOldKeys'][0] + 
    "\t\t\t\t\t\t   " + expInfo['probOldKeys'][1] + "/" + expInfo['probOldKeys'][0] +
    "\n" + expInfo['defNewKeys'][1] + "/" + expInfo['defNewKeys'][0] + 
    "\t\t\t\t\t\t   " + expInfo['probNewKeys'][1] + "/" + expInfo['probNewKeys'][0],
    font = 'Arial',
    units = 'pix',
    height = 40,
    bold = True,
    color = 'Red',
    pos = (-130, 270),
    autoLog = False,
)"""

defOldColoredButtons = visual.TextStim(
    win = win,
    text = "" + expInfo['defOldKeys'][1] + "/" + expInfo['defOldKeys'][0],
    font = 'Arial',
    units = 'pix',
    height = 40,
    bold = True,
    color = 'Red',
    pos = (-325, 297),
    autoLog = False,
)
probOldColoredButtons = visual.TextStim(
    win = win,
    text = "" + expInfo['probOldKeys'][1] + "/" + expInfo['probOldKeys'][0],
    font = 'Arial',
    units = 'pix',
    height = 40,
    bold = True,
    color = 'Red',
    pos = (65, 297),
    autoLog = False,
)
defNewColoredButtons = visual.TextStim(
    win = win,
    text = "" + expInfo['defNewKeys'][1] + "/" + expInfo['defNewKeys'][0],
    font = 'Arial',
    units = 'pix',
    height = 40,
    bold = True,
    color = 'Red',
    pos = (-325, 247),
    autoLog = False,
)
probNewColoredButtons = visual.TextStim(
    win = win,
    text = "" + expInfo['probNewKeys'][1] + "/" + expInfo['probNewKeys'][0],
    font = 'Arial',
    units = 'pix',
    height = 40,
    bold = True,
    color = 'Red',
    pos = (65, 247),
    autoLog = False,
)

#initialization of midwayStop prompt
midwayStop = visual.TextStim(
    win = win,
    text = "You are halfway through this portion of the study! \nTake a small break to rest your eyes and press spacebar to continue.",
    font = 'Arial',
    units = 'pix',
    height = 50,
    wrapWidth = 1100,
    color = (-1, -1, -1),
)

#initialization of end prompt
endStop = visual.TextStim(
    win = win,
    text = "Thank you! Please press spacebar to submit your data and complete the study.",
    font = 'Arial',
    units = 'pix',
    height = 50,
    wrapWidth = 1100,
    color = (-1, -1, -1),
)

#initialization of all Instructions-------------------------------------------------------------------------------------------------------------------------
totalDirections = []
directionsTitle = visual.TextStim(
    win = win,
    text = "Instructions: \n\nPlease read these intructions carefully before you begin the experiment.",
    color = (-1, -1, -1),
    pos = (-690, 420),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    font = 'Arial',
    bold = True,
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)
totalDirections.append(directionsTitle)

directions2 = visual.TextStim(
    win = win,
    text = "In this next part of the experiment, you will be presented with images that you previously categorized as man-made or natural "
    + "(\"Old images\") and images that you were not previously shown (\"New images\'\")",
    color = (-1, -1, -1),
    pos = (-690, 290),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    font = 'Arial',
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)
totalDirections.append(directions2)

directions3 = visual.TextStim(
    win = win,
    text = "On each trial, you will have 2 seconds per image to identify whether you saw the image previously (Old) or did not see the image (New).",
    color = (-1, -1, -1),
    pos = (-690, 195),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    font = 'Arial',
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)
totalDirections.append(directions3)

directions4 = visual.TextStim(
    win = win,
    text = "You will use the %s/%s and %s/%s keys to indicate whether an image is DEFINITELY or PROBABLY old, respectively." % (expInfo['defOldKeys'][1], expInfo['defOldKeys'][0], expInfo['probOldKeys'][1], expInfo['probOldKeys'][0])
    + "\nYou will use the %s/%s and %s/%s keys to indicate whether an image is DEFINITELY or PROBABLY new, respectively." % (expInfo['defNewKeys'][1], expInfo['defNewKeys'][0], expInfo['probNewKeys'][1], expInfo['probNewKeys'][0]) + 
    "\nThese response mappings will stay on the screen for these ratings",
    color = (-1, -1, -1),
    pos = (-690, 95),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    font = 'Arial',
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)
totalDirections.append(directions4)

directions5 = visual.TextStim(
    win = win,
    text = "Always press the a/A key with your LEFT middle finger, the s/S key with your LEFT index finger, the k/K key with your RIGHT index finger, and the l/L key with your RIGHT middle finger.",
    color = (-1, -1, -1),
    pos = (-690, -115),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    font = 'Arial',
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)
totalDirections.append(directions5)

directions6 = visual.TextStim(
    win = win,
    text = "Please stay focused during the experiment and try to respond within the time limits",
    color = (-1, -1, -1),
    pos = (-690, -215),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    font = 'Arial',
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)
totalDirections.append(directions6)

directions7 = visual.TextStim(
    win = win,
    text = "This task has 2 blocks, which will take 9 minutes each. Once you are ready to start, press the spacebar.",
    color = (-1, -1, -1),
    pos = (-690, -285),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    font = 'Arial',
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)
totalDirections.append(directions7)

presOldKeys = visual.TextStim(
    win = win,
    text = "" + expInfo['defOldKeys'][1] + "/" + expInfo['defOldKeys'][0] + "        " + expInfo['probOldKeys'][1] + "/" + expInfo['probOldKeys'][0],
    color = 'red',
    pos = (-472, 95),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    bold = True,
    font = 'Arial',
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)

presNewKeys = visual.TextStim(
    win = win,
    text = "" + expInfo['defNewKeys'][1] + "/" + expInfo['defNewKeys'][0] + "        " + expInfo['probNewKeys'][1] + "/" + expInfo['probNewKeys'][0],
    color = 'red',
    pos = (-472, 25),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    bold = True,
    font = 'Arial',
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)

pressSpacebar = visual.TextStim(
    win = win,
    text = "Press spacebar to continue.",
    color = 'green',
    pos = (-690, -370),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    font = 'Arial',
    bold = True,
    height = 30,
    wrapWidth = 1100,
    autoLog = False
)

#initializes headers of csv 
with open(os.path.join(pathExtension, dataSetFileName), 'w', newline = '') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(list(expInfo.keys()))

#helper methods for use later on
def to_frames(t):                                                                 # Converts time to frames accounting for the computer's refresh rate (aka framelength); input is the desired time on screen, but the ouput is the closest multiple of the refresh rate
    return int(round(t / framelength))

imgDuration = to_frames(2.0)                                                                #image duration
ISI = to_frames(0.5)                                                                 #Inter Stimulus Interval
ITI = to_frames(3)                                                                      #Inter Trial Interval

def countdown(num):
    for i in range (num):
        number = visual.TextStim(
            win = win,
            text = str(num-i),
            color = (-1, -1, -1),
            units = 'pix',
            font = 'Arial',
            height = 120,
            autoLog = False
        )
        
        for frameN in range(to_frames(1)):
            number.draw()
            win.flip()

varSaver = open(os.path.join(pathExtension, blockDataFileName), "r")
variables = varSaver.read()
variables = variables.split("\n")
specificVar = []
for var in variables:
    var = var.split(':')
    specificVar.append(var[1])

imgRandShuffle = specificVar[2].strip('][').split(', ')
imgRandShuffle = [int(i) for i in imgRandShuffle]
mSetImgRand = [i for i in imgRandShuffle]
nSetImgRand = [i for i in imgRandShuffle]

imgRemNotUsed = specificVar[4].strip('][').split(', ')
imgRemNotUsed = [int(i) for i in imgRemNotUsed]

imgOrder = specificVar[6].strip('][').split(', ')
imgOrder = [i.strip('\'') for i in imgOrder]

print(imgOrder)

memTrialOrder = []
for i in range(392):
    memTrialOrder.append('o')                                                   #appending 2/3 of set to be 'old'
for i in range(132):
    memTrialOrder.append('n')                                                   #appending 1/3 of set to be 'new'
shuffle(memTrialOrder)

precode = "mtask/"                                                               #precode to access the set of images

#displays all directions ---------------------------------------------------------------------------------------------------------------------
dirCount = 0
while dirCount < len(totalDirections):
    event.clearEvents()
    continueButton = event.getKeys(keyList=['space'])
    while (len(continueButton) < 1):
        pressSpacebar.draw()
        totalDirections[0].draw()
        if dirCount > 0:
            totalDirections[1].draw()
        if dirCount > 1:
            totalDirections[2].draw()
        if dirCount > 2:
            totalDirections[3].draw()
            presOldKeys.draw()
            presNewKeys.draw()
        if dirCount > 3:
            totalDirections[4].draw()
        if dirCount > 4:
            totalDirections[5].draw()
        if dirCount > 5:
            totalDirections[6].draw()
        win.flip()
        continueButton = event.getKeys(keyList=['space'])
    dirCount += 1


randStart = 'M'
needsPrompt = False                                                              #if participant doesn't respond fast enough, prompts them to respond faster


midwayCount = 262
for numTimes in range (2):
    countdown(3)
    for j in range(midwayCount):
        trialClock = core.Clock()
        i = numTimes * midwayCount + j
        stim = memTrialOrder[i]
        if stim == 'o':                                                             #if the stimulus is 'old'
            case = imgOrder.pop(0)[0].upper()
            if (case == 'M'):
                name = "" + case + str(mSetImgRand.pop(0) + 1) + ".jpg"
            else:
                name = "" + case + str(nSetImgRand.pop(0) + 1) + ".jpg"
            corrAns = [expInfo['defOldKeys'][0], expInfo['defOldKeys'][1], expInfo['probOldKeys'][0], expInfo['probOldKeys'][1]]
            expInfo['seenBefore'] = True
        else:                                                                       #else the stimulus is 'new'
            name = "" + randStart + str(imgRemNotUsed.pop(0)) + ".jpg"
            corrAns = [expInfo['defNewKeys'][0], expInfo['defNewKeys'][1], expInfo['probNewKeys'][0], expInfo['probNewKeys'][1]]
            expInfo['seenBefore'] = False
        
        allAns = []
        respTime = []
        
        expInfo['image'] = name.split(".")[0]
        print(name)
        img = visual.ImageStim(                                                       #initializes image stimuli to be presented
            win = win,
            image = precode + name,
            units = 'pix',
            autoLog = False
        )
        
        if (needsPrompt):
            for frameN in range(ISI):
                prompt.draw()
                win.flip()
        theseKeys = event.getKeys(keyList=['A', 'a', 'S', 's', 'K', 'k', 'L', 'l'])
        event.clearEvents()
        
        trialClock.reset()
        frameN = 0
        while frameN < imgDuration:
            defOldColoredButtons.draw()
            defNewColoredButtons.draw()
            probOldColoredButtons.draw()
            probNewColoredButtons.draw()
            img.draw()
            consDir.draw()
            win.flip()
            frameN += 1
        
        theseKeys = event.getKeys(keyList=['A', 'a', 'S', 's', 'K', 'k', 'L', 'l'], timeStamped = trialClock)
        print(theseKeys)
        didCorr = False
        
        expInfo['MemResponse'] = ""
        expInfo['Remembered'] = False
        expInfo['MemRespTime'] = -2.0
            
        if len(theseKeys) > 0:
            needsPrompt = False
            lastAns = theseKeys[0]
            #lastAns = theseKeys[-1]
            expInfo['MemResponse'] = lastAns[0]
            expInfo['MemRespTime'] = lastAns[1]             #do we need?
            if lastAns[0] in corrAns:
                didCorr = True
                allAns.append(didCorr)
                expInfo['Remembered'] = didCorr
                respTime.append(lastAns[1])
                expInfo['MemRespTime'] = lastAns[1]
        else:
            needsPrompt = True
            allAns.append(didCorr)
            respTime.append(-1.0)
            expInfo['Remembered'] = didCorr
            expInfo['MemRespTime'] = -1.0
            
        
        if stim == 'o':
            with open(os.path.join(pathExtension, dataSetFileName), 'a', newline='') as newFile:
                thewriter = csv.writer(newFile)
                thewriter.writerow(list(expInfo.values()))
        else:
            with open(os.path.join(pathExtension, dataSetFileName), 'a', newline='') as filer:
                thewriter = csv.writer(filer)
                thewriter.writerow(list(expInfo.values()))
        
    #displays textStim at end of experiment
    if (numTimes == 0):
        event.clearEvents()
        continueButton = event.getKeys(keyList=['space'])
        while (len(continueButton) < 1):
            midwayStop.draw()
            win.flip()
            continueButton = event.getKeys(keyList=['space'])

#displays textStim at end of experiment
event.clearEvents()
continueButton = event.getKeys(keyList=['space'])
while (len(continueButton) < 1):
    endStop.draw()
    win.flip()
    continueButton = event.getKeys(keyList=['space'])



win.close()

