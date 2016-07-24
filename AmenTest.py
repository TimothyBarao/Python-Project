from amen.utils import example_audio_file
from amen.audio import Audio
from amen.synthesize import synthesize

#audio_file = example_audio_file()

#audio_file1 = 'testtracks/01 One More Time.mp3'
#audio_file2 = 'testtracks/Knobbers.mp3'

#audio_file1 = 'testtracks/01 & Down (Original Mix).mp3'
#audio_file2 = 'testtracks/Aerodynamic (Daft Punk Remix).mp3'

#audio_file1 = 'testtracks/01 Old English.m4a'
#audio_file2 = 'testtracks/06 Empathy.mp3'

#audio_file1 = 'testtracks/1-02 Free Floating.mp3'
#audio_file2 = 'testtracks/02. The Clapping Track.mp3'

#audio_file1 = 'testtracks/01 This is Acid (Boys Noize Edit).mp3'
#audio_file2 = 'testtracks/01 Optic.mp3'

#audio_file1 = 'testtracks/01 Pop The Glock.mp3'
#audio_file2 = 'testtracks/Depeche Mode - Enjoy the Silence (Hands and Feet Mix).mp3'

#audio_file1 = 'testtracks/01 Upside Down.mp3'
#audio_file2 = 'testtracks/1-05 Give & Take.mp3'

#audio_file2 = 'testtracks/01 Mr. Muscle.m4a'
#audio_file1 = 'testtracks/01 Tell Me.m4a'

audio_file2 = 'testtracks/DatsiK - Apples [Dubstep].mp3'
audio_file1 = 'testtracks/Denzel Curry - Threatz.mp3'

#audio_file2 = 'testtracks/jealous.mp3'
#audio_file1 = 'testtracks/woman.mp3'



def mash(song1, song2):
	audio1 = Audio(song1)
	audio2 = Audio(song2)


	beats1 = audio1.timings['beats']
	beats2 = audio2.timings['beats']



	mashup =[]
	i = 1
	for beat1, beat2 in zip(beats1, beats2):
		#if (i % 4 == 3 or i % 4 == 1):
		#if (i % 4 == 2 or i % 4 == 1):
		if(i%8 == 7):
		#if (i % 4 == 3):
			mashup.append(beat1)
		else:
			mashup.append(beat2)
		i+=1

	#beats.reverse()
	out = synthesize(mashup)
	out.output('one_more_knob.wav')

if __name__ == '__main__':
	try:
		mash(audio_file1, audio_file2)
	except ValueError:
		print 'IT ERRORED'
		mash(audio_file2, audio_file1)
