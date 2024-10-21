from PyQt6 import QtWidgets, QtGui, QtCore
import sys
from pathlib import Path
import gui
import help

class HelpWindow(QtWidgets.QWidget, help.Ui_Form):
    def __init__(self):
        super().__init__()
        self.ui = help.Ui_Form()
        self.ui.setupUi(self)

class App(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_main_name()
        #self.setWindowIcon(QtGui.QIcon("icons/text-editor.svg"))
        self.textEdit.textChanged.connect(self.txtChg)
        self.home_dir = str(Path.home())

        self.edited = False

        self.filename_filters = "All Files (*);;Text files (*.txt)"

        self.filepath = ("","")
        self.help_window = None

        QtWidgets.QMainWindow.closeEvent = self.exit_window
        QtWidgets.QMainWindow.resizeEvent = self.resize_event

        self.toolBar.setIconSize(QtCore.QSize(12,12))

        self.actionNew.triggered.connect(self.actNew)
        self.actionNew.setStatusTip("Create new File")
        self.actionNew.setIcon(QtGui.QIcon("icons/add-file.svg"))

        self.actionOpen.triggered.connect(self.actOpen)
        self.actionOpen.setStatusTip("Open new File")
        self.actionOpen.setIcon(QtGui.QIcon("icons/folder-open.svg"))

        self.actionSave.triggered.connect(self.actSave)
        self.actionSave.setStatusTip("Save the File")
        self.actionSave.setIcon(QtGui.QIcon("icons/save.svg"))

        self.actionSave_As.triggered.connect(self.actSaveAs)
        self.actionSave_As.setStatusTip("Save the File As...")

        self.actionExit.triggered.connect(self.exit_window)
        self.actionExit.setStatusTip("Close the app")
        self.actionExit.setIcon(QtGui.QIcon("icons/windows-close.svg"))
        self.actionExit.setShortcut("Alt+F4")

        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionUndo.setStatusTip("Undo")
        self.actionUndo.setIcon(QtGui.QIcon("icons/undo.svg"))
        
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionRedo.setStatusTip("Redo")
        self.actionRedo.setIcon(QtGui.QIcon("icons/redo.svg"))

        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCut.setStatusTip("Cut")
        self.actionCut.setIcon(QtGui.QIcon("icons/cut.svg"))

        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionCopy.setStatusTip("Copy")
        self.actionCopy.setIcon(QtGui.QIcon("icons/copy.svg"))

        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.actionPaste.setStatusTip("Paste")
        self.actionPaste.setIcon(QtGui.QIcon("icons/paste.svg"))

        self.actionHelp.triggered.connect(self.actHelp)
        self.actionHelp.setStatusTip("Help")
        self.actionHelp.setIcon(QtGui.QIcon("icons/help.svg"))

    def update_main_name(self, name:str = "Untilited", edited:bool = False) -> None:
        self.setWindowTitle(f"{name}{"*" * edited} - Notepad")
        self.edited = edited

    def txtChg(self):
        try:
            file = open(self.filepath[0],"rb")
            self.update_main_name(file.name.split("/")[-1],file.read() != self.textEdit.toPlainText().encode("utf-8"))
            #self.edited = (file.read() != self.textEdit.toPlainText().encode("utf-8"))
        except:
            self.update_main_name(edited = "" != self.textEdit.toPlainText().encode("utf-8"))
            #self.edited = ("" != self.textEdit.toPlainText().encode("utf-8"))

    def resize_event(self, event:QtGui.QResizeEvent):
        self.textEdit.setGeometry(QtCore.QRect(-1,-1,event.size().width() + 2,event.size().height() - 60 + 2))

    def exit_window(self, event:QtGui.QCloseEvent):
        if self.edited == True:
            try:
                filename = open(self.filepath[0],"rb").name.split("/")[-1]
            except:
                filename = "Untilited"
            close = QtWidgets.QMessageBox.question(self,
                                                        "QUIT?",
                                                        f"Do you want to save the changes to a file\n{filename}?",
                                                        QtWidgets.QMessageBox.StandardButton.Yes|QtWidgets.QMessageBox.StandardButton.No|QtWidgets.QMessageBox.StandardButton.Cancel)
            if close == QtWidgets.QMessageBox.StandardButton.Yes:
                try:
                    self.actSave()
                    event.accept()
                    sys.exit()
                except AttributeError:
                    sys.exit()
            elif close == QtWidgets.QMessageBox.StandardButton.Cancel:
                try:
                    event.ignore()
                except AttributeError:
                    pass
            elif close == QtWidgets.QMessageBox.StandardButton.No:
                try:
                    event.accept()
                    sys.exit()
                except AttributeError:
                    sys.exit()
        else:
            try:
                event.accept()
                sys.exit()
            except AttributeError:
                sys.exit()

    def actNew(self):
        self.filepath = ""

        self.textEdit.setPlainText("")
        self.update_main_name()

    def actOpen(self):
        self.filepath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', self.home_dir, self.filename_filters)

        try:
            file = open(self.filepath[0],"rb")
            self.textEdit.setPlainText(file.read().decode("utf-8"))
            self.update_main_name(file.name.split("/")[-1])
            file.close()
            self.txtChg()
        except:
            pass

    def actSave(self):
        try:
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
        except:
            self.actSaveAs()

    def actSaveAs(self):
        self.filepath = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', self.home_dir, self.filename_filters)
        file = open(self.filepath[0],"wb")
        file.write(self.textEdit.toPlainText().encode("utf-8"))
        self.update_main_name(file.name.split("/")[-1])
        file.close()
        self.txtChg()

    def actHelp(self):
        if self.help_window is None:
            self.help_window = HelpWindow()
        self.help_window.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyleSheet(Path("style.qss").read_text())
    #app.setStyleSheet(Path("dark_style.qss").read_text())
    app.setStyleSheet(Path("blue_style.qss").read_text())
    window = App()

    window.show()
    app.exec()

if __name__ == '__main__':
    main()