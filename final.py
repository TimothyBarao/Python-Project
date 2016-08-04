from __future__ import print_function
from PyQt4 import QtGui
import sys
import os

from pylab import *
from amen.audio import Audio
from amen.synthesize import synthesize

import numpy as np
import scipy.io.wavfile
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import wave
import copy

class SongCombine(QtGui.QWidget):
    def __init__(self, parent=None):
        super(SongCombine, self).__init__(parent)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle("Song Combine")
        self.setToolTip("Window")
        self.add_content()
        self.show()

    def on_draw(self):
        """
        Description: on_draw performs error checking on the GUI inputs and, if everything is correct, it calls the funcitons that
        create and display the graph information on the GUI.
        Return value: none.
        """

        if not self.song1.text() or not self.song2.text():
            print("Please enter an absolute path")
        else:
            for x in range(0, 8):
                # ensures that all the boxes are checked off; if not displays error message
                if not self.boxL1[x].isChecked() and not self.boxL2[x].isChecked():
                   QtGui.QMessageBox.critical(self, "Error", "Please check of all boxes", QtGui.QMessageBox.Ok)
                   break
            else:
                # ensures that the two paths to the songs are valid and the files exist
                if self.testForSong(self.song1) != 1:
                    if self.testForSong(self.song2) != 1:
                        # if corect begins grabbing final information and displays graphs on GUI
                        song1 = self.song1
                        song2 = self.song2

                        modValues = list()

                        for pos, x in enumerate(self.boxL1):
                            if x.isChecked():
                                modValue.append(pos)

                        song3 = mash(song1, song2, modValues)

                        song1_plot = create_wave(song1)
                        song2_plot = create_wave(song2)
                        song3_plot = create_wave(song3)

                        self.fig1.plot(song1_plot)
                        self.fig2.plot(song2_plot)
                        self.fig3.plot(song3_plot)
                        self.canvas.draw()

    def testForSong(self, songName):
        """
        Description: Ensures that the song exits in the path given
        Return vaue: 0 if passes the test, 1 if it fails
        """

        # parses the path given in order to test if file exists

        retVal = 0
        sN = "./"

        sN = sN + songName.text()
        self.path = sN

        if songName.text()[-1:] == "/":
            sN = songName.text()[:-1]

        filename = ""
        slashIndex = -1

        for pos, x in enumerate(sN):
            if x == "/":
                slashIndex = pos

        for pos, x in enumerate(sN):
            if pos > slashIndex:
                filename = filename + x

        sN.replace(filename, "")

        # performs check to see if file exists, throw exception if it doesn't
        try:
            if filename not in os.listdir(sN):
                #print("File not found")
                QtGui.QMessageBox.critical(self, "Error", "File for song not found", QtGui.QMessageBox.Ok)
                retVal = 1
        except OSError:
            #print("That directory does not exist")
            QtGui.QMessageBox.critical(self, "Error", "Directory for song not found", QtGui.QMessageBox.Ok)
            retVal =  1
        return retVal


    def add_content(self):
        """
        Description: Gathers all the elements necessary to make GUI and displays it.
        Return value: None.
        """

        self.setGeometry(0,0,1000,600)
        self.central_widget = QtGui.QWidget()

        # creates textbox to enter paths
        self.song1 = QtGui.QLineEdit("~/Group_Project/Gui/wav/knob.wav")
        self.song2 = QtGui.QLineEdit("~/Group_Project/Gui/wav/time.wav")

        # labels for textboxes
        s1Label = QtGui.QLabel()
        s2Label = QtGui.QLabel()

        s1Label.setText("Song 1")
        s2Label.setText("Song 2")

        # button that makes the mix occur
        mixer = MixButton(self.central_widget)

        self.mainVBox = QtGui.QVBoxLayout()
        hBox = QtGui.QHBoxLayout()

        #self.mainVBox.setSpacing(0)

        # adding all elements to horizontal layout
        hBox.addWidget(s1Label)
        hBox.addWidget(self.song1)
        hBox.addWidget(mixer)
        hBox.addWidget(self.song2)
        hBox.addWidget(s2Label)


        frame = QtGui.QFrame()
        frame.setLayout(hBox)

        self.mainVBox.addWidget(frame)

        # create check boxes
        self.boxL1 = list()
        self.boxL2 = list()
        cbg1 = QtGui.QHBoxLayout()
        cbg2 = QtGui.QHBoxLayout()
        vertNested = QtGui.QVBoxLayout()

        buttonGroup1 = QtGui.QButtonGroup()
        buttonGroup1.setExclusive(False)
        buttonGroup2 = QtGui.QButtonGroup()
        buttonGroup2.setExclusive(False)

        vertNested.setSpacing(0)

        # creates and initalizes check boxes
        # adds them to list and horizontal layout
        for x in range(0, 8):
            temp1 = QtGui.QCheckBox(str(x+1))
            temp2 = QtGui.QCheckBox(str(x+1))

            self.boxL1.append(temp1)
            self.boxL2.append(temp2)

            cbg1.addWidget(temp1)
            cbg2.addWidget(temp2)

            buttonGroup1.addButton(temp1)
            buttonGroup2.addButton(temp2)


        frame2 = QtGui.QFrame()
        frame2.setLayout(cbg1)

        vertNested.addWidget(frame2)

        frame3 = QtGui.QFrame()
        frame3.setLayout(cbg2)
        vertNested.addWidget(frame3)

        self.fig = Figure()
        self.fig1 = self.fig.add_subplot(311)
        self.fig2 = self.fig.add_subplot(312)
        self.fig3 = self.fig.add_subplot(313)
        self.canvas = FigureCanvas(self.fig)


        frame4 = QtGui.QFrame()
        cbg4 = QtGui.QVBoxLayout()
        cbg4.addWidget(self.canvas)
        frame4.setLayout(cbg4)
        vertNested.addWidget(frame4)


        self.mainVBox.addLayout(vertNested)

        self.setLayout(self.mainVBox)
        # ----------------

        # establishes connections for check boxes
        for x in range(0, 8):
            self.boxL1[x].clicked.connect(self.checkOther)
            self.boxL2[x].clicked.connect(self.checkOther)

        # when the button is clicked calls this function
        mixer.clicked.connect(self.on_draw)


    def checkOther(self):
    """
    Description: checks off check box that triggered call and greys out the opposite
    check box on the second row that is for the other song
    """

        for x in range(0, 8):
            if self.boxL1[x].isChecked():
                self.boxL2[x].setEnabled(False)
            if self.boxL2[x].isChecked():
                self.boxL1[x].setEnabled(False)

            if not self.boxL1[x].isChecked():
                self.boxL2[x].setEnabled(True)
            if not self.boxL2[x].isChecked():
                self.boxL1[x].setEnabled(True)


