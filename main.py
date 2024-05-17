import sys
import subprocess
from PyQt6.QtGui import QCursor, QCloseEvent, QIcon, QPixmap, QAction
from PyQt6.QtWidgets import QApplication, QLabel, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtCore import QTimer, Qt, QTranslator, QLocale
import os
from Get_Config import read_config_file


class TextSelectionMonitor(QLabel):
    def __init__(self, config):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.ToolTip
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.hide()

        # Check selection every 500ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_selection)
        self.timer.start(500)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        self.tray_icon.setVisible(True)

        self.is_monitoring = True
        self.current_mode = "Mode 0"

        self.create_menu()

        self.previous_text = ""

    def create_menu(self):
        self.menu = QMenu()

        # Toggle monitoring action
        self.toggle_action = QAction(self.tr("开关划线取词"), self)
        self.toggle_action.triggered.connect(self.toggle_monitoring)
        self.menu.addAction(self.toggle_action)

        # Mode selection submenu
        self.mode_menu = QMenu(self.tr("响应模式选择"), self)
        self.mode0_action = QAction(self.tr("智能解析"), self)
        self.mode0_action.setCheckable(True)
        self.mode0_action.triggered.connect(lambda: self.set_mode("Mode 0"))

        self.mode1_action = QAction(self.tr("翻译文本"), self)
        self.mode1_action.setCheckable(True)
        self.mode1_action.triggered.connect(lambda: self.set_mode("Mode 1"))

        self.mode2_action = QAction(self.tr("代码解析"), self)
        self.mode2_action.setCheckable(True)
        self.mode2_action.triggered.connect(lambda: self.set_mode("Mode 2"))

        self.mode_menu.addAction(self.mode0_action)
        self.mode_menu.addAction(self.mode1_action)
        self.mode_menu.addAction(self.mode2_action)
        self.menu.addMenu(self.mode_menu)

        # Exit action
        exit_action = QAction(self.tr("退出"), self)
        exit_action.triggered.connect(QApplication.instance().quit)
        self.menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.update_menu()

    def toggle_monitoring(self):
        self.is_monitoring = not self.is_monitoring
        self.update_menu()

    def set_mode(self, mode):
        self.current_mode = mode
        self.update_menu()

    def update_menu(self):
        self.toggle_action.setText(
            self.tr("开启划线取词")
            if not self.is_monitoring
            else self.tr("关闭划线取词")
        )
        self.mode0_action.setChecked(self.current_mode == "Mode 0")
        self.mode1_action.setChecked(self.current_mode == "Mode 1")
        self.mode2_action.setChecked(self.current_mode == "Mode 2")

    def check_selection(self):
        try:
            selected_text = (
                subprocess.check_output(["xclip", "-o", "-selection", "primary"])
                .decode("utf-8")
                .strip()
            )
            if selected_text != self.previous_text:
                self.previous_text = selected_text
                processed_text = self.deal(selected_text)
                if processed_text:
                    print(processed_text)
                    self.setText(processed_text)
                    self.adjustSize()
                    self.move(QCursor.pos())
                    self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
                    self.show()
                else:
                    self.hide()
        except subprocess.CalledProcessError:
            self.hide()

    def deal(self, text):
        return f"Processed: {text}"


if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QApplication(sys.argv)
    translator = QTranslator()
    print(QLocale.system().name())
    config = read_config_file()
    locale = config["lang"][2:]
    if translator.load(f"translations_{locale}.qm"):
        app.installTranslator(translator)
    monitor = TextSelectionMonitor(config=config)
    sys.exit(app.exec())
