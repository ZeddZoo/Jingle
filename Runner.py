####################
#NAME: ZIYI ZUO
#ANDREWID: ZIYIZUO
#SECTION: N
####################

import module_manager
import numpy
import pyaudio
from Pattern import *
import pygame


####################

pygame.init()

size = (1080, 720)
screen = pygame.display.set_mode(size)
currMode = "drum pattern editor" #"main menu"
running = True

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

#######REMOVE
selectedPattern = DrumPattern()
######

#Template from pygame documentation
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    #####################################################
    if currMode == "main menu":

        iconRect = icon.get_rect().move(size[1] // 2,
                                        (size[0] - iconOffset) // 5)
        titleRect = title.get_rect().move(size[1] // 2 + 50, 50)

        if pygame.mouse.get_pressed():
            if titleRect.collidepoint(pygame.mouse.get_pos()):
                currMode = "FileSelector"

        screen.blit(icon, iconRect)
        screen.blit(title, titleRect)
        pygame.display.flip()

    if currMode == "FileSelector":
        pass
        #if (createsNewFile):
            #Change mode and instatiate a new, empty pattern

    if currMode == "song editor":
        selectedPattern = Pattern.patternList[0]


    if currMode == "drum pattern editor":


        if not pattGridsDrawn:
            instrHeight = (size[1]) // (selectedPattern.instrCount * 6)
            beatWidth = (size[0] - 300) // (selectedPattern.barCount * 4)

            # pianoRoll = pygame.Surface((size[0] - 2 * marginX, size[1] - 2 * marginY))
            pianoRoll = pygame.Surface(size)
            pianoRollRects = []

            offSetX = 200
            offSetY = 200

            for instrument in range(selectedPattern.instrCount):
                instrRow = []
                for beat in range(selectedPattern.barCount * 4):
                    beatrect = ((offSetX + beat*beatWidth, offSetY + instrument * instrHeight + 50 * instrument), (beatWidth, instrHeight))
                    if beat % 4 == 0:
                        width = 3
                    else: width = 1
                    instrRow.append(pygame.draw.rect(pianoRoll, (255, 255, 255), beatrect, width))


                pianoRollRects.append(instrRow)

            pattGridsDrawn = True

            screen.blit(pianoRoll, screen.get_rect())

        if pygame.mouse.get_pressed()[0]: #Check if left mouse pressed
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
                        pianoRollRects[row][col] = (pygame.draw.rect(pianoRoll, (255, 255, 0), beatrect, width))
                        selectedPattern.addNote(col, row)

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
            iconRect = pygame.Rect((offSetX // 2, offSetY - 30 + 3* instrument * instrHeight), (64, 64))
            screen.blit(imageList[instrument], iconRect)

        #Play
        playBracketRect = pygame.Rect((offSetX, 2.75 * offSetY), (200, 100))
        playRect = pygame.Rect((offSetX + 50, 2.9 * offSetY - 10), (200, 100))
        playText = controlFont.render("PLAY", True, (255, 255, 255))
        screen.blit(bracket, playBracketRect)
        screen.blit(playText, playRect)

        #EXPORT
        exportBracketRect = pygame.Rect((3.25 * offSetX, 2.75 * offSetY), (200, 100))
        exportRect = pygame.Rect((3.25 * offSetX + 50, 2.9 * offSetY), (200, 100))
        exportText = controlFontLittle.render("EXPORT", True, (255, 255, 255))
        screen.blit(bracket, exportBracketRect)
        screen.blit(exportText, exportRect)

        # while playing:
        #     code
        #     playing = False




        pygame.display.flip()




