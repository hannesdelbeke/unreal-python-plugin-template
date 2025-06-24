from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
import unreal_qt
unreal_qt.setup()  # without this, unreal crashes when creating a widget


class HelloWorldWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = QLabel('Hello', parent=self)
        self.button = QPushButton('OK', parent=self)
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
