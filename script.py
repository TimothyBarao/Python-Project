from pydub import AudioSegment
import sys
sound = AudioSegment.from_mp3(sys.argv[1])

first10 = 10 * 10000

sound = sound[:first10]


sound.export("30.wav", format="wav")





