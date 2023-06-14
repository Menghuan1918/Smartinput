import pyperclip
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from translate import Translator

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 781, 221))
        self.textEdit.setObjectName("textEdit")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 280, 781, 261))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 240, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 240, 321, 26))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuMain = QtWidgets.QMenu(parent=self.menubar)
        self.menuMain.setObjectName("menuMain")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtGui.QAction(parent=MainWindow)
        self.actionQuit.setObjectName("Check Clipboard")
        self.menuMain.addAction(self.actionQuit)
        self.menubar.addAction(self.menuMain.menuAction())
        self.actionQuit.triggered.connect(self.check_clipboard_change)

        self.retranslateUi(MainWindow)
        self.pushButton_2.clicked.connect(self.textEdit.clear)
        self.pushButton_2.clicked.connect(self.textBrowser.clear)
        self.pushButton.clicked.connect(self.translate_to_chinese)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ENG TO CN"))
        self.pushButton.setText(_translate("MainWindow", "Translate"))
        self.pushButton_2.setText(_translate("MainWindow", "Clear"))
        self.menuMain.setTitle(_translate("MainWindow", "Main"))
        self.actionQuit.setText(_translate("MainWindow", "Check Clipboard"))
    
    def check_clipboard_change(self):
        global check
        if(check == True):
            check = False
            info_check = "Stop checking clipboard"
            self.textBrowser.setText(info_check)
            self.statusbar.showMessage(info_check)
            print(info_check)
        elif(check == False):
            check = True
            info_check = "Start checking clipboard"
            self.textBrowser.setText(info_check)
            self.statusbar.showMessage(info_check)
            print(info_check)
            self.check_clipboard()

    def translate_to_chinese(self):
        text = self.textEdit.toPlainText()
        translator = Translator(to_lang='zh')
        translation = translator.translate(text)
        self.textBrowser.setText(translation)
    
    def clipboard_to_chinese(self):
        text = pyperclip.paste()
        self.textEdit.setText(text)
        translator = Translator(to_lang='zh')
        translation = translator.translate(text)
        self.textBrowser.setText(translation)
    
    def check_clipboard(self):
        previous_clipboard = pyperclip.paste()
        while check:
            current_clipboard = pyperclip.paste()
            if current_clipboard != previous_clipboard:
                self.clipboard_to_chinese()
                previous_clipboard = current_clipboard
            QtWidgets.QApplication.processEvents()

if __name__=="__main__":
    check  = True
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    if check:
        ui.check_clipboard()
    sys.exit(app.exec())