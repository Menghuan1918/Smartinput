import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QLabel, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QCursor, QCloseEvent, QIcon, QPixmap

import os


class TextSelectionMonitor(QLabel):
    def __init__(self):
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
        self.tray_icon.setIcon(QIcon("logo.png"))
        self.tray_icon.setVisible(True)

        menu = QMenu()

        self.previous_text = ""

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
    monitor = TextSelectionMonitor()
    sys.exit(app.exec())
