####################
#NAME: ZIYI ZUO
#ANDREWID: ZIYIZUO
#SECTION: N
####################

from pydub import AudioSegment
from Synthesizer import *
import numpy

silence = AudioSegment.from_wav("Silence.wav")

#####SOUNDS SAMPLED FROM FL STUDIO 20 DEFAULT DRUM KIT########
hat = AudioSegment.from_wav("Hat.wav")
kick = AudioSegment.from_wav("Kick.wav")
snare = AudioSegment.from_wav("Snare.wav")
clap = AudioSegment.from_wav("Clap.wav")
##############################################################


class Pattern(object):

    patternList = []

    def __init__(self, patternName=len(patternList), barCount=4, instrCount=-1, patternPos=-1, tempo=112, instrPos=-1):
        self.barCount = barCount
        self.instrCount = instrCount
        self.pianoRoll = []
        self.name = patternName
        self.tempo = tempo
        self.instrPos = instrPos
        self.patternPos = patternPos            #Figure out units for this
        for bar in range(4 * barCount):
            self.pianoRoll.append([0] * instrCount)
        Pattern.patternList.append(self)

    def copy(self):
        return Pattern(self.name, self.barCount, self.instrCount)

    def addNote(self, beat, instr):
        self.pianoRoll[beat][instr] = 1

    def delNote(self, beat, instr):
        self.pianoRoll[beat][instr] = 0

    def addToPlayList(self, position):
        self.patternPos = position





class DrumPattern(Pattern):
    #Make sure to check if this increments patternCount later
    def __init__(self, patternName=len(Pattern.patternList), barCount = 4, patternPos=-1, tempo = 112, instrPos = -1):
        super().__init__(patternName, barCount, 4, patternPos, tempo, instrPos)

    def export(self):
        silenceLen = silence[:self.patternPos]
        secondsPerBeat = 60 * 1000 // (4 * self.tempo)
        exportPattern = silence[:0]

        for beat in self.pianoRoll:
            beatSound = silence[:secondsPerBeat]
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
            beatSound = silence.overlay(kickVal).overlay(snareVal).overlay(hatVal).overlay(clapVal)[:secondsPerBeat]

            exportPattern += beatSound

        return exportPattern

    def exportAsPlaying(self):
        nowPlaying = self.export()
        nowPlaying.export("Now Playing.wav", format="wav")

class SynthPattern(Pattern):
    # Make sure to check if this increments patternCount later
    def __init__(self, patternName=len(Pattern.patternList), barCount = 4, patternPos=-1, tempo = 112, instrPos = -1):
        super().__init__(patternName, barCount, 1, patternPos, tempo, instrPos)
        self.scaleIndex = []
        self.pianoRoll = []
        for bar in range(4 * barCount):
            self.pianoRoll.append([0] * 25)

    def export(self, synth):
        secondsPerBeat = 60 * 1000 // (4 * self.tempo)
        exportPattern = silence[:0]


        for beat in self.pianoRoll:
            beatSound = silence[200:secondsPerBeat + 200]
            for pitch in range(len(beat)):
                if beat[pitch] == 1:
                    actualPitch = len(beat) - pitch - 1
                    t1, t2, t3 = synth.synthesizer.freqList
                    t1 = int(t1 * ((2 ** (1 / 12)) ** actualPitch))
                    t2 = int(t2 * ((2 ** (1 / 12)) ** actualPitch))
                    t3 = int(t3 * ((2 ** (1 / 12)) ** actualPitch))
                    lcmT = numpy.lcm.reduce([t1, t2, t3])   #From scipy.org
                    if lcmT > secondsPerBeat:
                        beatSound = beatSound.overlay(synth.synthesizer.sampleList[actualPitch][200:secondsPerBeat + 200])
                    else:
                        print('hello', lcmT)
                        beatSound = beatSound.overlay(synth.synthesizer.sampleList[actualPitch][200:lcmT * 1000 + 200])
                        beatSound = beatSound * 1000
                        beatSound = beatSound[:secondsPerBeat]
            exportPattern += beatSound

        return exportPattern

    def exportAsPlaying(self, synth):
        nowPlaying = self.export(synth)
        nowPlaying.export("Now Playing.wav", format="wav")




