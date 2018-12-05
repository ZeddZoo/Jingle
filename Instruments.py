####################
#NAME: ZIYI ZUO
#ANDREWID: ZIYIZUO
#SECTION: N
####################

from Pattern import *
from Synthesizer import *

class Instrument(object):
    def __init__(self, name):
        self.name = name
        self.patterns = 0


class DrumKit(Instrument):

    def addPattern(self, patternName, barCount=4):
        self.patterns += 1
        return DrumPattern(patternName, barCount)


class Lead(Instrument):
    def __init__(self, name, baseFreq=440):
        super().__init__(name)
        self.baseFreq = baseFreq
        self.synthesizer = Synthesizer3OSC(self.name, baseFreq)

    def addPattern(self, patternName, barCount=4):
        self.patterns += 1
        return SynthPattern(patternName, barCount)



# class Bass(Instrument):
#
#     def addPattern(self, patternName, barCount=4):
#         self.patterns += 1
#         return SynthPattern(patternName, barCount)
#

