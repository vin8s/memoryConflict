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
expInfo['ManmadeKeys'] = possKeys[0]
expInfo['NaturalKeys'] = possKeys[1]

#initialization of directions
directions = visual.TextStim(
    win = win,
    text = "Press " + expInfo['NaturalKeys'][0] + " when you see Natural images. \nPress " + expInfo['ManmadeKeys'][0] + " when you see Man-made images.",
    color = (-1, -1, -1),
    units = "pix",
    font = 'Arial',
    height = 30,
    wrapWidth = 1100,
    autoLog = False
)

#creates directory and data files to be used to store data and analyze later on
pathExtension = "/data/" + expInfo['participant']

newpath = _thisDir + pathExtension
if not os.path.exists(newpath):
    os.makedirs(newpath)

fileName = "PracticeSet" + expInfo['participant'] + ".csv"

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
        
        #img.size = resize(img.size[0], img.size[1], 800)
        """
        if i in [5, 11, 16]:
            if (promptNeeded):
                for frameN in range(ITI):
                    prompt.draw()
                    win.flip()
            else:
                for frameN in range(ITI):
                    blank.draw()
                    win.flip()
        else:
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
                    blank.draw()
                    win.flip()
        """
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
    #return [mSet, nSet]
        

#initializing set of stimuli with classification predefined--------------------------------------

mStimuli = {}                                              #dictionary of all manmade stimuli - 272
nStimuli = {}                                              #dictionary of all natural stimuli - 272

for i in range(272):                                       #loops through 272 to initialize all stimuli elements 
    num = i + 1
    
    man = ['M' + str(num) + '.jpg', expInfo['ManmadeKeys'], 'manmade']
    mStimuli[i] = man
    
    nat = ['N' + str(num) + '.jpg', expInfo['NaturalKeys'], 'natural']
    nStimuli[i] = nat
    
manSelectedStimuli = []                                       #list of the randomly selected manmade stimuli - 180
natSelectedStimuli = []                                       #list of the randomly selected natural stimuli - 180

imgRandShuffle = random.sample(range(len(mStimuli)), 180)     #randomly access 180 numbers from 272 to use in the loop to select the 180 stimuli
imgNotSelected = [i for i in range(272)]

for selected in imgRandShuffle:
    manSelectedStimuli.append(mStimuli[selected])
    natSelectedStimuli.append(nStimuli[selected])
    imgNotSelected.remove(selected)
    
shuffle(imgNotSelected)

varSaveFile = "blockData" + expInfo['participant'] + ".txt"
varSaver = open(os.path.join(newpath, varSaveFile), 'w')
varSaver.write("ManmadeKeys:" + str(expInfo['ManmadeKeys']))
varSaver.write("\nNaturalKeys:" + str(expInfo['NaturalKeys']))
varSaver.write("\nimgRandShuffle:" + str(imgRandShuffle))
varSaver.write("\nPracticeSet:" + str(imgNotSelected[0:10]))

manPracticeStimuli = []
natPracticeStimuli = []

for i in range(10):
    selected = imgNotSelected.pop(0)
    manPracticeStimuli.append(mStimuli[selected])
    natPracticeStimuli.append(nStimuli[selected])
    
varSaver.write("\nRemainingNotUsed:" + str(imgNotSelected))
varSaver.close()



#runs the practice block 
precode = "mtask/"                                                               #precode to access the set of images

practiceBlock = ['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',]
shuffle(practiceBlock)

for frameN in range(to_frames(5)):
    directions.draw()
    win.flip()

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
    text = "Your accuracy on the practice was %0.2f%%. \n\nCall the experimenter over to continue." % (accuracy),
    font = 'Arial',
    units = 'pix',
    height = 30,
    wrapWidth = 1000,
    color = (-1, -1, -1),
)

for frameN in range(to_frames(8)):
    accuracy1.draw()
    win.flip()

win.close()

