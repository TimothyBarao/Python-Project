from __future__ import print_function
from PyQt5 import QtWidgets, QtGui
import sys
import os

class SongCombine(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle("Song Combine")
        self.setToolTip("yuh")
        self.add_content()
        self.show()

    def on_draw(self):
        if not self.song1.text() or not self.song2.text():
            print("Please enter an absolute path")
        else:

            for x in xrange(0, 8):
                if self.boxL1[x].isChecked() and self.boxL2[x].isChecked():
                   QtWidgets.QMessageBox.critical(self, "Error", "Cannot have same measure checked", QtWidgets.QMessageBox.Ok)
                   break


            if self.testForSong(self.song1) != 1:
                if self.testForSong(self.song2) != 1:
                    print("run Tim's code here")


    def testForSong(self, songName):
        retVal = 0
        s1 = songName.text().split('/')
        scanLocation = "/".join(s1[:-1])

        if(songName == "song1"):
            fileErrorMsg = "File for song 1 not found"
            dirErrorMsg = "Directory for song 1 not found"
        else:
            fileErrorMsg = "File for song 2 not found"
            dirErrorMsg = "Directory for song 2 not found"

        try:
            if s1[-1] not in os.listdir(scanLocation):
                print("File not found")
                QtWidgets.QMessageBox.critical(self, "Error", fileErrorMsg, QtWidgets.QMessageBox.Ok)
                retVal = 1
        except OSError:
            print("That directory does not exist")
            QtWidgets.QMessageBox.critical(self, "Error", dirErrorMsg, QtWidgets.QMessageBox.Ok)
            retVal = 1

        return retVal


    def add_content(self):
        self.central_widget = QtWidgets.QWidget()

        # creates textbox to enter paths
        self.song1 = QtWidgets.QLineEdit("~/absolute/path/example")
        self.song2 = QtWidgets.QLineEdit("~/absolute/path/example")

        # labels for textboxes
        s1Label = QtWidgets.QLabel()
        s2Label = QtWidgets.QLabel()

        s1Label.setText("Song 1")
        s2Label.setText("Song 2")

        # button that makes the mix occur
        mixer = MixButton(self.central_widget)

        self.mainVBox = QtWidgets.QVBoxLayout()
        hBox = QtWidgets.QHBoxLayout()

        #self.mainVBox.setSpacing(0)

        # adding all elements to horizontal layout
        hBox.addWidget(s1Label)
        hBox.addWidget(self.song1)
        hBox.addWidget(mixer)
        hBox.addWidget(self.song2)
        hBox.addWidget(s2Label)

        frame = QtWidgets.QFrame()
        frame.setLayout(hBox)

        self.mainVBox.addWidget(frame)

        # create check boxes -------------------
        self.boxL1 = list()
        self.boxL2 = list()
        cbg1 = QtWidgets.QHBoxLayout()
        cbg2 = QtWidgets.QHBoxLayout()
        vertNested = QtWidgets.QVBoxLayout()

        buttonGroup1 = QtWidgets.QButtonGroup()
        buttonGroup1.setExclusive(False)
        buttonGroup2 = QtWidgets.QButtonGroup()
        buttonGroup2.setExclusive(False)

        vertNested.setSpacing(0)

        for x in xrange(0, 8):
            temp1 = QtWidgets.QCheckBox(str(x+1))
            temp2 = QtWidgets.QCheckBox(str(x+1))

            self.boxL1.append(temp1)
            self.boxL2.append(temp2)

            cbg1.addWidget(temp1)
            cbg2.addWidget(temp2)

            buttonGroup1.addButton(temp1)
            buttonGroup2.addButton(temp2)


        frame2 = QtWidgets.QFrame()
        frame2.setLayout(cbg1)

        vertNested.addWidget(frame2)

        frame3 = QtWidgets.QFrame()
        frame3.setLayout(cbg2)
        vertNested.addWidget(frame3)

        self.mainVBox.addLayout(vertNested)

        # ----------------

        for x in xrange(0, 8):
            self.boxL1[x].clicked.connect(self.checkOther)
            self.boxL2[x].clicked.connect(self.checkOther)

        # when the button is clicked calls this function
        mixer.clicked.connect(self.on_draw)

        self.central_widget.setLayout(self.mainVBox)
        self.setCentralWidget(self.central_widget)

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

class MixButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Mix")
    def enable(self, boolean):
        self.setEnabled(boolean)
    def disable(self, boolean):
        self.setDisabled(boolean)

if __name__ == "__main__":
    print("subbable")

    app = QtWidgets.QApplication(sys.argv)
    main_window = SongCombine()

    app.exec_()