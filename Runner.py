####################
#NAME: ZIYI ZUO
#ANDREWID: ZIYIZUO
#SECTION: N
####################

import module_manager
# import numpy
# import pyaudio
import time
import string
from Pattern import *
from Instruments import *
from Song import *
import pygame


####################

pygame.init()

size = (1080, 720)
screen = pygame.display.set_mode(size)
background = pygame.image.load("BackGround.png")
playButton = pygame.image.load("Play.png")
playSongIcon = pygame.image.load("Play Small.png")
plusButton = pygame.image.load("Add Track.png")
exportButton = pygame.image.load("Export.png")
# playButtonRect = playButton.get_rect()
backgroundRect = background.get_rect()
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

def playPattern(patternObject):
    if not pygame.mixer.get_busy():
        patternObject.exportAsPlaying()
        nowPlaying = pygame.mixer.Sound("Now Playing.wav")
        soundPlayer.play(nowPlaying)

def playSong(songObject):
    if not pygame.mixer.get_busy():
        songObject.exportAsNowPlaying()
        nowPlaying = pygame.mixer.Sound("Now Playing.wav")
        soundPlayer.play(nowPlaying)

def exportPattern(selectedPattern, selectedSong, position):
    selectedSong.soundList[selectedPattern.instrPos][position] = selectedPattern.export()
    global currMode
    currMode = "song editor"
    global screenUncleared
    global pattGridsDrawn
    pattGridsDrawn = False
    screenUncleared = True



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
                time.sleep(.1)

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

        selectedSong = None

        if selectedSong is None:
            newSongRect = pygame.Rect((620, 400), (400, 100))
            newSongText = controlFontLittle.render("Create New Song", True, (255, 255, 255))
            screen.blit(newSongText, newSongRect)
            if pygame.mouse.get_pressed()[0]:
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
                                break

                        pygame.display.flip()

                    patternList = selectedSong.patternList
                    instrumentRack = selectedSong.instrumentRack
                    songList = selectedSong.soundList

                    currMode = "song editor"
                    selectedPattern = None
                    screenUncleared = True

        pygame.display.flip()


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
            instrumentRack.append(Lead("Lead"))
            instrumentRack.append(Lead("Bass"))
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

        if len(selectedSong.rectList) == 0:
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
                    pygame.draw.rect(screen, unselectedColor, selectedSong.rectList[instrument][pattern])
                    addRect = ((265 + pattern * barDivision + barDivision // 2 - 45,
                                instrument * instrumentHeight + 20 + instrumentHeight // 2 - 50), (50, 50))
                    screen.blit(plusButton, addRect)
                    if pygame.mouse.get_pressed()[0]:
                        if pygame.Rect(addRect).collidepoint(pygame.mouse.get_pos()):

                            patternName = str(len(Pattern.patternList))

                            while True:

                                if len(songName) > 18:
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

                                namePromptText = tempoEntryFont.render("Pattern Name: (25 char.)", True,
                                                                       (255, 255, 255))

                                screen.blit(namePromptText, namePromptBox)

                                screen.blit(patternNameRender, nameBox)

                                playButtonRect = ((490, 400), (100, 100))
                                screen.blit(playButton, playButtonRect)

                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_BACKSPACE:
                                            patternName = patternName[:-1]
                                        else:
                                            patternName += pygame.key.name(event.key)
                                            if len(songName) >= 25:
                                                patternName = patternName[:-1]

                                if pygame.mouse.get_pressed()[0]:
                                    time.sleep(.5)
                                    if pygame.Rect(playButtonRect).collidepoint(pygame.mouse.get_pos()) \
                                            and patternName != "":
                                        instrumentPatternToCreate = selectedSong.instrumentRack[instrument]
                                        if isinstance(instrumentPatternToCreate, DrumKit):
                                            selectedPattern = DrumPattern(patternName, 4, pattern, selectedSong.tempo, instrument)
                                            patternList[instrument][pattern] = selectedPattern
                                            currMode = "drum pattern editor"
                                        break

                                pygame.display.flip()
                else:
                    pygame.draw.rect(screen, selectedColor, selectedSong.rectList[instrument][pattern])
                    #Draw the name rect

                if isinstance(patternList[instrument][pattern], Pattern):
                    pygame.draw.rect(screen, selectedColor, selectedSong.rectList[instrument][pattern])

        exportRect = ((20, 640), (64, 64))
        screen.blit(exportButton, exportRect)

        playSongRect = ((92, 640), (64, 64))
        screen.blit(playSongIcon, playSongRect)

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

        for instrument in range(4):
            if instrument < len(instrumentRack):
                nameFontSize = 300 // len(instrumentRack[instrument].name)
                nameFont = pygame.font.Font("DisposableDroidBB.otf", nameFontSize)
                pygame.draw.line(screen, (255, 255, 255), (20, (instrument + 1) * instrumentHeight),
                                 (1080, (instrument + 1) * instrumentHeight), 2)
                nameRect = ((40, instrument * instrumentHeight + 55), (100, 50))
                nameText = nameFont.render(instrumentRack[instrument].name, True, (255, 255, 255))
                screen.blit(nameText, nameRect)
                #Draw Delete Instr
            else:
                #Draw Add Instr
                pass

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
                    instrRow.append(pygame.draw.rect(pianoRoll, (255, 255, 255), beatrect, width))


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




