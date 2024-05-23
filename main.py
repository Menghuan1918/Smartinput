import sys
from PyQt6.QtGui import QCursor, QIcon, QAction, QFont, QTextCursor
from PyQt6.QtWidgets import (
    QApplication,
    QTextEdit,
    QSystemTrayIcon,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QStatusBar,
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
from Tools.Config import read_config_file, change_one_config
from Tools.Chat_LLM import predict
import logging
from Tools.Get_Copy import get_selected_text, copy_to_clipboard


class Chat_LLM_Single(QObject):
    text_get = pyqtSignal(str, int)


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
                self.text_get.text_get.emit(get_text, 1)
        except Exception as e:
            self.text_get.text_get.emit(str(e), 2)
        self.text_get.text_get.emit("", 0)


class TextSelectionMonitor(QWidget):
    def __init__(self, General_config):
        super().__init__()
        self.LLM_config = read_config_file(filename="LLM_config")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.hide()
        self.setFont(QFont(General_config["font"], int(General_config["font_size"])))
        self.setWindowTitle("Smartinput")
        self.setWindowIcon(QIcon("icon.png"))

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Text edit
        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        # Copy button
        self.copy_button = QPushButton(self.tr("Copy"), self)
        self.copy_button.clicked.connect(self.copy_to_clipboard_ui)
        self.layout.addWidget(self.copy_button)

        # Status bar
        self.status_bar = QStatusBar()
        self.layout.addWidget(self.status_bar)
        status_font_size = max(1, int(General_config["font_size"]) - 5)
        self.status_bar.setFont(QFont(General_config["font"], status_font_size))

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
        self.current_mode = General_config["current_mode"]
        self.current_process_mode = General_config["current_process_mode"]
        self.current_listen_mode = General_config["current_listen_mode"]

        self.create_menu()

        self.previous_text = ""
        self.previous_text = get_selected_text(
            self.previous_text, self.current_listen_mode
        )
        self.get_text = ""
        self.wait_cursor = 0

        # Try to get last window size, store in config['width'] and config['height']
        try:
            self.resize(int(General_config["width"]), int(General_config["height"]))
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

        #! Need to change!
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
        #! End here

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
            if self.wait_cursor < 2:
                self.wait_cursor += 1
            else:
                selected_text = get_selected_text(
                    self.previous_text, self.current_listen_mode
                )
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
        self.status_bar.showMessage(self.tr("Processing: Sending request..."))
        lang_dict = {
            "en_US": "English",
            "zh_CN": "Simplified Chinese",
            "fr_FR": "French",
            "es_ES": "Spanish",
            "ja_JP": "Japanese",
        }
        system_prompt = self.LLM_config[self.current_mode[-1:]]  #! Need to change!
        lang = lang_dict.get(General_config["lang"][:5], "English")
        system_prompt = system_prompt.format(lang=lang)
        self.get_text = ""
        Chat_LLM_thread = Chat_LLM(selected_text, system_prompt, self.LLM_config)
        Chat_LLM_thread.text_get.text_get.connect(self.update_text)
        self.threadpool.start(Chat_LLM_thread)

    def update_text(self, text, flag):
        if flag == 1:
            self.get_text += text
            self.text_edit.setText(self.get_text)
            self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
            self.status_bar.showMessage(self.tr("Processing: Normal"))
        elif flag == 2:
            self.get_text += text
            self.text_edit.setText(self.get_text)
            self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
            self.status_bar.showMessage(self.tr("API error"))
            logging.error(f"[API error]: {text}")
        else:
            self.status_bar.showMessage(self.tr("Done"))
            logging.info(f"[Get text]: {self.get_text}")

    def copy_to_clipboard_ui(self):
        text = self.text_edit.toPlainText()
        copy_to_clipboard(text)
        self.tray_icon.showMessage(
            self.tr("Copied to clipboard"),
            text,
            QSystemTrayIcon.MessageIcon.Information,
            2000,
        )

    def closeEvent(self, event):
        event.ignore()
        self.process_flag = False
        self.hide()

    def quit_save_size(self):
        change_one_config("General_config", "width", str(self.width()))
        change_one_config("General_config", "height", str(self.height()))
        change_one_config("General_config", "current_mode", self.current_mode)
        change_one_config("General_config", "current_process_mode", self.current_process_mode)
        change_one_config("General_config", "current_listen_mode", self.current_listen_mode)
        QApplication.instance().quit
        sys.exit()


if __name__ == "__main__":
    #! No wayland support yet
    if sys.platform == "linux":
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    os.makedirs(os.path.expanduser("./log"), exist_ok=True)
    logging.basicConfig(
        filename=os.path.expanduser("./log/smartinput.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    app = QApplication(sys.argv)
    translator = QTranslator()
    General_config = read_config_file(filename="General_config")
    locale = General_config["lang"][:2]
    if translator.load(f"translations_{locale}.qm"):
        app.installTranslator(translator)
    monitor = TextSelectionMonitor(General_config=General_config)
    sys.exit(app.exec())
