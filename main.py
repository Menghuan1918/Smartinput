import pyperclip
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
from translate import Translator
from main_ui import Ui_MainWindow
import sys
import subprocess
import gpt3_5api as gpt3
import json
from datetime import datetime


class GPT_file:
    def __init__(self):
        global now
        now = datetime.now()
        time_string = now.strftime("%Y.%m.%d %H.%M.%S.txt")
        now = time_string
        self.file_path = time_string

    def GPT_write_message_to_file(self, role, content):
        with open(self.file_path, "a") as file:
            message = {"role": role, "content": content.replace('"', '\\"')}
            file.write(json.dumps(message) + "\n")


with open("GPT_prompt.md", "r", encoding="utf-8") as file:
    content = file.read()
GTPstart = GPT_file()
GTPstart.GPT_write_message_to_file("system", content)
with open("openai_api.txt", "r", encoding="utf-8") as file:
    global openaikey
    openaikey = file.read()


class Main_ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.api_enter.setText(openaikey)

        self.check_translate = True
        self.check_chat = False
        self.check = False
        self.previous_clipboard = pyperclip.paste()

        self.ui.actionQuit.triggered.connect(self.check_clipboard_change)
        self.ui.pushButton.clicked.connect(self.text_go)
        self.ui.CNinput.clicked.connect(self.TKenter)
        self.ui.commandLinkButton.clicked.connect(self.cghat_history)
        self.ui.actionTranslate.triggered.connect(self.actionTran)
        self.ui.actionChatGPT.triggered.connect(self.actionChat)
        self.ui.api_ok.clicked.connect(self.renewapi)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(1000)  # 每隔1秒检查一次剪贴板

    def text_go(self):
        if self.check_translate:
            self.translate_to_chinese()
        elif self.check_chat:
            self.chatgpt3()

    def translate_to_chinese(self):
        # 用于将输入的内容翻译为中文
        text = self.ui.textEdit.toPlainText()
        translator = Translator(to_lang="zh")
        translation = translator.translate(text)
        self.ui.textBrowser.setText(translation)

    def chatgpt3(self):
        text = self.ui.textEdit.toPlainText()
        gpt_ans = gpt3.chat(openaikey, text, now)
        self.ui.textBrowser.setText(gpt_ans)

    def cghat_history(self):
        gpt_ans = gpt3.chat(openaikey, "his", now)
        self.ui.textBrowser.setText(gpt_ans)

    def renewapi(self):
        openaikey = self.ui.api_enter.toPlainText()
        info_check = "Add " + "OpenAI key: " + openaikey
        self.ui.textBrowser.setText(info_check)
        self.ui.statusbar.showMessage(info_check)
        with open("openai_api.txt", "w", encoding="utf-8") as file:
            file.truncate()
            file.write(openaikey)

    def clipboard_to_text(self):
        # 用于将剪贴板内容翻译为中文
        text = pyperclip.paste()
        self.ui.textEdit.setText(text)
        if self.check_translate:
            self.translate_to_chinese()
        elif self.check_chat:
            self.chatgpt3()

    def check_clipboard(self):
        # 用于检查剪贴板是否发生变化
        if not self.check:
            return
        current_clipboard = pyperclip.paste()
        if current_clipboard != self.previous_clipboard:
            self.clipboard_to_text()
            self.previous_clipboard = current_clipboard

    def check_clipboard_change(self):
        # 用于切换剪切板检测状态
        if self.check == True:
            self.check = False
            info_check = "Stop checking clipboard"
            self.ui.textBrowser.setText(info_check)
            self.ui.statusbar.showMessage(info_check)
        elif self.check == False:
            self.check = True
            info_check = "Start checking clipboard"
            self.ui.textBrowser.setText(info_check)
            self.ui.statusbar.showMessage(info_check)

    def actionTran(self):
        self.check_translate = True
        self.check_chat = False
        info_check = "Translate mode"
        self.ui.textBrowser.setText(info_check)
        self.ui.statusbar.showMessage(info_check)

    def actionChat(self):
        self.check_translate = False
        self.check_chat = True
        info_check = "ChatGPT3.5 mode"
        self.ui.textBrowser.setText(info_check)
        self.ui.statusbar.showMessage(info_check)

    def TKenter(self):
        # 传统输入模式
        self.check = True
        subprocess.Popen(["python3", "tk_enter.py"])

    def closeEvent(self, event):
        # 重写closeEvent方法，实现窗口关闭时执行一些操作
        reply = QtWidgets.QMessageBox.question(
            self,
            "Message",
            "Are you sure to quit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.check = False
            info_check = "Stop checking clipboard"
            self.ui.textBrowser.setText(info_check)
            self.ui.statusbar.showMessage(info_check)
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main_ui()
    window.show()
    sys.exit(app.exec())
