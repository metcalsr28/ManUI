from PyQt5 import QtWidgets, QtGui, QtCore, uic
import sys
import os
import subprocess


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('MainWindow.ui', self)  # Load the .ui file

        self.lvFiles = self.findChild(QtWidgets.QListView, 'lvFiles')
        self.teManOutput = self.findChild(QtWidgets.QTextEdit, 'teManOutput')
        self.menuSelectFolder = self.findChild(QtWidgets.QMenu, 'menuSelectFolder')
        self.menu_action = QtWidgets.QAction('Option #1', self)
        self.menu_action.triggered.connect(self.menuSelectFolderClicked)
        self.menuSelectFolder.addAction(self.menu_action)
        self.current_folder = "/"

        self.model = QtGui.QStandardItemModel()
        self.lvFiles.setModel(self.model)

        self.selectedListItem = ""
        self.lvFiles.clicked[QtCore.QModelIndex].connect(self.lvFilesClicked)

        for root, dirs, files in os.walk("/bin/"):
            for filename in files:
                self.model.appendRow(QtGui.QStandardItem(filename))
            break
        self.show()  # Show the GUI

    def menuSelectFolderClicked(self):
        print("test")
        self.current_folder = QtWidgets.QFileDialog.getExistingDirectory()
        self.model.clear()
        for root, dirs, files in os.walk(self.current_folder):
            for filename in files:
                self.model.appendRow(QtGui.QStandardItem(filename))
            break

    def lvFilesClicked(self, index):
        self.selectedListItem = self.model.itemFromIndex(index)
        print(self.selectedListItem.text())
        try:
            os.remove("last_output.txt")
        except:
            print("File Not Found!")
        proc = subprocess.Popen('man ' + self.selectedListItem.text() + " >> last_output.txt", shell=True)
        proc.wait()
        
        self.teManOutput.clear()
        with open("last_output.txt", "r") as output:
            contents = output.readlines()
            if not contents:
                self.teManOutput.append("NO MANUAL ENTRY FOR THIS FILE")
                return
            for i in range(len(contents)):
                self.teManOutput.append(contents[i])
            self.teManOutput.verticalScrollBar().setValue(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Ui()  # Create an instance of our class
    app.exec_()  # Start the application