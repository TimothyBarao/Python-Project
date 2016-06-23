from pydub import AudioSegment
song = AudioSegment.from_file( "Music/erb.mp3",  format="mp3")

half = len(song) / 2
first_half = song[:half]
sh3 = first_half + first_half + first_half

sh3.export("Music/3test.mp3", format="mp3")
print "Export complete"
