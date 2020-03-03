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
dataSetFileName = "dataSet" + expInfo['participant'] + ".csv"
blockDataFileName = "blockData" + expInfo['participant'] + ".txt"

#initializing window
win = visual.Window(
    size=(1280, 800), fullscr=False, allowGUI=False,
    monitor='testMonitor', color=[1,1,1], useFBO=True
)


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

#initialization of blank
blank = visual.TextStim(
    win = win,
    text = "",
    color = (-1, -1, -1),
    autoLog = False
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
expInfo['ManmadeKeys'] = []
expInfo['NaturalKeys'] = []

with open(os.path.join(pathExtension, dataSetFileName), 'w', newline = '') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(list(expInfo.keys()))

#helper methods for use later on
def to_frames(t):                                                                 # Converts time to frames accounting for the computer's refresh rate (aka framelength); input is the desired time on screen, but the ouput is the closest multiple of the refresh rate
    return int(round(t / framelength))

imgDuration = to_frames(1)                                                                #image duration
ISI = to_frames(0.5)                                                                      #Inter Stimulus Interval (feedback duration)
ITI = to_frames(5.5)                                                                      #Inter Trial Interval (blank duration

def resize(x, y, newSize):                                                                 #resizes picture to all have same width of 800 px
    multiple = newSize/x
    new_y = y * multiple
    return [newSize, new_y]

def giveOpp(input):
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


def giveOrder(block, lastExtra):
    trialOrder = []
    
    setNum = (block % 9)
    if setNum == 0:
        setNum = 9
        
    if setNum in [1, 2, 4]:
        trialOrder = ['m', 'n']
    elif setNum in [3, 5, 6, 7, 8]:
        trialOrder = ['m', 'm', 'n', 'n']
    elif setNum in [9]:
        trialOrder = ['m', 'm', 'm', 'n', 'n', 'n']
    
    newLastExtra = lastExtra
    if (setNum % 2 == 0):
        if lastExtra == 'm':
            trialOrder.append('n')
            newLastExtra = 'n'
        else:
            trialOrder.append('m')
            newLastExtra = 'm'
    
    shuffle(trialOrder)
    
    if block > 18:
        conflict = 'N'                                        #to indicate for natural stimuli during possible conflict
    else:
        conflict = 'M'                                         #to indicate for manmade stimuli during possible conflict
        
    if ((int(block/9))%2) == 0:
        conflict = conflict + 'I'                               #to indicate if congruent during possible conflict trial
    else:
        conflict = conflict + 'C'                               #to indicate if incongruent during possible conflict trial
    
    if setNum <= 3:
        trialOrder.insert(1, conflict)
    elif setNum <= 6:
        trialOrder.insert(2, conflict)
    else:
        trialOrder.insert(3, conflict)
    
    return trialOrder, newLastExtra
    
def runBlock(block, mSet, nSet, precode):
    setNum = expInfo['block'] % 9
    if setNum == 0:
        setNum = 9
        
    if setNum <= 3:
        startOrder = -1
    elif setNum <= 6:
        startOrder = -2
    else:
        startOrder = -3
        
    trialClock = core.Clock()
    allAns = []
    respTime = []
    
    needPrompt = False
    didCorr = True
    
    for trial in block:
        printWord = False
        expInfo['trialType'] = ""
        expInfo['order'] = startOrder
        expInfo['conflict'] = ""
        
        if trial == "m":
            currStim = mSet.pop(0)
            expInfo['trialType'] = "Manmade"
        elif trial == "n":
            currStim = nSet.pop(0)
            expInfo['trialType'] = "Natural"
        elif trial == 'MC':
            currStim = mSet.pop(0)
            printWord = True
            expInfo['trialType'] = "Manmade"
            expInfo['conflict'] = "Congruent"
        elif trial == 'NC':
            currStim = nSet.pop(0)
            printWord = True
            expInfo['trialType'] = "Natural"
            expInfo['conflict'] = "Congruent"
        elif trial == 'MI':
            currStim = mSet.pop(0)
            printWord = True
            expInfo['trialType'] = "Manmade"
            expInfo['conflict'] = "Incongruent"
        else:
            currStim = nSet.pop(0)
            printWord = True
            expInfo['trialType'] = "Natural"
            expInfo['conflict'] = "Incongruent"
        
        name = currStim[0]
        expInfo['image'] = name.split(".")[0]
        
        img = visual.ImageStim(                                                       #initializes image stimuli to be presented
            win = win,
            image = precode + name,
            units = 'pix',
            autoLog = False
        )
        
        #img.size = resize(img.size[0], img.size[1], 800)
        
        if (printWord):
            overlayText = (giveOpp(currStim[2].lower())).upper()
            if (trial in ['MC', 'NC']):
                overlayText = currStim[2].upper()
            word = visual.TextStim(
                win = win,
                text = overlayText,
                bold = False,
                font = 'Arial',
                units = 'pix',
                height = 100,
                color = (1, -1, -1)
            )
        """
        if (needPrompt):
            for frameN in range(ISI):
                prompt.draw()
                win.flip()
        elif (not(didCorr)):
            for frameN in range(ISI):
                incorrectR.draw()
                win.flip()
        else:
            for frameN in range(ISI):
                blank.draw()
                win.flip()
        theseKeys = event.getKeys(keyList=['M', 'm', 'Z', 'z'])
        event.clearEvents()
        """
        
        frameN = 0
        trialClock.reset()
        if (printWord):
            while frameN < to_frames(0.2):
                word.draw()
                win.flip()
                frameN += 1
            while frameN < imgDuration + to_frames(0.2):
                img.draw()
                word.draw()
                win.flip()
                frameN += 1
        else:
            while frameN < imgDuration:
                img.draw()
                win.flip()
                frameN += 1
        
        theseKeys = event.getKeys(keyList=['M', 'm', 'Z', 'z'], timeStamped = trialClock)
        
        corrAns = currStim[1]
        didCorr = False
        
        expInfo['Response'] = ""
        expInfo['CorrectAns'] = False
        expInfo['RespTime'] = -2.0
        
        if len(theseKeys) > 0:
            needPrompt = False
            lastAns = theseKeys[-1]
            expInfo['Response'] = lastAns[0]
            if lastAns[0] in corrAns:
                didCorr = True
                allAns.append(didCorr)
                respTime.append(lastAns[1])
                expInfo['CorrectAns'] = didCorr
                expInfo['RespTime'] = lastAns[1]
            else:
                allAns.append(didCorr)
                respTime.append(-2.0)
        else:
            needPrompt = True
            allAns.append(didCorr)
            respTime.append(-1.0)
            expInfo['CorrectAns'] = didCorr
            expInfo['RespTime'] = -1.0
            
        if (needPrompt):
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
                
        with open(os.path.join(pathExtension, dataSetFileName), 'a', newline = '') as file:
            thewriter = csv.writer(file)
            thewriter.writerow(list(expInfo.values()))
        
        startOrder += 1
        
    return [mSet, nSet, allAns]
        



#initializing variables predefined and randomized from the Practice Set-------------------------
varSaver = open(os.path.join(pathExtension, blockDataFileName), "r")
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

imgRandShuffle = specificVar[2].strip('][').split(', ')
imgRandShuffle = [int(i) for i in imgRandShuffle]

imgRemNotUsed = specificVar[4].strip('][').split(', ')
imgRemNotUsed = [int(i) for i in imgRemNotUsed]

#initialization of directions
directions = visual.TextStim(
    win = win,
    text = "Note that on the rest of the blocks, you may see a word overlaid on the images. You should ignore the word presented. \n\nAs a reminder: \nPress " + expInfo['NaturalKeys'][0] + " when you see Natural images. \nPress " + expInfo['ManmadeKeys'][0] + " when you see Man-made images.",
    color = (-1, -1, -1),
    font = 'Arial',
    units = 'pix',
    height = 30,
    wrapWidth = 1100,
    autoLog = False
)

#display directions
for frameN in range(to_frames(5)):
    directions.draw()
    win.flip()

#initializing set of stimuli with classification predefined--------------------------------------
mStimuli = {}                                              #dictionary of all manmade stimuli - 272
nStimuli = {}                                              #dictionary of all natural stimuli - 272

for i in range(272):                                       #loops through 272 to initialize all stimuli elements 
    num = i + 1
    
    man = ['M' + str(num) + '.jpg', expInfo['ManmadeKeys'], 'manmade']
    mStimuli[i] = man
    
    nat = ['N' + str(num) + '.jpg', expInfo['NaturalKeys'], 'natural']
    nStimuli[i] = nat
    
manSelectedStimuli = []                                       #dictionary of the randomly selected manmade stimuli - 180
natSelectedStimuli = []                                       #dictionary of the randomly selected natural stimuli - 180

for selected in imgRandShuffle:
    manSelectedStimuli.append(mStimuli[selected])
    natSelectedStimuli.append(nStimuli[selected])

#----------------------------------------------------------------------------------------------------------------

#develops block order by initially adding two trials of each of the 36 different blocks and then shuffling order
blockOrder = []
for i in range(36):
    blockOrder.append(i+1)
    blockOrder.append(i+1)
shuffle(blockOrder)

#equally distributes manmade and natural stimuli to the blocks in a pseudorandom manner
totalList = []
totalCombinedList = []

#print(blockOrder)
lastExtra = 'm'
for block in blockOrder:
    [tOrder, lastExtra] = giveOrder(block, lastExtra)
    totalList.append(tOrder)
    totalCombinedList.extend(tOrder)

varSaver = open(os.path.join(pathExtension, blockDataFileName), "a")
varSaver.write("\nblockOrder:" + str(blockOrder))
varSaver.write("\nimageOrder:" + str(totalCombinedList))
varSaver.close()


precode = "mtask/"                                                               #precode to access the set of images

#runs first block of 90
countdown(3)
totalImgCount = 0
totalAns = []
i = 0
while (totalImgCount < 180):
    expInfo['block'] = blockOrder[i]
    [manSelectedStimuli, natSelectedStimuli, setAns] = runBlock(totalList[i], manSelectedStimuli, natSelectedStimuli, precode)
    totalAns.extend(setAns)
    totalImgCount += len(totalList[i])
    for frameN in range(ITI):
        blank.draw()
        win.flip()
    i += 1

#calculates accuracy of first block to present to the participant
count = 0
for ans in totalAns:
    if ans:
        count +=1 
accuracy = 100 * count / len(totalAns)
print(totalAns)
print("Your accuracy was %0.2f%%" % (accuracy))

#initializes accuracy textStim for end of first block
accuracy1 = visual.TextStim(
    win = win,
    text = "Your accuracy was %0.2f%%. You may take a small break for two minutes and rest your eyes. \n\n As a reminder: \nPress %s when you see Natural images. \nPress %s when you see Man-made images. \n\nPress spacebar to continue to the second half." % (accuracy, expInfo['NaturalKeys'][0], expInfo['ManmadeKeys'][0]),
    font = 'Arial',
    units = 'pix',
    height = 30,
    wrapWidth = 1100,
    color = (-1, -1, -1),
)

#displays accuracy textStim at end of first block
event.clearEvents()
continueButton = event.getKeys(keyList=['space'])
while (len(continueButton) < 1):
    accuracy1.draw()
    win.flip()
    continueButton = event.getKeys(keyList=['space'])


#runs second block of 90
countdown(3)
while i < len(blockOrder):
    expInfo['block'] = blockOrder[i]
    [manSelectedStimuli, natSelectedStimuli, setAns] = runBlock(totalList[i], manSelectedStimuli, natSelectedStimuli, precode)
    totalAns.extend(setAns)
    for frameN in range(ITI):
        blank.draw()
        win.flip()
    i += 1

#calculates accuracy of complete experiment to present to the participant
count = 0
for ans in totalAns:
    if ans:
        count +=1 
accuracy = 100 * count / len(totalAns)
print(totalAns)
print("Your accuracy was %0.2f%%" % (accuracy))

#initializes textStim for end of experiment
accuracy2 = visual.TextStim(
    win = win,
    text = "Your accuracy across test blocks was %0.2f%%. You will now fill out a questionnaire. \n\nPlease press the spacebar to submit your data and move on to the questionnaire. Ask your experimenter to set up the questionnaire." % (accuracy),
    font = 'Arial',
    units = 'pix',
    height = 30,
    wrapWidth = 1100,
    color = (-1, -1, -1),
)

#displays textStim at end of experiment
event.clearEvents()
continueButton = event.getKeys(keyList=['space'])
while (len(continueButton) < 1):
    accuracy2.draw()
    win.flip()
    continueButton = event.getKeys(keyList=['space'])



win.close()

