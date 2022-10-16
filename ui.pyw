import requests
import time
from os import environ
from PyQt5 import QtCore, QtGui, QtWidgets

vk_token = environ.get('VK_API')
HOST = "https://api.vk.com/method/"


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 120, 231, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 50, 271, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(190, 80, 261, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(190, 170, 261, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(150, 220, 321, 192))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_functions()

    def add_functions(self):
        self.pushButton.clicked.connect(lambda: self.work(self.lineEdit.text().strip().replace('https://vk.com/', '')))

    def work(self, target):
        '''
        Отправляет запросы к API VK, получает id учасников сообщества, выгружает в файл.
        Ограничение API: 3000 id в секунду. 
        Отправляет 3 запроса в секунду, добавляя через offset сдвиг запрашиваемых id.

        '''
        try:
            start_time = time.perf_counter()
            offset = 0
            people_in_target = requests.get(HOST + 'groups.getMembers', params={'group_id': target, 'access_token': vk_token, 'v': 5.131})
            people_1000 = people_in_target.json()['response']['count']
            starting_text = "Количество подписчиков: " + str(people_1000)
            self.textBrowser.append(target)
            self.textBrowser.append(starting_text)
            result_file = open(f"{target}.txt", "w")
            self.progressBar.setMaximum(people_1000 // 1000 + 1)
            for i in range(people_1000 // 1000 + 1):
                time.sleep(0.3)
                answer = requests.get(HOST + 'groups.getMembers', params={'group_id': target, 'offset': offset, 'access_token': vk_token, 'v': 5.131})
                to_write = [*answer.json()['response']['items']]
                offset += 1000
                for item in to_write:
                    print(item, file=result_file, sep='\n')
                self.progressBar.setValue(i + 1)
            result_file.close()
            finish_time = time.perf_counter()
            result_text = "Успех, ID выгружены. " + str(round(finish_time-start_time, 2)) + "сек." + "\n"
            self.textBrowser.append(result_text)
        except KeyError:
            self.textBrowser.setText('Ошибка имени сообщества')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Создание файла для рекламного ретаргета"))
        self.pushButton.setText(_translate("MainWindow", "Выгрузить подписчиков в файл"))
        self.label.setText(_translate("MainWindow", "Введите ID или название сообщества:"))
        self.progressBar.setFormat(_translate("MainWindow", "%p%"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
