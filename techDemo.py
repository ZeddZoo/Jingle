####################
#NAME: ZIYI ZUO
#ANDREWID: ZIYIZUO
#SECTION: N
####################

"""TECH DEMO"""

def demopygame():
    import pygame

    pygame.init()

    screenSize = (900, 600)
    screen = pygame.display.set_mode(screenSize)
    backGround = pygame.image.load("back.png")
    backRect = backGround.get_rect()
    floor = pygame.Rect((-1000, 600, 9000000, 100000000))
    running = True

    class Character(object):
        def __init__(self, icon):
            self.icon = pygame.image.load(icon)
            self.rect = self.icon.get_rect()
            self.speed = 0
            self.acceleration = 0
            self.speedY = 0

        def move(self):
            self.rect = self.rect.move(self.speed, 0)

        def accelerateX(self, direction):
            if ((direction < 0) and (self.acceleration > 0)) or \
                    ((direction > 0) and (self.acceleration < 0)):
                self.acceleration = 0

            if -2 < self.acceleration < 2:
                self.acceleration += 1 * direction
            self.speed += self.acceleration

        def decelerateX(self):
            if self.speed < 0:
                self.speed += 1
            if self.speed > 0:
                self.speed -= 1

        def jump(self):
            self.speedY = -20
            self.rect = self.rect.move(0, self.speedY)

        def fall(self):
            self.speedY += 1
            if floor.colliderect(self.rect):
                self.rect = self.rect.move(0, -self.speedY)
                self.speedY = 0
            self.rect = self.rect.move(0, self.speedY)






    prot = Character("hero.png")


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    prot.jump()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            prot.accelerateX(1)
        if keys[pygame.K_LEFT]:
            prot.accelerateX(-1)

        prot.decelerateX()
        prot.fall()
        prot.move()
        screen.blit(backGround, backRect)
        screen.blit(prot.icon, prot.rect)
        pygame.display.flip()

#############

# demopygame()

#######################################################

def pydubDemo():
    from pydub import AudioSegment

    #Import samples:
    silence = AudioSegment.from_wav("Silence.wav")
    hat = AudioSegment.from_wav("Hat.wav")
    kick = AudioSegment.from_wav("Kick.wav")
    snare = AudioSegment.from_wav("Snare.wav")
    clap = AudioSegment.from_wav("Clap.wav")

    tempo = int(input("Please provide a tempo!"))
    secondsPerBeat = 60 * 1000 // (4 * tempo)

    loopPattern = [[1, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 1, 0],
                   [1, 0, 1, 0],

                   [1, 1, 0, 1],
                   [0, 0, 0, 0],
                   [1, 0, 1, 0],
                   [0, 0, 1, 0],

                   [1, 0, 0, 0],
                   [0, 0, 0, 0],
                   [1, 0, 1, 0],
                   [0, 0, 1, 0],

                   [0, 1, 0, 1],
                   [0, 0, 0, 0],
                   [1, 0, 1, 0],
                   [0, 0, 1, 0],
                   ]

    loop = silence[:0]


    for beat in loopPattern:
        if beat[0]:
            kickVal = kick[:secondsPerBeat]
        else:
            kickVal = silence[:secondsPerBeat]
        if beat[1]:
            snareVal = snare[:secondsPerBeat]
        else:
            snareVal = silence[:secondsPerBeat]
        if beat[2]:
            hatVal = hat[:secondsPerBeat]
        else:
            hatVal = silence[:secondsPerBeat]
        if beat[3]:
            clapVal = clap[:secondsPerBeat]
        else:
            clapVal = silence[:secondsPerBeat]
        beat = silence.overlay(kickVal).overlay(snareVal).overlay(hatVal).overlay(clapVal)[:secondsPerBeat]

        loop += beat
        print(len(beat))

    loop *= 4
    loop.export("loop.wav", format="wav")



pydubDemo()













