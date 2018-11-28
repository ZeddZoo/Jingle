####################
#NAME: ZIYI ZUO
#ANDREWID: ZIYIZUO
#SECTION: N
####################

import pickle

from pydub import AudioSegment

class Song(object):

    def __init__(self, songName, tempo):
        self.silence = AudioSegment.from_wav("Silence.wav")
        self.songName = songName
        self.tempo = tempo
        self.secondsPerBar = 60 * 1000 // (self.tempo)
        self.patternList = []
        self.soundList = []
        for i in range(4):
            self.patternList.append([None] * 4)
            self.soundList.append([self.silence[:self.secondsPerBar]] * 4)
        self.instrumentRack = []
        self.rectList = []

    def saveSong(self):
        pickle.dump(self, "%s.pyc" % self.songName)

    def exportSong(self):
        song = self.silence[:0]
        for bar in range(len(self.soundList[0])):
            barSound = self.silence[:(4* self.secondsPerBar)]
            for instrument in range(len(self.soundList)):
                barSound = barSound.overlay(self.soundList[instrument][bar])
            song = song + barSound
        song.export("%s - %d BPM.wav" % (self.songName, self.tempo), format="wav")

    def exportAsNowPlaying(self):
        song = self.silence[:0]
        for bar in range(len(self.soundList[0])):
            barSound = self.silence[:(4 * self.secondsPerBar)]
            for instrument in range(len(self.soundList)):
                barSound = barSound.overlay(self.soundList[instrument][bar])
            song = song + barSound
        song.export("Now Playing.wav", format="wav")

    def __repr__(self):
        return "%s at %d BPM" % (self.songName, self.tempo)

