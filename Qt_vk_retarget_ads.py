import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

import vk_retarget_ads


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(640, 480))

        self.setWindowTitle("vk retarget")
        button = QPushButton("Выгрузить")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        vk_retarget_ads.test()
        print("Clicked!")


app = QApplication(sys.argv)


window = MainWindow()
window.show()

app.exec()
