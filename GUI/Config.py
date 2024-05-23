from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSlider,
    QTabWidget
)
from PyQt6.QtCore import Qt

def Text_input(parent, title, description, default_text=""):
    """
    A text input control is generated.
    """
    layout = QVBoxLayout()
    title_label = QLabel(title, parent)
    title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
    layout.addWidget(title_label)
    description_label = QLabel(description, parent)
    description_label.setStyleSheet("font-size: 12px; color: gray;")
    layout.addWidget(description_label)
    text_input = QLineEdit(parent)
    text_input.setText(default_text)
    layout.addWidget(text_input)
    return layout

def Select(parent, title, description, options, default_index=0):
    """
    A drop-down selection control is generated.
    """
    layout = QVBoxLayout()
    title_label = QLabel(title, parent)
    title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
    layout.addWidget(title_label)
    description_label = QLabel(description, parent)
    description_label.setStyleSheet("font-size: 12px; color: gray;")
    layout.addWidget(description_label)
    select = QComboBox(parent)
    select.addItems(options)
    select.setCurrentIndex(default_index)
    layout.addWidget(select)
    return layout

def Select_2(parent, title, description, min_value, max_value, default_value):
    """
    A slider control is generated.
    """
    layout = QVBoxLayout()
    title_label = QLabel(title, parent)
    title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
    layout.addWidget(title_label)
    description_label = QLabel(description, parent)
    description_label.setStyleSheet("font-size: 12px; color: gray;")
    layout.addWidget(description_label)
    slider = QSlider(Qt.Orientation.Horizontal, parent)
    slider.setRange(min_value, max_value)
    slider.setValue(default_value)
    layout.addWidget(slider)
    value_label = QLabel(str(default_value), parent)
    layout.addWidget(value_label)
    return layout

class Config(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("Configuration"))
        self.resize(800, 500)

        self.tab_widget = QTabWidget()

        self.tab_general = QWidget()
        self.tab_LLM = QWidget()

        self.tab_widget.addTab(self.tab_general, self.tr("General"))
        self.tab_widget.addTab(self.tab_LLM, self.tr("Model"))

        self.layout_general = QVBoxLayout()
        self.layout_LLM = QVBoxLayout()

        # Setting of the general tab
        self.layout_general.addLayout(Text_input(self, self.tr("Title"), self.tr("Please enter the title.")))
        self.layout_general.addLayout(Select(self, self.tr("Language"), self.tr("Please select the language."), ["English", "Chinese"]))
        self.layout_general.addLayout(Select_2(self, self.tr("Volume"), self.tr("Please adjust the volume."), 0, 100, 50))

        # Setting of the LLM tab
        self.layout_LLM.addLayout(Text_input(self, self.tr("Title"), self.tr("Please enter the title.")))
        self.layout_LLM.addLayout(Select(self, self.tr("Language"), self.tr("Please select the language."), ["English", "Chinese"]))
        self.layout_LLM.addLayout(Select_2(self, self.tr("Volume"), self.tr("Please adjust the volume."), 0, 100, 50))


        self.tab_general.setLayout(self.layout_general)
        self.tab_LLM.setLayout(self.layout_LLM)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)
        
app = QApplication([])
window = Config()
window.show()
app.exec()