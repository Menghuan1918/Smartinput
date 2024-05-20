import sys
import subprocess
from PyQt6.QtGui import QCursor, QIcon, QAction, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QTextEdit,
    QSystemTrayIcon,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import (
    QTimer,
    Qt,
    QTranslator,
    pyqtSignal,
    QThreadPool,
    QRunnable,
    QObject,
    QPoint,
)
import os
from Config import read_config_file,change_one_config
from Chat_LLM import predict
import logging


class Chat_LLM_Single(QObject):
    text_get = pyqtSignal(str, bool)


class Chat_LLM(QRunnable):
    def __init__(self, text, system_prompt, config):
        super(Chat_LLM, self).__init__()
        self.text = text
        self.system_prompt = system_prompt
        self.config = config
        self.text_get = Chat_LLM_Single()

    def run(self):
        try:
            for get_text in predict(
                inputs=self.text,
                llm_kwargs=self.config,
                history=[],
                system_prompt=self.system_prompt,
            ):
                self.text_get.text_get.emit(get_text, True)
        except Exception as e:
            self.text_get.text_get.emit(str(e), False)
        self.text_get.text_get.emit("", False)


class TextSelectionMonitor(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.hide()
        self.setFont(QFont(config["font"], int(config["font_size"])))

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Text edit
        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        # Copy button
        self.copy_button = QPushButton("Copy", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.layout.addWidget(self.copy_button)

        # Check selection every 1000ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_selection)
        self.timer.start(1000)
        self.process_flag = False
        self.threadpool = QThreadPool()

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip("Smartinput")

        self.is_monitoring = True
        self.current_mode = "Mode 0"
        self.current_process_mode = "Pop"
        self.current_listen_mode = "Mixed"

        self.create_menu()

        self.previous_text = self.get_selected_text()
        self.get_text = ""
        self.wait_cursor = 0

        # Try to get last window size, store in config['width'] and config['height']
        try:
            self.resize(int(config["width"]), int(config["height"]))
        except:
            pass


    def create_menu(self):
        self.menu = QMenu()

        # Toggle monitoring action
        self.toggle_action = QAction(self.tr("Text selection ON/OFF"), self)
        self.toggle_action.triggered.connect(self.toggle_monitoring)
        self.menu.addAction(self.toggle_action)

        # processing mode: Direct / Pop-up confirmation
        self.process_mode = QMenu(self.tr("Processing mode"), self)
        self.process_mode_0 = QAction(self.tr("Pop-up confirmation"), self)
        self.process_mode_0.setCheckable(True)
        self.process_mode_0.triggered.connect(lambda: self.set_process_mode("Pop"))
        self.process_mode_1 = QAction(self.tr("Direct show"), self)
        self.process_mode_1.setCheckable(True)
        self.process_mode_1.triggered.connect(lambda: self.set_process_mode("Direct"))
        self.process_mode.addAction(self.process_mode_0)
        self.process_mode.addAction(self.process_mode_1)
        self.menu.addMenu(self.process_mode)

        # Listening modes: Mixed, Clipboard, Mouse Selection
        self.listen_mode = QMenu(self.tr("Listening mode"), self)
        self.listen_mode_mixed = QAction(self.tr("Mixed"), self)
        self.listen_mode_mixed.setCheckable(True)
        self.listen_mode_mixed.triggered.connect(lambda: self.set_listen_mode("Mixed"))
        self.listen_mode_clip = QAction(self.tr("Clipboard"), self)
        self.listen_mode_clip.setCheckable(True)
        self.listen_mode_clip.triggered.connect(lambda: self.set_listen_mode("Clip"))
        self.listen_mode_mouse = QAction(self.tr("Mouse Selection"), self)
        self.listen_mode_mouse.setCheckable(True)
        self.listen_mode_mouse.triggered.connect(lambda: self.set_listen_mode("Mouse"))
        self.listen_mode.addAction(self.listen_mode_mixed)
        self.listen_mode.addAction(self.listen_mode_clip)
        self.listen_mode.addAction(self.listen_mode_mouse)
        self.menu.addMenu(self.listen_mode)

        # Mode selection submenu
        self.mode_menu = QMenu(self.tr("Response mode selection"), self)
        self.mode0_action = QAction(self.tr("Intelligent parsing"), self)
        self.mode0_action.setCheckable(True)
        self.mode0_action.triggered.connect(lambda: self.set_mode("Mode 0"))

        self.mode1_action = QAction(self.tr("Translated text"), self)
        self.mode1_action.setCheckable(True)
        self.mode1_action.triggered.connect(lambda: self.set_mode("Mode 1"))

        self.mode2_action = QAction(self.tr("Parse text"), self)
        self.mode2_action.setCheckable(True)
        self.mode2_action.triggered.connect(lambda: self.set_mode("Mode 2"))

        self.mode_menu.addAction(self.mode0_action)
        self.mode_menu.addAction(self.mode1_action)
        self.mode_menu.addAction(self.mode2_action)
        self.menu.addMenu(self.mode_menu)

        # Exit action
        exit_action = QAction(self.tr("Quit"), self)
        exit_action.triggered.connect(self.quit_save_size)
        self.menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.update_menu()

    def toggle_monitoring(self):
        self.is_monitoring = not self.is_monitoring
        if self.is_monitoring:
            if not self.timer.isActive():
                self.timer.start(1000)
        else:
            self.timer.stop()
        self.update_menu()

    def set_mode(self, mode):
        self.current_mode = mode
        self.update_menu()

    def set_process_mode(self, mode):
        self.current_process_mode = mode
        self.update_menu()

    def set_listen_mode(self, mode):
        self.current_listen_mode = mode
        self.update_menu()

    def update_menu(self):
        self.toggle_action.setText(
            self.tr("Turn on text selection")
            if not self.is_monitoring
            else self.tr("Turn off text selection")
        )
        self.process_mode_0.setChecked(self.current_process_mode == "Pop")
        self.process_mode_1.setChecked(self.current_process_mode == "Direct")

        self.listen_mode_mixed.setChecked(self.current_listen_mode == "Mixed")
        self.listen_mode_clip.setChecked(self.current_listen_mode == "Clip")
        self.listen_mode_mouse.setChecked(self.current_listen_mode == "Mouse")

        self.mode0_action.setChecked(self.current_mode == "Mode 0")
        self.mode1_action.setChecked(self.current_mode == "Mode 1")
        self.mode2_action.setChecked(self.current_mode == "Mode 2")

    def check_selection(self):
        if not self.is_monitoring or self.process_flag:
            return
        selected_text = ""
        try:
            if self.wait_cursor < 3:
                self.wait_cursor += 1
            else:
                selected_text = self.get_selected_text()
                if selected_text != self.previous_text:
                    self.previous_text = selected_text
                    if self.current_process_mode == "Direct":
                        self.set_text(selected_text)
                    else:
                        self.process_button(selected_text)
            return
        except Exception as e:
            logging.error(e)
            self.set_text(e)
            return

    def process_button(self, selected_text):
        self.button = QPushButton("Go")
        self.button.setGeometry(0, 0, 30, 30)
        self.button.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.button.setWindowOpacity(0.8)
        self.button.move(QCursor.pos() + QPoint(15, -25))
        self.button.show()
        self.button.clicked.connect(lambda: self.set_text(selected_text))
        self.button.clicked.connect(self.button.hide)
        self.timer_button = QTimer()
        self.timer_button.timeout.connect(self.hide_process_button)
        self.timer_button.start(5000)

    def hide_process_button(self):
        self.button.hide()

    def set_text(self, selected_text):
        self.process_flag = True
        self.wait_cursor = 0
        self.show()
        self.move(QCursor.pos())
        self.text_edit.setText(str(self.tr("Process...Please wait")))
        lang_dict = {
            "en_US": "English",
            "zh_CN": "Simplified Chinese",
            "fr_FR": "French",
            "es_ES": "Spanish",
            "ja_JP": "Japanese",
        }
        system_prompt = config[self.current_mode[-1:]]
        lang = lang_dict.get(config["lang"][:5], "English")
        system_prompt = system_prompt.format(lang=lang)
        self.get_text = ""
        Chat_LLM_thread = Chat_LLM(selected_text, system_prompt, config)
        Chat_LLM_thread.text_get.text_get.connect(self.update_text)
        self.threadpool.start(Chat_LLM_thread)

    def update_text(self, text, flag):
        if flag:
            self.get_text += text
            self.text_edit.setText(self.get_text)
        else:
            logging.info(f"[Get text]: {self.get_text}")
            self.text_edit.setText(self.get_text)
            self.process_flag = False

    def final_text(self, text):
        lines = text.split("\n")
        processed_lines = []
        max_len = 35 if config["lang"][:2] == "zh" else 100
        for line in lines:
            if len(line) <= max_len:
                processed_lines.append(line)
            else:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line + word) <= max_len:
                        current_line += word + " "
                    else:
                        processed_lines.append(current_line.strip())
                        current_line = word + " "
                if current_line:
                    processed_lines.append(current_line.strip())
        return " \n ".join(processed_lines)

    def get_selected_text(self):
        try:
            text = (
                subprocess.check_output(["xclip", "-o", "-selection", "clipboard"])
                .decode("utf-8")
                .strip()
            )
        except:
            try:
                text = self.previous_text
            except:
                text = ""
        try:
            primary_text = (
                subprocess.check_output(["xclip", "-o", "-selection", "primary"])
                .decode("utf-8")
                .strip()
            )
        except:
            primary_text = ""
        if self.current_listen_mode == "Mixed" and primary_text != "":
            text = primary_text
        elif self.current_listen_mode == "Clip":
            pass
        elif self.current_listen_mode == "Mouse" and primary_text != "":
            text = primary_text
        return text

    def copy_to_clipboard(self):
        text = self.text_edit.toPlainText()
        subprocess.Popen(
            ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
        ).communicate(text.encode("utf-8"))

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def quit_save_size(self):
        change_one_config("width", str(self.width()))
        change_one_config("height", str(self.height()))
        QApplication.instance().quit

if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    os.makedirs(os.path.expanduser("./log"), exist_ok=True)
    logging.basicConfig(
        filename=os.path.expanduser("./log/smartinput.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    app = QApplication(sys.argv)
    translator = QTranslator()
    config = read_config_file()
    locale = config["lang"][:2]
    if translator.load(f"translations_{locale}.qm"):
        app.installTranslator(translator)
    monitor = TextSelectionMonitor(config=config)
    sys.exit(app.exec())
