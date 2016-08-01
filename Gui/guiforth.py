from __future__ import print_function
from PyQt4 import QtGui
import sys
import os

class SongCombine(QtGui.QWidget):
    def __init__(self, parent=None):
        super(SongCombine, self).__init__(parent)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle("Song Combine")
        self.setToolTip("Window")
        self.add_content()
        self.show()

    def on_draw(self):
        if not self.song1.text() or not self.song2.text():
            print("Please enter an absolute path")
        else:
            for x in xrange(0, 8):
                if not self.boxL1[x].isChecked() and not self.boxL2[x].isChecked():
                   QtGui.QMessageBox.critical(self, "Error", "Please check of all boxes", QtGui.QMessageBox.Ok)
                   break
            else:
                if self.testForSong(self.song1) != 1:
                    if self.testForSong(self.song2) != 1:
                        print("run Tim's code here")


    def testForSong(self, songName):
        retVal = 0
        s1 = str(songName.text().split('/'))
        scanLocation = "/".join(s1[:-1])

        print(songName.text())

        try:
            if s1[-1] not in os.listdir(scanLocation):
                #print("File not found")
                QtGui.QMessageBox.critical(self, "Error", "File for song not found", QtGui.QMessageBox.Ok)
                retVal = 1
        except OSError:
            #print("That directory does not exist")
            QtGui.QMessageBox.critical(self, "Error", "Directory for song not found", QtGui.QMessageBox.Ok)
            retVal = 1

        return retVal


    def add_content(self):
        self.central_widget = QtGui.QWidget()

        # creates textbox to enter paths
        self.song1 = QtGui.QLineEdit("~/absolute/path/example")
        self.song2 = QtGui.QLineEdit("~/absolute/path/example")

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

        # create check boxes -------------------
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

        for x in xrange(0, 8):
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

        self.mainVBox.addLayout(vertNested)

        self.setLayout(self.mainVBox)
        # ----------------

        for x in xrange(0, 8):
            self.boxL1[x].clicked.connect(self.checkOther)
            self.boxL2[x].clicked.connect(self.checkOther)

        # when the button is clicked calls this function
        mixer.clicked.connect(self.on_draw)

        #self.central_widget.setLayout(self.mainVBox)
        #self.setCentralWidget(self.central_widget)

    def checkOther(self):
        for x in xrange(0, 8):
            if self.boxL1[x].isChecked():
                self.boxL2[x].setEnabled(False)
            if self.boxL2[x].isChecked():
                self.boxL1[x].setEnabled(False)

            if not self.boxL1[x].isChecked():
                self.boxL2[x].setEnabled(True)
            if not self.boxL2[x].isChecked():
                self.boxL1[x].setEnabled(True)

class MixButton(QtGui.QPushButton):
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