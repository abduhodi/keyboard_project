from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from widgets.signals import MySignals
from widgets.check import Check
from widgets.user import User
from widgets.db import Database
import threading
from img import resources



class SignIn(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.check_thread = threading.Thread(target=self.check)

        self.data = []

        self.setWindowTitle("Sign in")
        self.setWindowIcon(QIcon(":/icons/user.png"))
        self.setGeometry(500, 150, 400, 500)
        self.setFixedSize(400, 500)
        self.setSignInWindow()
        self.signal = MySignals()


    def showEvent(self, a0: QShowEvent) -> None:
        del self.check_thread
        self.check_thread = threading.Thread(target=self.check)
        self.check_thread.start()


    def get_point(self):
        x = self.geometry().topLeft().x()
        y = self.geometry().topLeft().y()
        return (x, y)


    def setSignInWindow(self):
        input_style = """
        QLineEdit{
        max-width: 300px;
        height: 30px;
        border-radius: 8px;
        outline: none;
        border: 1px solid grey;
        font-size: 18px;
        }
        QLineEdit:focus{
        border: 1px solid green;
        }
        """

        button_style = """
        QPushButton{
        max-width: 200px;
        height: 35px;
        border-radius: 16px;

        font-size: 18px;
        background-color: #362FD9;
        color: white;
        }
        QPushButton:hover{
        background-color: #0ea4ef;
        color: #060047;
        }
        """

        self.header = QLabel('')
        self.header.setPixmap(QPixmap(":/icons/header.png").scaled(100, 100))
        self.header.setFixedSize(100, 100)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.header)

        self.email_label = QLabel('')
        self.email_label.setPixmap(QPixmap(":/icons/email.png").scaled(25, 25))
        self.email_label.setStyleSheet("padding-left: 1.5px;")
        self.email_label.setFixedSize(30, 30)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@gmail.com")
        self.email_input.setStyleSheet(input_style)

        email_layout = QHBoxLayout()
        email_layout.addSpacing(20)
        email_layout.addWidget(self.email_label)
        email_layout.addWidget(self.email_input)
        email_layout.addSpacing(25)


        self.passwd_label = QLabel('')
        self.passwd_label.setPixmap(QPixmap(":/icons/padlock.png").scaled(25, 25))
        self.passwd_label.setStyleSheet("padding-left: 1.5px;")
        self.passwd_label.setFixedSize(30, 30)

        self.passwd_input = QLineEdit()
        self.passwd_input.setPlaceholderText("********")
        self.passwd_input.setStyleSheet(input_style)
        self.passwd_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.passwd_view = QPushButton(QIcon(":/icons/hide.png"), '')
        self.passwd_view.setFixedSize(20, 20)
        self.passwd_view.setStyleSheet("background-color: transparent;")
        self.passwd_view.clicked.connect(self.unhide)
        

        passwd_layout = QHBoxLayout()
        passwd_layout.addSpacing(20)
        passwd_layout.addWidget(self.passwd_label)
        passwd_layout.addWidget(self.passwd_input)
        passwd_layout.addWidget(self.passwd_view)


        self.sign_in_button = QPushButton("Sign in")
        self.sign_in_button.setStyleSheet(button_style)
        self.sign_in_button.clicked.connect(self.sign_in)

        sign_in_btn_layout = QHBoxLayout()
        sign_in_btn_layout.addWidget(self.sign_in_button)


        self.register_button = QPushButton("Register now")
        self.register_button.setStyleSheet(button_style)
        self.register_button.clicked.connect(self.register)

        register_btn_layout = QHBoxLayout()
        register_btn_layout.addWidget(self.register_button)



        layout = QVBoxLayout()
        layout.addSpacing(30)
        layout.addLayout(header_layout)
        layout.addLayout(email_layout)
        layout.addLayout(passwd_layout)
        layout.addLayout(sign_in_btn_layout)
        layout.addLayout(register_btn_layout)
        layout.addSpacing(50)


        center = QWidget()
        center.setStyleSheet("""
        background-color: #ffffff;
        """)

        center.setLayout(layout)
        self.setCentralWidget(center)


    def unhide(self):
        if self.passwd_input.echoMode().name =="Password":
            self.passwd_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.passwd_view.setIcon(QIcon(":/icons/eye.png"))
        elif self.passwd_input.echoMode().name =="Normal":
            self.passwd_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.passwd_view.setIcon(QIcon(":/icons/hide.png"))


    def check(self):
        db = Database()
        self.data = db.read()

    
    def sign_in(self):
        if not Check.is_valid_email(self.email_input.text()):
            self.email_input_error = QMessageBox.critical(self, "Email error", "Email input error!")
        elif not Check.is_valid_passwd(self.passwd_input.text()):
            self.passwd_input_error = QMessageBox.critical(self, "Password error", "Password input error!")
        else:
            data = ()
            for user in self.data:
                if self.email_input.text() == user[2] and self.passwd_input.text() == user[4]:
                    data = user
                    break
            if data:
                self.user = User(
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8]
                )
                QMessageBox.about(self, "logged in", "You are logged in")
                self.email_input.clear()
                self.passwd_input.clear()
                self.signal.main_signal.emit()
                self.close()
            else:
                QMessageBox.about(self, "not registered", "Email or Password did not match Maybe You are not registered yet")
            
    @staticmethod
    def get_user(self) -> User:
        return self.user


    def register(self):
        self.email_input.clear()
        self.passwd_input.clear()
        self.signal.sign_up_signal.emit()
        self.close()

    
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape.value:
            self.close()