def mash(song1, song2, modValues):

	'''converts songs from an mp3'''
	audio1 = Audio(song1)
    audio2 = Audio(song2)

	'''breaks the song apart based on beats, returns a list of audio segments'''
    beats1 = audio1.timings['beats']
    beats2 = audio2.timings['beats']

    mashup =[]
    i = 1
	'''appends beats from each song to a list, dependent on the beats selected by the user in the GUI'''
    for beat1, beat2 in zip(beats1, beats2):
        if(i%8 in modValues):
	        mashup.append(beat1)
        else:
	        mashup.append(beat2)
        i+=1

	'''converts song from a list of audio to one seamless piece of audio'''
    out = synthesize(mashup)
    output = 'one_knob.wav'
	'''saves the newly created song as an uncompressed .wav file'''
    out.output(output)
    return output

def create_wave(song):
    mpl.rcParams['agg.path.chunksize'] = 10000
    rate, data = scipy.io.wavfile.read(song)
    data = copy.deepcopy(data)
    newdata =np.array([[0,0]])

    i = 0
    while 1:
        newdata = np.append(newdata, data[i])
        i += 10000
        if i > data.shape[0]:
            break

    return newdata

class MixButton(QtGui.QPushButton):
    """
    Description: warpper class for GUI button
    Triggers: on click causes GUI to process user information
    """

    def __init__(self, parent):
        QtGui.QPushButton.__init__(self, parent)
        self.setText("Mix")
    def enable(self, boolean):
        self.setEnabled(boolean)
    def disable(self, boolean):
        self.setDisabled(boolean)

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    main_window = SongCombine()
    app.exec_()