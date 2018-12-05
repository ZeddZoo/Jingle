import wave

exportWaveform = wave.open("test waveform.wav", "wb")
exportWaveform.setnchannels(1)
exportWaveform.setsampwidth(3)
exportWaveform.setframerate(44100)

byteString = ""
# byteString = "0xff-0x0-0xff-0x00xff0x00xff0x00xff0x0"
for i in range(-255, 255):
	if i % 2 == 0:
		byteString += bin(1) + bin(i) + bin(1)

print(byteString)



exportWaveform.writeframes(bytearray(byteString, 'utf-8'))