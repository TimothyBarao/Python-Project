from pydub import AudioSegment
song = AudioSegment.from_file( "Music/erb.mp3",  format="mp3")
#change path to song above to use whatever fiel you wish 

half = len(song) / 2
first_half = song[:half]
sh3 = first_half + first_half + first_half

sh3.export("Music/3test.mp3", format="mp3")
print "Export complete"

''' simple program that takes the first half of a song and creates a new song
that is the concatentation of the first half 3 times'''
