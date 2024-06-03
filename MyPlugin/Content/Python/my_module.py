import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout


class HelloWorldWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel('Hello')
        self.button = QPushButton('OK')
        self.button.clicked.connect(self.print_hello)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def print_hello(self):
        print('Hello')


def show():
  widget = HelloWorldWidget()
  widget.show()
  return widget
