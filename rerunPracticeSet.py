from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
import numpy as np                                                              # Whole numpy lib is available, prepend 'np.'
from numpy.random import random, randint, normal, shuffle
import random
import os                                                                       # Handy system and path functions
import sys                                                                      # to get file system encoding
import csv

_thisDir = (os.path.dirname(
            os.path.abspath(__file__)))

expName = 'Memory_script'                                                          # From the Builder filename that created this script
expInfo = {'participant':'','session':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()                                                                 # User pressed cancel during popout
expInfo['date'] = data.getDateStr()                                             # Add a simple timestamp
expInfo['expName'] = expName

blockDataFileName = "blockData" + expInfo['participant'] + ".txt"

#initializing window
win = visual.Window(
    size=(1280, 800), fullscr=True, allowGUI=False,
    monitor='testMonitor', color=[1,1,1], useFBO=True
)

#initialization of fixation
fixation = visual.TextStim(
    win = win,
    text = "+",
    color = (-1, -1, -1),
    autoLog = False
)

#initialization of blank
blank = visual.TextStim(
    win = win,
    text = "",
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

#initialization of incorrect response
incorrectR = visual.TextStim(
    win = win,
    text = "Incorrect",
    font = 'Arial',
    units = 'pix',
    height = 50,
    color = (-1, -1, -1),
)

#initialization of correct response
correctR = visual.TextStim(
    win = win,
    text = "Correct",
    font = 'Arial',
    units = 'pix',
    height = 50,
    color = (-1, -1, -1),
)

CONGRUENT = False
INCONGRUENT = True
MAN = True
NAT = False

frameRate = win.getActualFrameRate()                                              #gets FrameRate
framelength = win.monitorFramePeriod                                              #gets frameLength
expInfo['frameRate'] = frameRate

expInfo['block'] = -10
expInfo['trialType'] = ""
expInfo['order'] = -10
expInfo['conflict'] = ""
expInfo['image'] = ""
expInfo['Response'] = ""
expInfo['CorrectAns'] = False
expInfo['RespTime'] = -10.0

possKeys = [['M', 'm'],['Z', 'z']]
shuffle(possKeys)
expInfo['ManmadeKeys'] = [] #changed
expInfo['NaturalKeys'] = [] #changed

#creates directory and data files to be used to store data and analyze later on-------------------------------------------------------------------
pathExtension = "/data/" + expInfo['participant']

newpath = _thisDir + pathExtension
if not os.path.exists(newpath):
    os.makedirs(newpath)

fileName = "reRunPracticeSet" + expInfo['participant'] + ".csv"

with open(os.path.join(newpath, fileName), 'w', newline = '') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(list(expInfo.keys()))
    
    
#helper methods for use later on
def to_frames(t):                                                                 # Converts time to frames accounting for the computer's refresh rate (aka framelength); input is the desired time on screen, but the ouput is the closest multiple of the refresh rate
    return int(round(t / framelength))

imgDuration = to_frames(1)                                                           #image duration
ISI = to_frames(0.5)                                                                 #Inter Simulus Interval (feedback duration)
ITI = to_frames(5.5)                                                                 #Inter Trial Interval (blank duration)

def resize(x, y, newSize):                                                                 #resizes picture to all have same width of 800 px
    multiple = newSize/x
    new_y = y * multiple
    return [newSize, new_y]

def giveOpp(input):                                                                 #gives opposite to the input
    if (input == 'manmade'):
        return 'natural'
    elif (input == 'natural'):
        return 'manmade'

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
            

def runPracticeBlock(block, mSet, nSet, precode):
    setNum = expInfo['block'] % 9
    if setNum == 0:
        setNum = 9
    
    promptNeeded = False
    didCorr = True
    trialClock = core.Clock()
    allAns = []
    respTime = []
    
    i = 0
    
    for trial in block:
        expInfo['trialType'] = ""
        if trial == "m":
            currStim = mSet.pop(0)
            expInfo['trialType'] = "Manmade"
        else:
            currStim = nSet.pop(0)
            expInfo['trialType'] = "Natural"
        
        name = currStim[0]
        expInfo['image'] = name.split(".")[0]
        
        img = visual.ImageStim(                                                       #initializes image stimuli to be presented
            win = win,
            image = precode + name,
            units = 'pix',
            autoLog = False
        )
        
        theseKeys = event.getKeys(keyList=['M', 'm', 'Z', 'z'])
        event.clearEvents()
        
        frameN = 0
        trialClock.reset()
        while frameN < imgDuration:
            img.draw()
            win.flip()
            frameN += 1
        
        theseKeys = event.getKeys(keyList=['M', 'm', 'Z', 'z'], timeStamped = trialClock)
        print(theseKeys)
        
        corrAns = currStim[1]
        didCorr = False
        
        expInfo['Response'] = ""
        expInfo['CorrectAns'] = False
        expInfo['RespTime'] = -10.0
        
        if len(theseKeys) > 0:
            promptNeeded = False
            lastAns = theseKeys[-1]
            expInfo['Response'] = lastAns[0]
            if lastAns[0] in corrAns:
                didCorr = True
                allAns.append(didCorr)
                expInfo['CorrectAns'] = didCorr
                respTime.append(lastAns[1])
                expInfo['RespTime'] = lastAns[1]
            else:
                allAns.append(didCorr)
                expInfo['CorrectAns'] = didCorr
                respTime.append(-1.0)
                expInfo['RespTime'] = -1.0
        else:
            promptNeeded = True
            allAns.append(False)
            respTime.append(-2.0)
            expInfo['CorrectAns'] = didCorr
            expInfo['RespTime'] = -2.0
            
        if (promptNeeded):
            for frameN in range(ISI):
                prompt.draw()
                win.flip()
        elif (not(didCorr)):
            for frameN in range(ISI):
                incorrectR.draw()
                win.flip()
        else:
            for frameN in range(ISI):
                correctR.draw()
                win.flip()
        if i in [4, 10, 15]:
            for frameN in range(ITI):
                blank.draw()
                win.flip()
        
        with open(os.path.join(newpath, fileName), 'a', newline = '') as f:
            thewriter = csv.writer(f)
            thewriter.writerow(list(expInfo.values()))
        
        i += 1
        
    print(allAns)
    print(respTime)
    return allAns
        
#accessing variables predefined and randomized from the Practice Set-------------------------
varSaver = open(os.path.join(newpath, blockDataFileName), "r")
variables = varSaver.read()
variables = variables.split("\n")
specificVar = []
for var in variables:
    var = var.split(':')
    specificVar.append(var[1])
expInfo['ManmadeKeys'] = specificVar[0].strip('][').split(', ')
expInfo['ManmadeKeys'] = [i.strip('\'') for i in expInfo['ManmadeKeys']]

expInfo['NaturalKeys'] = specificVar[1].strip('][').split(', ')
expInfo['NaturalKeys'] = [i.strip('\'') for i in expInfo['NaturalKeys']]

imgPracticeSet = specificVar[3].strip('][').split(', ')
imgPracticeSet = [int(i) for i in imgPracticeSet]

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
    wrapWidth = 1100,
    autoLog = False
)
totalDirections.append(directionsTitle)

directions2 = visual.TextStim(
    win = win,
    text = "In this experiment, you will be presented a series of images.",
    color = (-1, -1, -1),
    pos = (-690, 290),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    font = 'Arial',
    height = 30,
    wrapWidth = 1100,
    autoLog = False
)
totalDirections.append(directions2)

directions3 = visual.TextStim(
    win = win,
    text = "On each trial, please categorize whether the image is manmade or natural, while ignoring any words that are overlaid on the images. \n\tPress " 
    + expInfo['NaturalKeys'][0] + "/" + expInfo['NaturalKeys'][1] + " if the image is NATURAL. \n\tPress " + expInfo['ManmadeKeys'][0] + "/" + expInfo['ManmadeKeys'][1] 
    + " if the image is MAN-MADE.",
    color = (-1, -1, -1),
    pos = (-690, 220),
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
    text = "Respond to each image as quickly as possible while still being accurate. You will have until the image disappears to make your response." + 
    " Always press the Z/z key with your LEFT index finger and the M/m key with your RIGHT index finger.",
    color = (-1, -1, -1),
    pos = (-690, 50),
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
    text = "Please stay focused during the experiment. You will first go through a practice run of 20 trials to get acclimated to the button responses." + 
    " You must get a total accuracy above 80% on this practice phase to proceed onto the main task.",
    color = (-1, -1, -1),
    pos = (-690, -80),
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
    text = "This task will take ~17.6 minutes and has 2 main blocks, and the practice block will take 1 minute. Press spacebar to begin the practice task.",
    color = (-1, -1, -1),
    pos = (-690, -210),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    font = 'Arial',
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)
totalDirections.append(directions6)

natKeys = visual.TextStim(
    win = win,
    text = "" + expInfo['NaturalKeys'][0] + "/" + expInfo['NaturalKeys'][1],
    color = 'red',
    pos = (-555, 150),
    units = "pix",
    alignHoriz = 'left',
    alignVert = 'top',
    bold = True,
    font = 'Arial',
    height = 30,
    wrapWidth = 1400,
    autoLog = False
)

manmKeys = visual.TextStim(
    win = win,
    text = "" + expInfo['ManmadeKeys'][0] + "/" + expInfo['ManmadeKeys'][1],
    color = 'red',
    pos = (-555, 116),
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

#initializing set of stimuli with classification predefined--------------------------------------

mStimuli = {}                                              #dictionary of all manmade stimuli - 272
nStimuli = {}                                              #dictionary of all natural stimuli - 272

for i in range(272):                                       #loops through 272 to initialize all stimuli elements 
    num = i + 1
    
    man = ['M' + str(num) + '.jpg', expInfo['ManmadeKeys'], 'manmade']
    mStimuli[i] = man
    
    nat = ['N' + str(num) + '.jpg', expInfo['NaturalKeys'], 'natural']
    nStimuli[i] = nat
    

manPracticeStimuli = []
natPracticeStimuli = []

for selected in imgPracticeSet:
    manPracticeStimuli.append(mStimuli[selected])
    natPracticeStimuli.append(nStimuli[selected])



#runs the practice block 
precode = "mtask/"                                                               #precode to access the set of images

practiceBlock = ['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n']
shuffle(practiceBlock)

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
            natKeys.draw()
            manmKeys.draw()
        if dirCount > 2:
            totalDirections[3].draw()
        if dirCount > 3:
            totalDirections[4].draw()
        if dirCount > 4:
            totalDirections[5].draw()
        win.flip()
        continueButton = event.getKeys(keyList=['space'])
    dirCount += 1

#begins practice task----------------------------------------------------------------------------------------------------------
countdown(3)

totalAns = runPracticeBlock(practiceBlock, manPracticeStimuli, natPracticeStimuli, precode)

count = 0
for ans in totalAns:
    if ans:
        count +=1 
accuracy = 100 * count / len(totalAns)
print(totalAns)
print("Your accuracy was %0.2f%%" % (accuracy))

accuracy1 = visual.TextStim(
    win = win,
    text = "Your accuracy on the practice was %0.2f%%. Call the experimenter over to continue." % (accuracy),
    font = 'Arial',
    alignHoriz = 'left',
    pos = (-690, 0),
    units = 'pix',
    bold = True,
    height = 30,
    wrapWidth = 1400,
    color = (-1, -1, -1),
)

#displays accuracy textStim at end of first block
event.clearEvents()
nextTaskKey = event.getKeys(keyList=['P', 'p'])
while (len(nextTaskKey) < 1):
    accuracy1.draw()
    win.flip()
    nextTaskKey = event.getKeys(keyList=['P', 'p'])

win.close()