from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import os
from io import TextIOWrapper
from pathlib import Path
import gui

class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_main_name()
        self.textEdit.textChanged.connect(self.txtChg)
        self.home_dir = str(Path.home())

        self.filename_filters = "All Files (*);;Text files (*.txt)"

        self.filepath = ("","")

        QtWidgets.QMainWindow.closeEvent = self.exit_window
        QtWidgets.QMainWindow.resizeEvent = self.resize_event

        self.actionOpen.triggered.connect(self.actOpen)
        self.actionOpen.setStatusTip("Open new File")

        self.actionExit.triggered.connect(self.exit_window)
        self.actionOpen.setStatusTip("Close the app")

        self.actionSave.triggered.connect(self.actSave)
        self.actionSave.setStatusTip("Save the File")

    def update_main_name(self, name:str = "Untilited", edited:bool = False) -> None:
        self.setWindowTitle(f"{name}{"*" * edited} - Notepad")

    def txtChg(self):
        try:
            file = open(self.filepath[0],"rb")
            self.update_main_name(file.name.split("/")[-1],file.read() != self.textEdit.toPlainText().encode("utf-8"))
        except:
            pass

    def resize_event(self, event:QtGui.QResizeEvent):
        self.textEdit.setGeometry(QtCore.QRect(0,0,event.size().width(),event.size().height() - 45))

    def exit_window(self, event:QtGui.QCloseEvent):
        close = QtWidgets.QMessageBox.question(self,
                                                    "QUIT?",
                                                    "Are you sure want to STOP and EXIT?",
                                                    QtWidgets.QMessageBox.StandardButton.Yes|QtWidgets.QMessageBox.StandardButton.No)
        if close == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                event.accept()
                sys.exit()
            except AttributeError:
                sys.exit()
        else:
            try:
                event.ignore()
            except AttributeError:
                pass

    def actOpen(self):
        self.filepath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', self.home_dir, self.filename_filters)

        try:
            file = open(self.filepath[0],"rb")
            self.textEdit.setPlainText(file.read().decode("utf-8"))
            self.update_main_name(file.name.split("/")[-1])
            file.close()
        except:
            pass

    def actSave(self):
        if self.filepath[0] != "":
            file = open(self.filepath[0],"wb")
            file.write(self.textEdit.toPlainText().encode("utf-8"))
            file.close()
        elif self.filepath[0] == "":
            self.filepath = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', self.home_dir, self.filename_filters)
            file = open(self.filepath[0],"wb")
            file.write(self.textEdit.toPlainText().encode("utf-8"))
            self.update_main_name(file.name.split("/")[-1])
            file.close()
        self.txtChg()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()

    window.show()
    app.exec()

if __name__ == '__main__':
    main()