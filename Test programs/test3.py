import sys
from aubio import source, pitch
from pydub import AudioSegment
from math import floor

'''
if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]
'''

filename1 = "Music/song_1.mp3"
filename2 = "Music/song_2.mp3"

downsample = 1
samplerate = 44100 // downsample
#if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

samplerate = 44100

win_s = 4096 // downsample # fft size
hop_s = 512  // downsample # hop size

s = source(filename1, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 0.8

pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

pitches = []
confidences = []

# total number of frames read
total_frames = 0
time_stamps_1 = []
time_stamps_2 = []
p = 0.0
n = 0.0
while True:
    samples, read = s()
    pitch = pitch_o(samples)[0]
    n = pitch

    if n > (p * 1.5) or n < (p * .5):
        #print "n: "
        #print n
        #print total_frames/float(samplerate)
        time_stamps_1.append(total_frames/float(samplerate))
        #print "p:"
        #print p
    p = pitch

    #pitch = int(round(pitch))
    confidence = pitch_o.get_confidence()
    #if confidence < 0.8: pitch = 0.
    #print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
    pitches += [pitch]
    confidences += [confidence]
    total_frames += read
    if read < hop_s: break


s = source(filename2, samplerate, hop_s)
samplerate = s.samplerate

pitch_o.set_unit("freq")
pitch_o.set_tolerance(tolerance)

pitches = []
confidences = []

# total number of frames read
total_frames = 0
p = 0.0
n = 0.0
while True:
    samples, read = s()
    pitch = pitch_o(samples)[0]
    n = pitch

    if n > (p * 15.0):
        #print "n: "
        #print n
        #print total_frames/float(samplerate)
        time_stamps_2.append(total_frames/float(samplerate))
        #print "p:"
        #print p
    p = pitch

    #pitch = int(round(pitch))
    confidence = pitch_o.get_confidence()
    #if confidence < 0.8: pitch = 0.
    #print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
    pitches += [pitch]
    confidences += [confidence]
    total_frames += read
    if read < hop_s: break




'''
for i in time_stamps_1:
    print i

for i in time_stamps_2:
    print i
'''

print len(time_stamps_1)

print len(time_stamps_2)

i = 0

while i < len(time_stamps_1):
    time_stamps_1[i] = floor(time_stamps_1[i]) * 1000
    i +=1

i = 0
while i < len(time_stamps_2):
    time_stamps_2[i] = floor(time_stamps_2[i]) * 1000
    i +=1
   
time_stamps_1 =  sorted(set(time_stamps_1))
time_stamps_2 =  sorted(set(time_stamps_2))


for i in time_stamps_1:
    print i

song1 = AudioSegment.from_file( "Music/song_1.mp3",  format="mp3")
song2 = AudioSegment.from_file( "Music/song_2.mp3",  format="mp3")

split1 = []
split2 = []


print "TESTING SPLITTING"


k = 0
for j in time_stamps_1:
    part = song1[k:j]
    split1.append(part)
    k = j

k = 0
for j in time_stamps_2:
    part = song2[k:j]
    split2.append(part)
    k = j


new_song = song1[:1]


'''
for i in split1:
    new_song += i
'''

lol = 0
while lol < len(split1):
    new_song += split1[lol] + split2[lol]
    lol += 1


'''
lol = 0
while lol < len(split1):



    new_song += split1[lol]
    print "TESTESTESTEST"
    lol +=1
'''

new_song.export("Music/please.mp3", format="mp3")


'''
half = len(song) / 2
first_half = song[:half]
sh3 = first_half + first_half + first_half



sh3.export("Music/3test.mp3", format="mp3")
print "Export complete"
'''





