from aubio import pitch, source

s = source("Music/erb.mp3", 44100, 512)
samplerate = s.samplerate

pitch_o = pitch("yin", 4096, 512, samplerate)
pitch_o.set_tolerance(0.8)

pitches = []
conf =[]
timestamp =[]

total_frames = 0
while True:
   samples, read = s()
   pitch = pitch_o(samples)[0]
   pitch = float(pitch)
   confidence = pitch_o.get_confidence()
   print "%f %f %f" % (total_frames/float(samplerate), pitch, confidence)
   pitches += [pitch]
   conf +=[confidence]
   timestamp +=[total_frames/float(samplerate)]
   total_frames += read
   if read < 512: break

print "Total seconds in song:"
print total_frames/float(samplerate)
