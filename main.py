import sys
import subprocess
from PyQt6.QtGui import QCursor, QIcon, QAction, QFont
from PyQt6.QtWidgets import QApplication, QLabel, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, Qt, QTranslator
import os
from Get_Config import read_config_file
from Chat_LLM import predict


class TextSelectionMonitor(QLabel):
    def __init__(self, config):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.ToolTip
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.hide()
        self.setFont(QFont(config["font"], int(config["font_size"])))

        # Check selection every 500ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_selection)
        self.timer.start(500)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip("Smartinput")

        self.is_monitoring = True
        self.current_mode = "Mode 0"

        self.create_menu()

        self.previous_text = self.get_selected_text()
        self.lastMoveTime = 0
        self.moveInterval = 200

    def create_menu(self):
        self.menu = QMenu()

        # Toggle monitoring action
        self.toggle_action = QAction(self.tr("Text selection ON/OFF"), self)
        self.toggle_action.triggered.connect(self.toggle_monitoring)
        self.menu.addAction(self.toggle_action)

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
        exit_action.triggered.connect(QApplication.instance().quit)
        self.menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.update_menu()

        self.wait_cursor = 0

    def toggle_monitoring(self):
        self.is_monitoring = not self.is_monitoring
        if self.is_monitoring:
            self.timer.start(500)
        else:
            self.timer.stop()
        self.update_menu()

    def set_mode(self, mode):
        self.current_mode = mode
        self.update_menu()

    def update_menu(self):
        self.toggle_action.setText(
            self.tr("Trun on text selection")
            if not self.is_monitoring
            else self.tr("Trun off text selection")
        )
        self.mode0_action.setChecked(self.current_mode == "Mode 0")
        self.mode1_action.setChecked(self.current_mode == "Mode 1")
        self.mode2_action.setChecked(self.current_mode == "Mode 2")

    def check_selection(self):
        try:
            selected_text = ()
            if self.wait_cursor < 5:
                self.wait_cursor += 1
                return
            selected_text = self.get_selected_text()
            if selected_text != self.previous_text:
                self.set_text(selected_text)
        except subprocess.CalledProcessError:
            self.hide()

    def set_text(self, selected_text):
        self.timer.stop()
        self.wait_cursor = 0
        self.previous_text = selected_text
        self.show()
        self.move(QCursor.pos())
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setText(str(self.tr("Process...Please wait")))
        self.adjustSize()
        QApplication.processEvents()
        processed_text = ""

        try:
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
            for processed_text_temp in self.deal(selected_text, system_prompt):
                processed_text += processed_text_temp
                #! If use stream the window size will be changed too fast....
                # self.setText(processed_text)
                # self.adjustSize()
            self.setText(self.final_text(processed_text))
            self.adjustSize()
            self.timer.start(500)
        except Exception as e:
            self.setText(str(e))
            self.adjustSize()
            self.timer.start(500)
            return

    def deal(self, text, system_prompt):
        for get_text in predict(
            inputs=text, llm_kwargs=config, history=[], system_prompt=system_prompt
        ):
            yield get_text

    def final_text(self, text):
        lines = text.split("\n")
        processed_lines = []
        for line in lines:
            if len(line) <= 100:
                processed_lines.append(line)
            else:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line + word) <= 100:
                        current_line += word + " "
                    else:
                        processed_lines.append(current_line.strip())
                        current_line = word + " "
                if current_line:
                    processed_lines.append(current_line.strip())
        return "\n".join(processed_lines)

    def get_selected_text(self):
        return (
            subprocess.check_output(["xclip", "-o", "-selection", "primary"])
            .decode("utf-8")
            .strip()
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPosition = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()
        elif event.button() == Qt.MouseButton.RightButton:
            self.hide()

    def mouseMoveEvent(self, event):
        currentTime = event.timestamp()
        if (
            event.buttons() & Qt.MouseButton.LeftButton
            and (currentTime - self.lastMoveTime) > self.moveInterval
        ):
            self.move(event.globalPosition().toPoint() - self.dragPosition)
            self.lastMoveTime = currentTime
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.text())
            self.tray_icon.showMessage(
                self.tr("Copied to clipboard"),
                self.text(),
                QSystemTrayIcon.MessageIcon.Information,
            )


if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QApplication(sys.argv)
    translator = QTranslator()
    config = read_config_file()
    locale = config["lang"][:2]
    if translator.load(f"translations_{locale}.qm"):
        app.installTranslator(translator)
    monitor = TextSelectionMonitor(config=config)
    sys.exit(app.exec())
