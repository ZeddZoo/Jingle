####################
#NAME: ZIYI ZUO
#ANDREWID: ZIYIZUO
#SECTION: N
####################

import module_manager
import os
import time
import string
from Pattern import *
from Instruments import *
from Synthesizer import *
from Song import *
import pygame


####################

module_manager.review()

pygame.init()

size = (1080, 720)
screen = pygame.display.set_mode(size)

#ALL custom images created using piskel
background = pygame.image.load("BackGround.png")
playButton = pygame.image.load("Play.png")
playSongIcon = pygame.image.load("Play Small.png")
plusButton = pygame.image.load("Add Track.png")
exportButton = pygame.image.load("Export.png")
saveButton = pygame.image.load("Save.png")
# playButtonRect = playButton.get_rect()
backgroundRect = background.get_rect()
settingsIcon = pygame.image.load("Settings.png")
trashIcon = pygame.image.load("trash.png")
exit = pygame.image.load("doorOut.png")
currMode = "main menu"
#"drum pattern editor"#"song editor" #"main menu"
running = True
screenUncleared = True

pattGridsDrawn = False

marginX = 140
marginY = 60

#####
"""Import media files"""


icon = pygame.transform.scale(pygame.image.load("Logo.png").convert(),
                              (size[1] // 2, size[1] // 2))
titleFont = pygame.font.Font("Fipps-Regular.otf", 50)
controlFont = pygame.font.Font("DisposableDroidBB_ital.otf", 90)

controlFontLittle = pygame.font.Font("DisposableDroidBB_ital.otf", 60)
title = titleFont.render("Jingle", True, (255, 255, 255))
iconOffset = 128

####### IMPORT MEDIA #######
kick = pygame.transform.scale2x(pygame.image.load("Kick.png"))
hat = pygame.transform.scale2x(pygame.image.load("Hat.png"))
snare = pygame.transform.scale2x(pygame.image.load("Snare.png"))
clap = pygame.transform.scale2x(pygame.image.load("Clap.png"))
imageList = [kick, snare, hat, clap]
bracket = pygame.transform.scale2x(pygame.image.load("Bracket.png"))
############################

soundPlayer = pygame.mixer.Channel(0)

def getPatternCount(patternList):
    found = 0
    for instrument in range(len(patternList)):
        for bar in range(len(patternList[instrument])):
            if patternList[instrument][bar] is not None:
                found += 1
    return str(found + 1)

def playPattern(patternObject):
    if not pygame.mixer.get_busy():
        if isinstance(selectedPattern, DrumPattern):
            patternObject.exportAsPlaying()
        else:
            patternObject.exportAsPlaying(selectedSong.instrumentRack[selectedSong.selectedInstrument])
        nowPlaying = pygame.mixer.Sound("Now Playing.wav")
        soundPlayer.play(nowPlaying)

def playSong(songObject):
    if not pygame.mixer.get_busy():
        # if isinstance(selectedPattern, DrumPattern):
        #     songObject.exportAsNowPlaying()
        # else:
        #     songObject.exportAsNowPlaying(selectedSong.instrumentRack[selectedSong.selectedInstrument])
        songObject.exportAsNowPlaying()
        nowPlaying = pygame.mixer.Sound("Now Playing.wav")
        soundPlayer.play(nowPlaying)

def exportPattern(selectedPattern, selectedSong, position):
    if isinstance(selectedPattern, DrumPattern):
        selectedSong.soundList[selectedPattern.instrPos][position] = selectedPattern.export()
    else:
        selectedSong.soundList[selectedPattern.instrPos][position] = selectedPattern.export(selectedSong.instrumentRack[selectedSong.selectedInstrument])
    global currMode
    currMode = "song editor"
    global screenUncleared
    global pattGridsDrawn
    pattGridsDrawn = False
    screenUncleared = True

projectList = []

def projectLister(projectList):
    projList = []

    projectObjectList = projectList

    #From 112 notes
    def findFiles(projectList, path):
        if not os.path.isdir(path):
            if path.endswith("project.pyc"):
                projectList += [path]
        else:
            for newPath in os.listdir(path):
                findFiles(projectList, path + "\\" + newPath)
    def getProjectsFromDir(projectObjectList, projList):
        for objectDirectory in projList:
            file = open(objectDirectory, "rb")
            fileObject = pickle.load(file)
            if fileObject not in projectObjectList:
                projectObjectList.append(fileObject)

    # Many thanks to stackoverload for os.getcwd
    # (https://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python)
    findFiles(projList, os.getcwd())
    getProjectsFromDir(projectObjectList, projList)

projectLister(projectList)

selectedSong = None

projectRects = []

#Template from pygame documentation
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    #####################################################
    if currMode == "main menu":

        if screenUncleared:
            screen.blit(background, backgroundRect)
            screenUncleared = False

        iconRect = icon.get_rect().move(size[1] // 2,
                                        (size[0] - iconOffset) // 5)
        titleRect = title.get_rect().move(size[1] // 2 + 50, 50)

        if pygame.mouse.get_pressed()[0]:
            if iconRect.collidepoint(pygame.mouse.get_pos()):
                currMode = "FileSelector"
                screenUncleared = True

        screen.blit(icon, iconRect)
        screen.blit(title, titleRect)
        pygame.display.flip()

    if currMode == "FileSelector":

        if screenUncleared:
            screen.blit(background, backgroundRect)
            screenUncleared = False

        pygame.draw.line(screen, (255, 255, 255), (600, 10), (600, 620), 5)
        pygame.draw.line(screen, (255, 255, 255), (0, 620), (1080, 620), 5)
        pygame.draw.line(screen, (255, 0, 0), (600, 20), (600, 600), 1)
        pygame.draw.line(screen, (255, 0, 0), (20, 620), (1060, 620), 1)

        exitToMenuRect = pygame.Rect((20, 640), (64, 64))
        screen.blit(exit, exitToMenuRect)

        ##########LIST FILES##########
        statsBoxrect = pygame.Rect((600, 0), (480, 620))

        for project in range(len(projectList)):
            if len(projectList) >= 4:
                displayHeight = 570 // len(projectList)
            else:
                displayHeight = 140
            nameFont = pygame.font.Font("DisposableDroidBB_ital.otf", displayHeight // 5)
            nameRender = nameFont.render(projectList[project].songName, True, (255, 255, 255))
            nameRect = ((50, 50 + 155 * project), (600, displayHeight))
            pygame.draw.line(screen, (255, 255, 255), (50, 50 + 155 * project + displayHeight), (550, 50 + 155 * project + displayHeight), 1)
            if len(projectRects) < len(projectList):
                projectRects.append(pygame.Rect(nameRect))
            screen.blit(nameRender, nameRect)

        continueBreaking = False

        if selectedSong is None:
            goingForward = False
            newSongRect = pygame.Rect((620, 400), (400, 100))
            newSongText = controlFontLittle.render("Create New Song", True, (255, 255, 255))
            screen.blit(newSongText, newSongRect)
            if pygame.mouse.get_pressed()[0]:
                if exitToMenuRect.collidepoint(pygame.mouse.get_pos()):
                    currMode = "main menu"
                    screenUncleared = True
                if newSongRect.collidepoint(pygame.mouse.get_pos()):
                    songName = "hello world"
                    tempo = "112"
                    selectedBox = "name"

                    while True:

                        if len(songName) > 18:
                            nameEntryFontSize = 65 - len(songName)

                        else:
                            nameEntryFontSize = 60
                        tempoEntryFontSize = 60

                        nameEntryFont = pygame.font.Font("DisposableDroidBB_ital.otf", nameEntryFontSize)
                        tempoEntryFont = pygame.font.Font("DisposableDroidBB_ital.otf", tempoEntryFontSize)

                        namePopupRect = ((200, 100), (680, 420))
                        pygame.draw.rect(screen, (50, 50, 50), namePopupRect)
                        nameBox = ((225, 175), (630, 50))
                        pygame.draw.rect(screen, (255, 255, 255), nameBox)
                        tempoBox = ((225, 325), (630, 50))
                        pygame.draw.rect(screen, (255, 255, 255), tempoBox)
                        songNameRender = nameEntryFont.render(songName, True, (0, 0, 0))
                        songTempoRender = tempoEntryFont.render(tempo, True, (0, 0, 0))

                        namePromptBox = ((225, 125), (630, 50))
                        tempoPromptBox = ((225, 275), (630, 50))

                        namePromptText = tempoEntryFont.render("Project Name: (25 char.)", True, (255, 255, 255))
                        tempoPromptText = tempoEntryFont.render("Project Tempo: (50 - 500)", True, (255, 255, 255))

                        if pygame.mouse.get_pressed()[0]:  # Check if left mouse pressed
                            mouseLocation = pygame.mouse.get_pos()
                            if pygame.Rect(nameBox).collidepoint(mouseLocation):
                                selectedBox = "name"
                            elif pygame.Rect(tempoBox).collidepoint(mouseLocation):
                                selectedBox = "tempo"

                        #Draw the selection box
                        if selectedBox == "name":
                            pygame.draw.rect(screen, (0, 0, 0), nameBox, 4)
                        else:
                            pygame.draw.rect(screen, (0, 0, 0), tempoBox, 4)


                        screen.blit(namePromptText, namePromptBox)
                        screen.blit(tempoPromptText, tempoPromptBox)

                        screen.blit(songNameRender, nameBox)
                        screen.blit(songTempoRender, tempoBox)

                        playButtonRect = ((490, 400), (100, 100))
                        screen.blit(playButton, playButtonRect)

                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if selectedBox == "name":
                                    if event.key == pygame.K_BACKSPACE:
                                        songName = songName[:-1]
                                    else:
                                        songName += pygame.key.name(event.key)
                                        if len(songName) >= 25:
                                            songName = songName[:-1]
                                else:
                                    if event.key == pygame.K_BACKSPACE:
                                        tempo = tempo[:-1]
                                    elif pygame.key.name(event.key) in string.digits:
                                        if (tempo == "" or int(tempo) == 0) and pygame.key.name(event.key) == "0":
                                            continue
                                        tempo += pygame.key.name(event.key)
                                        if int(tempo) > 500:
                                            tempo = ""

                        if pygame.mouse.get_pressed()[0]:
                            time.sleep(.1)
                            if pygame.Rect(playButtonRect).collidepoint(pygame.mouse.get_pos()) \
                                    and tempo != "":
                                selectedSong = Song(songName, int(tempo))
                                continueBreaking = True
                                goingForward = True
                                break

                            elif not pygame.Rect(namePopupRect).collidepoint(pygame.mouse.get_pos()):
                                screenUncleared = True
                                break

                        pygame.display.flip()

                    if goingForward:
                        patternList = selectedSong.patternList
                        instrumentRack = selectedSong.instrumentRack
                        songList = selectedSong.soundList

                        currMode = "song editor"
                        selectedPattern = None
                        screenUncleared = True

        else:
            openProjectRect = pygame.Rect((800, 400), (200, 200))
            screen.blit(playButton, openProjectRect)

            fileName = controlFont.render(selectedSong.songName, True, (255, 255, 255))
            tempoName = controlFontLittle.render(str(selectedSong.tempo), True, (255, 255, 255))

            fileNameBox = pygame.Rect((620, 150), (100, 50))
            tempoNameBox = pygame.Rect((650, 250), (100, 50))
            screen.blit(fileName, fileNameBox)
            screen.blit(tempoName, tempoNameBox)

            if pygame.mouse.get_pressed()[0]:
                if openProjectRect.collidepoint(pygame.mouse.get_pos()):
                    patternList = selectedSong.patternList
                    instrumentRack = selectedSong.instrumentRack
                    songList = selectedSong.soundList
                    currMode = "song editor"
                    selectedPattern = None
                    screenUncleared = True



        pygame.display.flip()


        if pygame.mouse.get_pressed()[0] and not continueBreaking:
            projUnfound = True
            for rect in range(len(projectRects)):
                if projectRects[rect].collidepoint(pygame.mouse.get_pos()):
                    selectedSong = projectList[rect]
                    selectedSongIndex = rect
                    screenUncleared = True
                    projUnfound = False
            if projUnfound and not statsBoxrect.collidepoint(pygame.mouse.get_pos()):
                selectedSong = None
                screenUncleared = True


    if currMode == "song editor":

        if screenUncleared:
            screen.blit(background, backgroundRect)
            screenUncleared = False

        ######################Startup Settings#############################
        instrumentHeight = 620 // 4
        barDivision = (1080 - 250) // 4

        if len(instrumentRack) == 0:
            #Load default instruments
            instrumentRack.append(DrumKit("Drum Kit"))
            instrumentRack.append(Lead("Lead", 440))
            instrumentRack.append(Lead("Bass", 110))
            instrumentRack[2].synthesizer.getScale()
            instrumentRack[1].synthesizer.getScale()
            selectedSong.selectedInstrument = 0
        pygame.draw.line(screen, (255, 255, 255), (250, 10), (250, 620), 5)
        pygame.draw.line(screen, (255, 255, 255), (0, 620), (1080, 620), 5)
        pygame.draw.line(screen, (255, 0, 0), (250, 20), (250, 600), 1)
        pygame.draw.line(screen, (255, 0, 0), (20, 620), (1060, 620), 1)
        pygame.display.flip()

        for barNum in range(1, 4):
            pygame.draw.line(screen, (255, 255, 255), (250 + barNum * barDivision, 20),
                             (250 + barNum * barDivision, 600))
        ###################################################################

        unselectedColor = (100, 100, 100)
        selectedColor = (255, 255, 0)

        if len(selectedSong.rectList) != len(selectedSong.instrumentRack):
            for instrument in range(len(instrumentRack)):
                instrumentPatterns = []
                for pattern in range(len(patternList[instrument])):
                    patternRect = ((265 + pattern * barDivision, instrument * instrumentHeight + 20),
                                   (barDivision - 25, instrumentHeight - 30))
                    instrumentPatterns.append(pygame.Rect(patternRect))
                selectedSong.rectList.append(instrumentPatterns)

        for instrument in range(len(instrumentRack)):
            for pattern in range(len(patternList[instrument])):
                if patternList[instrument][pattern] is None:
                    # pygame.draw.rect(screen, unselectedColor, selectedSong.rectList[instrument][pattern])
                    addRect = ((265 + pattern * barDivision + barDivision // 2 - 45,
                                instrument * instrumentHeight + 20 + instrumentHeight // 2 - 50), (50, 50))
                    screen.blit(plusButton, addRect)
                    if pygame.mouse.get_pressed()[0]:
                        if pygame.Rect(addRect).collidepoint(pygame.mouse.get_pos()):

                            patternName = getPatternCount(selectedSong.patternList)

                            while True:

                                breakLoop = False

                                if len(selectedSong.songName) > 18:
                                    nameEntryFontSize = 65 - len(patternName)

                                else:
                                    nameEntryFontSize = 60


                                nameEntryFont = pygame.font.Font("DisposableDroidBB_ital.otf", nameEntryFontSize)

                                namePopupRect = ((200, 100), (680, 420))
                                pygame.draw.rect(screen, (50, 50, 50), namePopupRect)
                                nameBox = ((225, 175), (630, 50))
                                pygame.draw.rect(screen, (255, 255, 255), nameBox)
                                patternNameRender = nameEntryFont.render(patternName, True, (0, 0, 0))

                                namePromptBox = ((225, 125), (630, 50))

                                namePromptText = nameEntryFont.render("Pattern Name: (25 char.)", True,
                                                                       (255, 255, 255))

                                screen.blit(namePromptText, namePromptBox)

                                screen.blit(patternNameRender, nameBox)

                                playButtonRect = ((490, 400), (100, 100))
                                screen.blit(playButton, playButtonRect)

                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_BACKSPACE:
                                            patternName = patternName[:-1]
                                        elif event.key == pygame.K_ESCAPE:
                                            breakLoop = True
                                        else:
                                            patternName += pygame.key.name(event.key)
                                            if len(selectedSong.songName) >= 25:
                                                patternName = patternName[:-1]

                                if pygame.mouse.get_pressed()[0]:
                                    time.sleep(.5)
                                    if pygame.Rect(playButtonRect).collidepoint(pygame.mouse.get_pos()) \
                                            and patternName != "":
                                        instrumentPatternToCreate = selectedSong.instrumentRack[instrument]
                                        print(instrumentPatternToCreate)
                                        if isinstance(instrumentPatternToCreate, DrumKit):
                                            selectedPattern = DrumPattern(patternName, 4, pattern, selectedSong.tempo, instrument)
                                            patternList[instrument][pattern] = selectedPattern
                                            currMode = "drum pattern editor"
                                            selectedSong.selectedInstrument = instrument
                                        elif isinstance(instrumentPatternToCreate, Lead):
                                            selectedPattern = SynthPattern(patternName, 4, pattern, selectedSong.tempo,
                                                                          instrument)
                                            patternList[instrument][pattern] = selectedPattern
                                            currMode = "synth pattern editor"
                                            selectedSong.selectedInstrument = instrument
                                            screenUncleared = True
                                        break
                                    # elif not pygame.Rect(namePopupRect).collidepoint(pygame.mouse.get_pos()):
                                    #     screenUncleared = True
                                    #     break

                                if breakLoop:
                                    screenUncleared = True
                                    break

                                pygame.display.flip()

                    pygame.display.flip()
                else:
                    pass
                    # pygame.draw.rect(screen, selectedColor, selectedSong.rectList[instrument][pattern])

                    #Draw the name rect

                if isinstance(patternList[instrument][pattern], Pattern):
                    # pygame.draw.rect(screen, selectedColor, selectedSong.rectList[instrument][pattern])
                    text = patternList[instrument][pattern].name
                    patternNameRect = ((250 + pattern * barDivision + barDivision // 2 - 5 * len(text),
                                   instrument * instrumentHeight + 20 + instrumentHeight // 2 - 64), (64, 64))
                    patternNameRenderation = pygame.font.Font("DisposableDroidBB_ital.otf", 60 // int(len(text) ** .5)).render(text, True, (255, 255, 255))
                    screen.blit(patternNameRenderation, patternNameRect)
                    deleteRect = ((280 + pattern * barDivision + barDivision // 2,
                                   instrument * instrumentHeight + 20 + instrumentHeight // 2 - 16), (64, 64))
                    newSettingsRect = ((((280 - 64 + pattern * barDivision + barDivision // 2,
                                   instrument * instrumentHeight + 20 + instrumentHeight // 2 - 16), (64, 64))))
                    screen.blit(trashIcon, deleteRect)
                    screen.blit(settingsIcon, newSettingsRect)
                    if pygame.mouse.get_pressed()[0]:
                        position = pygame.mouse.get_pos()
                        if pygame.Rect(deleteRect).collidepoint(position):
                            deleting = True
                            while deleting:
                                deleteConfirmRect = ((200, 100), (680, 420))
                                pygame.draw.rect(screen, (50, 50, 50), deleteConfirmRect)
                                doubleCheckFont = pygame.font.Font("DisposableDroidBB_ital.otf", 55)
                                deleteRender = doubleCheckFont.render("Delete this pattern?", True, (255, 255, 255))
                                prompt = doubleCheckFont.render("y -> Delete    n -> Cancel", True, (255, 255, 255))
                                deleteCheckRect = pygame.Rect((((220, 200), (680, 100))))
                                deletePromptRect = pygame.Rect((((220, 300), (680, 100))))

                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_y:
                                            selectedSong.patternList[instrument][pattern] = None
                                            selectedSong.soundList[instrument][pattern] = selectedSong.silence[:selectedSong.secondsPerBar]
                                            deleting = False
                                            screenUncleared = True
                                            break
                                        elif event.key == pygame.K_n:
                                            print('ok')
                                            deleting = False
                                            screenUncleared = True
                                            break

                                screen.blit(deleteRender, deleteCheckRect)
                                screen.blit(prompt, deletePromptRect)
                                pygame.display.flip()

                        elif pygame.Rect(newSettingsRect).collidepoint(position):
                            instrumentPatternToCreate = selectedSong.instrumentRack[instrument]
                            if isinstance(instrumentPatternToCreate, DrumKit):
                                selectedPattern = patternList[instrument][pattern]
                                currMode = "drum pattern editor"
                                selectedSong.selectedInstrument = instrument
                            elif isinstance(instrumentPatternToCreate, Lead):
                                selectedPattern = patternList[instrument][pattern]
                                currMode = "synth pattern editor"
                                selectedSong.selectedInstrument = instrument
                            screenUncleared = True



                        elif pygame.Rect(newSettingsRect).collidepoint(position):
                            print("ouch")

        exportRect = ((20, 640), (64, 64))
        screen.blit(exportButton, exportRect)

        playSongRect = ((92, 640), (64, 64))
        screen.blit(playSongIcon, playSongRect)

        saveSongRect = ((164, 640), (64, 64))
        screen.blit(saveButton, saveSongRect)

        exitToFileSelectRect = pygame.Rect((1080 - 20 - 64, 640), (64, 64))
        screen.blit(exit, exitToFileSelectRect)

        if pygame.mouse.get_pressed()[0]:
            if pygame.Rect(exportRect).collidepoint(pygame.mouse.get_pos()):
                selectedSong.exportSong()
                while True:
                    exportingFont = pygame.font.Font("DisposableDroidBB_ital.otf", 76)
                    exportPopUpRect = ((200, 100), (680, 420))
                    exportBox = ((250, 310), (680, 420))
                    pygame.draw.rect(screen, (255, 50, 50), exportPopUpRect)
                    exportingRender = exportingFont.render("Project Exported!", True, (255, 255, 255))
                    screen.blit(exportingRender, exportBox)
                    pygame.display.flip()
                    time.sleep(2)
                    screenUncleared = True
                    break
            if pygame.Rect(playSongRect).collidepoint(pygame.mouse.get_pos()):
                playSong(selectedSong)
                while pygame.mixer.get_busy():  #So you can't change the song while it's playing
                    continue
            if pygame.Rect(saveSongRect).collidepoint(pygame.mouse.get_pos()):
                selectedSong.saveSong()
                while True:
                    exportingFont = pygame.font.Font("DisposableDroidBB_ital.otf", 76)
                    exportPopUpRect = ((200, 100), (680, 420))
                    exportBox = ((250, 310), (680, 420))
                    pygame.draw.rect(screen, (255, 50, 50), exportPopUpRect)
                    exportingRender = exportingFont.render("Project Saved!", True, (255, 255, 255))
                    screen.blit(exportingRender, exportBox)
                    pygame.display.flip()
                    time.sleep(2)
                    screenUncleared = True
                    break
            if pygame.Rect(exitToFileSelectRect).collidepoint(pygame.mouse.get_pos()):
                currMode = "FileSelector"
                # projectLister(projectList)
                screenUncleared = True


        for instrument in range(4):
            if instrument < len(instrumentRack):
                nameFontSize = 300 // len(instrumentRack[instrument].name)
                nameFont = pygame.font.Font("DisposableDroidBB.otf", nameFontSize)
                pygame.draw.line(screen, (255, 255, 255), (20, (instrument + 1) * instrumentHeight),
                                 (1080, (instrument + 1) * instrumentHeight), 2)
                nameRect = ((40, instrument * instrumentHeight + 10), (100, 50))
                nameText = nameFont.render(instrumentRack[instrument].name, True, (255, 255, 255))
                screen.blit(nameText, nameRect)
                settingsRect = ((40, instrument * instrumentHeight + 80), (50, 50))
                screen.blit(settingsIcon, settingsRect)

                if pygame.mouse.get_pressed()[0] and pygame.Rect(settingsRect).collidepoint(pygame.mouse.get_pos())\
                        and not isinstance(instrumentRack[instrument], DrumKit):
                    editing = True
                    oscList = []
                    oscNameList = []
                    oscFreqList = []
                    oscFreqNameList = []
                    settingsFont = pygame.font.Font("DisposableDroidBB_ital.otf", 40)
                    for osc in range(3):
                        oscList.append(((250 + osc * 150, 200), (100, 40)))
                        oscNameList.append(((250 + osc * 150, 150), (100, 40)))
                        oscFreqNameList.append(((250 + osc * 150, 300), (100, 40)))
                        oscFreqList.append(((250 + osc * 150, 350), (100, 40)))


                    while editing:

                        editRect = pygame.Rect((200, 100), (680, 420))
                        pygame.draw.rect(screen, (50, 50, 50), editRect)

                        for osc in range(len(oscList)):
                            pygame.draw.rect(screen, (255, 255, 255), oscList[osc])
                            pygame.draw.rect(screen, (255, 255, 255), oscFreqList[osc])
                            oscName = settingsFont.render("osc " + str(osc + 1), True, (255, 255, 255))
                            oscState = " " + instrumentRack[instrument].synthesizer.waveForms[osc]
                            oscStateRender = settingsFont.render(oscState, True, (0, 0, 0))
                            oscFreqState = " %d" % (instrumentRack[instrument].synthesizer.freqList[osc])
                            oscFreqStateRender = settingsFont.render(oscFreqState, True, (0, 0, 0))
                            oscFreq = settingsFont.render("freq:", True, (255, 255, 255))
                            screen.blit(oscFreq, oscFreqNameList[osc])
                            screen.blit(oscFreqStateRender, oscFreqList[osc])
                            screen.blit(oscName, oscNameList[osc])
                            screen.blit(oscStateRender, oscList[osc])

                        playButtonRect = ((720, 250), (100, 100))
                        screen.blit(playButton, playButtonRect)

                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONUP:
                                position = pygame.mouse.get_pos()
                                for osc in range(len(oscList)):
                                    if pygame.Rect(oscList[osc]).collidepoint(position):
                                        waveFormList = ["sine", "tri", "sqr", "saw"]
                                        waveFormRects = []
                                        for waveForm in range(len(waveFormList)):
                                            waveFormRects.append(pygame.Rect(((252 + osc * 150, 202 + waveForm * 50), (96, 46))))
                                        selected = True

                                        while selected:

                                            dropDownBox = pygame.Rect((250 + osc * 150, 200), (100, 200))
                                            pygame.draw.rect(screen, (255, 255, 255), dropDownBox)
                                            for waveForm in range(len(waveFormList)):
                                                word = settingsFont.render(" " + waveFormList[waveForm], True, (0, 0, 0))
                                                screen.blit(word, waveFormRects[waveForm])

                                            for event in pygame.event.get():
                                                if event.type == pygame.MOUSEBUTTONUP:
                                                    position = pygame.mouse.get_pos()
                                                    for waveForm in range(len(waveFormRects)):
                                                        if waveFormRects[waveForm].collidepoint(position):
                                                            instrumentRack[instrument].synthesizer.waveForms[osc] = waveFormList[waveForm]
                                                            selected = False
                                                    selected = False


                                            pygame.display.flip()

                                    elif pygame.Rect(oscFreqList[osc]).collidepoint(position):
                                        selected = True
                                        freqString = "%d" % (instrumentRack[instrument].synthesizer.freqList[osc])

                                        while selected:
                                            pygame.draw.rect(screen, (255, 255, 255), oscFreqList[osc])
                                            word = settingsFont.render(freqString, True, (255, 0, 0))
                                            screen.blit(word, oscFreqList[osc])

                                            for event in pygame.event.get():
                                                if event.type == pygame.KEYDOWN:
                                                    if event.key == pygame.K_BACKSPACE and len(freqString) > 0:
                                                        freqString = freqString[:-1]
                                                    elif pygame.key.name(event.key) in string.digits:
                                                        freqString += pygame.key.name(event.key)
                                                        if len(freqString) > 4:
                                                            freqString = freqString[:-1]
                                                    elif (event.key == pygame.K_RETURN) and int(freqString) > 39:
                                                        instrumentRack[instrument].synthesizer.freqList[osc] = int(freqString)
                                                        print(instrumentRack[instrument].synthesizer.freqList)
                                                        selected = False


                                            pygame.display.flip()

                                if pygame.Rect(playButtonRect).collidepoint(position):
                                    instrumentRack[instrument].synthesizer.getScale()
                                    editing = False
                                    screenUncleared = True

                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                position = pygame.mouse.get_pos()
                                if not editRect.collidepoint(position):
                                    editing = False
                                    screenUncleared = True

                        pygame.display.flip()

            else:
                addInstrRect = pygame.Rect(((70, (instrument + .25) * instrumentHeight + 10), (64, 64)))
                screen.blit(plusButton, addInstrRect)
                if pygame.mouse.get_pressed()[0]:
                    if addInstrRect.collidepoint(pygame.mouse.get_pos()):
                        addingInstr = True
                        instrName = "Pat. Name"
                        selectedInstrBox = "drumBox"
                        instrBaseFreq = 440

                        while addingInstr:

                            addInstrBoxRect = pygame.Rect((200, 100), (680, 420))
                            pygame.draw.rect(screen, (50, 50, 50), addInstrBoxRect)
                            nameInputBox = ((250, 280), (580, 70))
                            pygame.draw.rect(screen, (255, 255, 255), nameInputBox)
                            appendInstrBox = pygame.Rect((540 - 64, 390), (64, 64))
                            screen.blit(playButton, appendInstrBox)

                            drumBox = pygame.Rect((250, 150), (240, 60))
                            synthBox = pygame.Rect((250 + 290, 150), (240, 60))

                            drumBoxTextRender = controlFontLittle.render("Drums", True, (255, 255, 255))
                            synthBoxTextRender = controlFontLittle.render("Synths", True, (255, 255, 255))

                            instrNameRender = controlFontLittle.render(" " + instrName, True, (0, 0, 0))

                            screen.blit(drumBoxTextRender, drumBox)
                            screen.blit(synthBoxTextRender, synthBox)
                            screen.blit(instrNameRender, nameInputBox)

                            if selectedInstrBox == "drumBox":
                                pygame.draw.rect(screen, (255, 255, 0), drumBox, 3)
                            else:
                                pygame.draw.rect(screen, (255, 255, 0), synthBox, 3)

                            for event in pygame.event.get():

                                if event.type == pygame.MOUSEBUTTONUP:
                                    position = pygame.mouse.get_pos()
                                    if drumBox.collidepoint(position):
                                        selectedInstrBox = "drumBox"
                                    elif synthBox.collidepoint(position):
                                        selectedInstrBox = "synthBox"
                                    elif appendInstrBox.collidepoint(position):
                                        if selectedInstrBox == "drumBox":
                                            instrumentRack.append(DrumKit(instrName))
                                            addingInstr = False
                                            screenUncleared = True
                                        else:
                                            promptingFreq = True

                                            while promptingFreq:
                                                bfPromptBox = pygame.Rect((250, 150), (580, 320))
                                                pygame.draw.rect(screen, (50, 50, 50), bfPromptBox)
                                                pygame.draw.rect(screen, (255, 255, 255), bfPromptBox, 5)
                                                bfBox = pygame.Rect((280, 200), (500, 70))
                                                pygame.draw.rect(screen, (255, 255, 255), bfBox)
                                                bfRender = controlFontLittle.render(str(instrBaseFreq) + "Hz", True, (0, 0, 0))

                                                screen.blit(bfRender, bfBox)

                                                for event in pygame.event.get():
                                                    if event.type == pygame.KEYDOWN:
                                                        if event.key == pygame.K_BACKSPACE:
                                                            instrBaseFreq //= 10
                                                        elif event.key == pygame.K_RETURN:
                                                            screenUncleared = True
                                                            promptingFreq = False

                                                        elif pygame.key.name(event.key) in string.digits:
                                                            instrBaseFreq = instrBaseFreq * 10 + int(pygame.key.name(event.key))

                                                pygame.display.flip()

                                            print(patternList)
                                            print(instrumentRack)

                                            instrumentRack.append(Lead(instrName, instrBaseFreq))
                                            instrumentRack[-1].synthesizer.getScale()
                                            addingInstr = False
                                            screenUncleared = True
                                            print(patternList)
                                            print(instrumentRack)

                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_BACKSPACE:
                                        instrName = instrName[:-1]
                                    elif pygame.key.name(event.key) in (string.digits + string.ascii_letters):
                                        instrName += pygame.key.name(event.key)
                                        if len(instrName) > 10:
                                            instrName = instrName[:-1]

                            pygame.display.flip()

            pygame.display.flip()


    if currMode == "drum pattern editor":

        if screenUncleared:
            screen.blit(background, backgroundRect)
            screenUncleared = False

        offSetX = 200
        offSetY = 200

        if not pattGridsDrawn:
            instrHeight = (size[1]) // (selectedPattern.instrCount * 6)
            beatWidth = (size[0] - 300) // (selectedPattern.barCount * 4)

            # pianoRoll = pygame.Surface((size[0] - 2 * marginX, size[1] - 2 * marginY))
            pianoRoll = pygame.Surface(size)
            pianoRollRects = []


            for instrument in range(selectedPattern.instrCount):
                instrRow = []
                for beat in range(selectedPattern.barCount * 4):
                    beatrect = ((offSetX + beat*beatWidth, offSetY + instrument * instrHeight + 50 * instrument),
                                (beatWidth, instrHeight))
                    if beat % 4 == 0:
                        width = 3
                    else: width = 1
                    isFilled = (selectedPattern.pianoRoll[beat][instrument] == 1)
                    color = (255, 255, 255)
                    if isFilled:
                        color = (255, 255, 0)
                    instrRow.append(pygame.draw.rect(pianoRoll, color, beatrect, width))


                pianoRollRects.append(instrRow)

            pattGridsDrawn = True

            # Play
            playBracketRect = pygame.Rect((offSetX, 2.75 * offSetY), (200, 100))
            playRect = pygame.Rect((offSetX + 50, 2.9 * offSetY - 10), (200, 100))
            playText = controlFont.render("PLAY", True, (255, 255, 255))


            # EXPORT
            exportBracketRect = pygame.Rect((3.25 * offSetX, 2.75 * offSetY), (200, 100))
            exportRect = pygame.Rect((3.25 * offSetX + 50, 2.9 * offSetY), (200, 100))
            exportText = controlFontLittle.render("EXPORT", True, (255, 255, 255))


            screen.blit(pianoRoll, screen.get_rect())

        if pygame.mouse.get_pressed()[0]: #Check if left mouse pressed
            mouseLocation = pygame.mouse.get_pos()
            unentered = True
            for row in range(len(pianoRollRects)):
                for col in range(len(pianoRollRects[row])):
                    if pianoRollRects[row][col].collidepoint(mouseLocation):
                        beatrect = ((offSetX + col * beatWidth, offSetY + row * instrHeight + 50 * row),
                                    (beatWidth, instrHeight))
                        if col % 4 == 0:
                            width = 3
                        else:
                            width = 1
                        pianoRollRects[row][col] = (pygame.draw.rect(pianoRoll, (255, 255, 0), beatrect, width))
                        selectedPattern.addNote(col, row)
            mouseLocation = pygame.mouse.get_pos()
            if playBracketRect.collidepoint(mouseLocation) and unentered:
                print("Now Playing...")
                playPattern(selectedPattern)
                unentered = False
                while pygame.mixer.get_busy():
                    continue
            if exportBracketRect.collidepoint(mouseLocation) and unentered:
                print("Now Exporting...")
                screen.blit(background, backgroundRect)
                pygame.display.flip()
                exportPattern(selectedPattern, selectedSong, selectedPattern.patternPos)
                selectedPattern = None
                unentered = False
                continue

        elif pygame.mouse.get_pressed()[2]: #Right click
            mouseLocation = pygame.mouse.get_pos()
            for row in range(len(pianoRollRects)):
                for col in range(len(pianoRollRects[row])):
                    if pianoRollRects[row][col].collidepoint(mouseLocation):
                        beatrect = ((offSetX + col * beatWidth, offSetY + row * instrHeight + 50 * row),
                                    (beatWidth, instrHeight))
                        if col % 4 == 0:
                            width = 3
                        else:
                            width = 1
                        pianoRollRects[row][col] = (pygame.draw.rect(pianoRoll, (255, 255, 255), beatrect, width))
                        selectedPattern.delNote(col, row)

        screen.blit(pianoRoll, screen.get_rect())

        for instrument in range(selectedPattern.instrCount):
            iconRect = pygame.Rect((offSetX // 2, offSetY - 30 + 3 * instrument * instrHeight), (64, 64))
            screen.blit(imageList[instrument], iconRect)

        screen.blit(bracket, playBracketRect)
        screen.blit(playText, playRect)

        screen.blit(bracket, exportBracketRect)
        screen.blit(exportText, exportRect)

        pygame.display.flip()

    if currMode == "synth pattern editor":
        if screenUncleared:
            screen.blit(background, backgroundRect)
            screenUncleared = False
            pattGridsDrawn = False

        if not pattGridsDrawn:
            pitchIndexHeight = 20
            beatWidth = 50

            pitchRowRects = []

            offSetX = 200
            offSetY = 150


            for pitch in range(len(selectedSong.instrumentRack[selectedSong.selectedInstrument].synthesizer.sampleList)):
                beatList = []
                for beat in range(len(selectedPattern.pianoRoll)):
                    octaveNumber = (len(selectedSong.instrumentRack[selectedSong.selectedInstrument].synthesizer.sampleList) - pitch - 1) // 12
                    beatRect = pygame.Rect((offSetX + beat * beatWidth, offSetY + pitch * pitchIndexHeight - 50 * octaveNumber), (beatWidth, pitchIndexHeight))
                    if beat % 4 == 0:
                        width = 3
                    else: width = 1
                    if pitch % 12 == 0:
                        freqFont = pygame.font.Font("DisposableDroidBB_ital.otf", 30)
                        baseFreq = selectedSong.instrumentRack[selectedSong.selectedInstrument].synthesizer.baseFreq
                        renderedFreq = freqFont.render(str((2 ** octaveNumber) * baseFreq), True, (255, 255, 255))
                        baseFreqRect = ((150, offSetY + pitch * pitchIndexHeight - 50 * octaveNumber), (beatWidth, pitchIndexHeight))
                        screen.blit(renderedFreq, baseFreqRect)
                    beatList.append(beatRect)

                    isFilled = (selectedPattern.pianoRoll[beat][pitch] == 1)
                    color = (255, 255, 255)
                    if isFilled:
                        color = (255, 255, 0)

                    pygame.draw.rect(screen, color, beatRect, width)
                pitchRowRects.append(beatList)

            pattGridsDrawn = True


            # Play
            playRect = pygame.Rect(((50, 300), (64, 64)))

            # EXPORT
            exportBracketRect = pygame.Rect((50, 400), (64, 64))

            screen.blit(playSongIcon, playRect)
            screen.blit(exportButton, exportBracketRect)

            pygame.display.flip()

        if pygame.mouse.get_pressed()[0]: #Check if left mouse pressed
            mouseLocation = pygame.mouse.get_pos()
            unentered = True
            for row in range(len(pitchRowRects)):
                for col in range(len(pitchRowRects[row])):
                    octaveNumber = (len(selectedSong.instrumentRack[
                                            selectedSong.selectedInstrument].synthesizer.sampleList) - row - 1) // 12
                    if pitchRowRects[row][col].collidepoint(mouseLocation):
                        beatrect = pygame.Rect((offSetX + col * beatWidth, offSetY + row * pitchIndexHeight - 50 * octaveNumber), (beatWidth, pitchIndexHeight))
                        if col % 4 == 0:
                            width = 3
                        else:
                            width = 1
                        pitchRowRects[row][col] = (pygame.draw.rect(screen, (255, 255, 0), beatrect, width))
                        selectedPattern.addNote(col, row)
            if playRect.collidepoint(mouseLocation):
                print("Now Playing...")
                playPattern(selectedPattern)
                unentered = False
                while pygame.mixer.get_busy():
                    continue
            if exportBracketRect.collidepoint(mouseLocation):
                print("Now Exporting...")
                screen.blit(background, backgroundRect)
                pygame.display.flip()
                exportPattern(selectedPattern, selectedSong, selectedPattern.patternPos)
                while True:
                    time.sleep(.5)
                    break
                selectedPattern = None
                unentered = False
                continue

        if pygame.mouse.get_pressed()[2]: #Right click
            mouseLocation = pygame.mouse.get_pos()
            for row in range(len(pitchRowRects)):
                for col in range(len(pitchRowRects[row])):
                    octaveNumber = (len(selectedSong.instrumentRack[
                                            selectedSong.selectedInstrument].synthesizer.sampleList) - row - 1) // 12
                    if pitchRowRects[row][col].collidepoint(mouseLocation):
                        beatrect = pygame.Rect((offSetX + col * beatWidth, offSetY + row * pitchIndexHeight - 50 * octaveNumber), (beatWidth, pitchIndexHeight))
                        if col % 4 == 0:
                            width = 3
                        else:
                            width = 1
                        pitchRowRects[row][col] = (pygame.draw.rect(screen, (255, 255, 255), beatrect, width))
                        selectedPattern.delNote(col, row)

        pygame.display.flip()








