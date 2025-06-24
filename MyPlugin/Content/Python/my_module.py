from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
import unreal_qt
unreal_qt.setup()  # without this, unreal crashes when creating a widget


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
