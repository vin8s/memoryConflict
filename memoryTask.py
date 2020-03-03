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
    size=(1280, 800), fullscr=False, allowGUI=False,
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

possKeys = [['A', 'a'],['L', 'l']]
shuffle(possKeys)
expInfo['OldKeys'] = possKeys[0]
expInfo['NewKeys'] = possKeys[1]

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

#initialization of initial directions
directions = visual.TextStim(
    win = win,
    text = "" + expInfo['OldKeys'][0] + " for Old or previously seen stimuli. " + expInfo['NewKeys'][0] + " for New or never seen stimuli.",
    color = (-1, -1, -1),
    autoLog = False,
)

#initialization of constantly presented directions
consDir = visual.TextStim(
    win = win,
    text = " = Old (previously seen);\n = New (never seen)",
    color = (-1, -1, -1),
    pos = (0, 0.65),
    autoLog = False
)

#initialization of colored directions
coloredButtons = visual.TextStim(
    win = win,
    text = "" + expInfo['OldKeys'][1] + "/" + expInfo['OldKeys'][0] + "\n" + expInfo['NewKeys'][1] + "/" + expInfo['NewKeys'][0],
    color = 'Red',
    pos = (-0.38, 0.65),
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

with open(os.path.join(pathExtension, dataSetFileName), 'w', newline = '') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(list(expInfo.keys()))

#helper methods for use later on
def to_frames(t):                                                                 # Converts time to frames accounting for the computer's refresh rate (aka framelength); input is the desired time on screen, but the ouput is the closest multiple of the refresh rate
    return int(round(t / framelength))

imgDuration = to_frames(3.0)                                                                #image duration
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
for i in range(270):
    memTrialOrder.append('o')                                                   #appending 4/5 of set to be 'old'
for i in range(90):
    memTrialOrder.append('n')                                                   #appending 1/5 of set to be 'new'
shuffle(memTrialOrder)

precode = "mtask/"                                                               #precode to access the set of images

trialClock = core.Clock()
for frameN in range(to_frames(5)):
    directions.draw()
    win.flip()


randStart = 'M'
needsPrompt = False                                                              #if participant doesn't respond fast enough, prompts them to respond faster



for numTimes in range (2):
    countdown(3)
    for j in range(10):
        i = numTimes * 10 + j
        stim = memTrialOrder[i]
        if stim == 'o':                                                             #if the stimulus is 'old'
            case = imgOrder.pop(0)[0].upper()
            if (case == 'M'):
                name = "" + case + str(mSetImgRand.pop(0) + 1) + ".jpg"
            else:
                name = "" + case + str(nSetImgRand.pop(0) + 1) + ".jpg"
            corrAns = expInfo['OldKeys']
            expInfo['seenBefore'] = True
        else:
            name = "" + randStart + str(imgRemNotUsed.pop(0)) + ".jpg"
            corrAns = expInfo['NewKeys']
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
        theseKeys = event.getKeys(keyList=['A', 'a', 'L', 'l'])
        event.clearEvents()
        
        trialClock.reset()
        frameN = 0
        while frameN < imgDuration:
            coloredButtons.draw()
            img.draw()
            consDir.draw()
            win.flip()
            frameN += 1
        
        theseKeys = event.getKeys(keyList=['A', 'a', 'L', 'l'], timeStamped = trialClock)
        print(theseKeys)
        didCorr = False
        
        expInfo['MemResponse'] = ""
        expInfo['Remembered'] = False
        expInfo['MemRespTime'] = -2.0
            
        if len(theseKeys) > 0:
            needsPrompt = False
            lastAns = theseKeys[-1]
            expInfo['MemResponse'] = lastAns[0]
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

