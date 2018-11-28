####################
#NAME: ZIYI ZUO
#ANDREWID: ZIYIZUO
#SECTION: N
####################

from Pattern import *

class Instrument(object):
    def __init__(self, name):
        self.name = name
        self.patterns = 0

class DrumKit(Instrument):

    def addPattern(self, patternName, barCount=4):
        self.patterns += 1
        return DrumPattern(patternName, barCount)

class Lead(Instrument):

    def addPattern(self, patternName, barCount=4):
        self.patterns += 1
        return SynthPattern(patternName, barCount)

class Bass(Instrument):

    def addPattern(self, patternName, barCount=4):
        self.patterns += 1
        return SynthPattern(patternName, barCount)


