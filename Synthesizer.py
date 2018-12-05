####################
#NAME: ZIYI ZUO
#ANDREWID: ZIYIZUO
#SECTION: N
####################

import math
import wave
from pydub import AudioSegment

####CONSIDER EXPORTING A WAV FOR EACH PITCH USED

class Synthesizer3OSC(object):

    def __init__(self, name, baseFreq=440, samplingRate = 96000):
        self.name = name
        self.baseFreq = baseFreq
        self.samplingRate = 44100
        self.waveForm = None
        self.waveTables = [[], [], []]
        self.waveForms = ["sine", "sine", "sine"]
        self.freqList = [baseFreq, baseFreq, baseFreq]
        self.freqListOffset = [0, 0, 0]
        self.sampleList = []


    def generateWaveForm(self, osc1, osc2, osc3):
        pass

    def assignWaveForm(self, osc, waveForm):
        if waveForm in ["sine", "tri", "sqr", "saw"]:
            self.waveForms[osc - 1] = waveForm

    def deleteOsc(self, osc):
        self.waveTables[osc - 1] = []

    def genWaveTable(self, frequency, osc=1, volume=.2):

        # self.freqList[osc - 1] = frequency

        def getSampleValue(freq, time, waveForm="sine"):
            #Formulas gleaned from Wolfram Mathworld
            if waveForm == "sine":
                return math.sin(2 * math.pi * freq * time)
            elif waveForm == "tri":
                return (2 / math.pi) * math.asin(math.sin(2 * math.pi * freq * time))
            elif waveForm == "sqr":
                x = math.sin((2 * math.pi * freq * time))
                if x == 0:
                    return 0.9999
                result = x / abs(x)
                if result > 0:
                    return 0.999
                else:
                    return -.999
            elif waveForm == "saw":
                unscaled = freq * (time % freq)
                result = -1 + 2 * unscaled
                return result


        def getBytes(rawValue):
            return (int((rawValue + 1) * (2 ** 7)))

        timeStep = 1 / self.samplingRate
        waveTable = list()
        time = 0
        period = 1 / frequency
        while time < period:
            waveTable.append(getBytes(volume * getSampleValue(frequency, time, self.waveForms[osc])))
            time += timeStep
        self.waveTables[osc] = waveTable


    def exportWave(self):

        for osc in range(1, 1 + len(self.waveTables)):

            #Directions on bytearray and wave class from python documentation
            exportWaveform = wave.open("%s %d waveform at %dHz.wav" % (self.name, osc, self.baseFreq), "wb")
            exportWaveform.setnchannels(1)
            exportWaveform.setsampwidth(1)
            exportWaveform.setframerate(self.samplingRate)
            exportWaveform.setnframes(0)
            exportWaveform.setcomptype('NONE', 'not compressed')

            byteString = bytearray()
            for sample in range(len(self.waveTables[osc - 1])):
                byteString.append(self.waveTables[osc - 1][sample])
            exportWaveform.writeframes(byteString)
            exportWaveform.close()

        silence = AudioSegment.from_wav("Silence.wav")
        resultSound = silence[:1000]

        for osc in range(1, 1 + len(self.waveTables)):
            waveCycle = 1 / self.freqList[osc - 1]
            oscSample = AudioSegment.from_wav("%s %d waveform at %dHz.wav" % (self.name, osc, self.baseFreq))#[:waveCycle * 1000]
            oscSample = oscSample * 10000
            resultSound = resultSound.overlay(oscSample[:1000])


        # resultSound.export("RESULT2.wav", format='wav')

        return resultSound

    def getScale(self):
        self.sampleList = []
        baseFreq = self.baseFreq
        temperament = 2 ** (1 / 12)
        for frequency in range(25):
            # print(currentFreq)
            for osc in range(3):
                self.genWaveTable(self.freqList[osc] * (temperament ** frequency), osc)
            self.sampleList.append(self.exportWave())

        # silence = AudioSegment.from_wav("Silence.wav")
        # sound = silence[:0]
        # for segment in range(len(self.sampleList) // 2):
        #     if segment % 12 in {0, 2, 3, 5, 7, 8, 11}:
        #         sound += self.sampleList[segment][:500]
        # sound.export("scaleTest.wav", format="wav")


# test1 = Synthesizer3OSC("1", 220)

# test1 = Synthesizer3OSC("1")
# test1.getScale()
# test1.assignWaveForm(1, "sine")
# test1.genWaveTable(9999, 1)
#
# test1.assignWaveForm(2, "sqr")
# test1.genWaveTable(1, 2)
#
# test1.assignWaveForm(3, "saw")
# test1.genWaveTable(4401, 3)
# test1.exportWave()
# silence = AudioSegment.from_wav("Silence.wav")
# sound = silence[:0]
# for segment in range(len(test1.sampleList) // 2):
#     if segment % 12 in {0, 2, 3, 5, 7, 8, 11}:
#         sound += test1.sampleList[segment][:500]
# for segment in range(len(test1.sampleList) // 2, -1, -1):
#     if segment % 12 in {0, 2, 3, 5, 7, 8, 11}:
#         sound += test1.sampleList[segment][:500]
# sound.export("scaleTest.wav", format="wav")
