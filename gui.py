import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signupbutton.clicked.connect(self.gotosignup)

    def loginfunction(self):
        username = self.username.text()
        password = self.password.text()
        print("Successfully logged in with email: ", username, "and password:", password)

    def gotosignup(self):
        signup = SignUp()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class SignUp(QDialog):
    def __init__(self):
        super(SignUp, self).__init__()
        loadUi("signup.ui", self)
        self.signupbutton.clicked.connect(self.signupfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def signupfunction(self):
        username = self.username.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            print("Successfully created acc with email: ", username, "and password: ", password)
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1000)
widget.setFixedHeight(800)
widget.show()
app.exec_()
