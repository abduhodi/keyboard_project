from PyQt6 import QtCore, QtGui, QtWidgets
import time
import threading
from widgets.keyboard_module import KeyboardWidget
import random
from widgets.user import User
from widgets.db import Database
from widgets.signals import MySignals
from img import resources


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.user = User('default', 'default', 'default', 'default')
        self.db = Database()
        self.signal = MySignals()

        self.speed = 0.009

        self.latin = "ABCDEFGHIJKLMNOPQRSTUVWXVZabcdefghijklmnopqrstuvwxvz"
        self.crylic = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
        self.lang = self.latin
        self.type = 'en'
        self.keyboard = KeyboardWidget(self.type)
        self.keyboard.setStyleSheet("border: 1px solid #333; border-radius: 10px")

        self.time = threading.Thread(target=self.count_down)
        self.run = threading.Thread(target=self.run_letter)
        self.save = threading.Thread(target=self.save_to_server, args=(self.user,))

        self.breaker = False

        self.setObjectName("MainWindow")
        self.resize(720, 550)
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: white;")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.runningWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.runningWidget.setMinimumSize(QtCore.QSize(670, 200))
        self.runningWidget.setMaximumSize(QtCore.QSize(16667, 200))
        self.runningWidget.setObjectName("runningWidget")
        self.runningWidget.setStyleSheet("border: 1px solid #333; border-radius: 10px")

        self.runningWidget_layout = QtWidgets.QHBoxLayout()
        self.runningWidget_layout.addStretch()
        self.runningWidget_layout.addWidget(self.runningWidget)
        self.runningWidget_layout.addStretch()

        self.gridLayout.addLayout(self.runningWidget_layout, 0, 0, 1, 1)

        self.running_letter = QtWidgets.QLabel(parent=self.runningWidget)
        self.running_letter.setText("")
        self.running_letter.setStyleSheet("font-size: 18px; font-weight: 600; border: none")
        self.running_letter.setGeometry(5, 5, 25, 25)



        self.keyboard_layout = QtWidgets.QHBoxLayout()
        self.keyboard_layout.addStretch()
        self.keyboard_layout.addWidget(self.keyboard)
        self.keyboard_layout.addStretch()
        self.gridLayout.addLayout(self.keyboard_layout, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.score_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.score_label.setMinimumSize(QtCore.QSize(200, 40))
        self.score_label.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.score_label.setFont(font)
        self.score_label.setObjectName("score_label")
        self.horizontalLayout.addWidget(self.score_label)
        self.topScore_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.topScore_label.setMinimumSize(QtCore.QSize(200, 40))
        self.topScore_label.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.topScore_label.setFont(font)
        self.topScore_label.setObjectName("topScore_label")
        self.horizontalLayout.addWidget(self.topScore_label)
        self.time_label = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.time_label.setFont(font)
        self.time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_label.setObjectName("time_label")
        self.horizontalLayout.addWidget(self.time_label)
        self.time_lcd = QtWidgets.QLCDNumber(parent=self.centralwidget)
        self.time_lcd.setMinimumSize(QtCore.QSize(60, 25))
        self.time_lcd.setMaximumSize(QtCore.QSize(100, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.time_lcd.setFont(font)
        self.time_lcd.setStyleSheet("")
        self.time_lcd.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.time_lcd.setLineWidth(1)
        self.time_lcd.setMidLineWidth(0)
        self.time_lcd.setDigitCount(2)
        self.time_lcd.setProperty("intValue", 60)
        self.time_lcd.setObjectName("time_lcd")
        self.horizontalLayout.addWidget(self.time_lcd)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 719, 21))
        self.menubar.setObjectName("menubar")
        self.menuDifficulty = QtWidgets.QMenu(parent=self.menubar)
        self.menuDifficulty.setObjectName("menuDifficulty")
        self.menuLang = QtWidgets.QMenu(parent=self.menubar)
        self.menuLang.setObjectName("menuLang")
        self.menu_Help = QtWidgets.QMenu(parent=self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.setMenuBar(self.menubar)
        self.action_help = QtGui.QAction(parent=self)
        self.action_help.setObjectName("action_help")
        self.actionEnglish = QtGui.QAction(parent=self)
        self.actionEnglish.setObjectName("actionEnglish")
        self.action_Ru = QtGui.QAction(parent=self)
        self.action_Ru.setObjectName("action_Ru")
        self.action_Easy = QtGui.QAction(parent=self)
        self.action_Easy.setObjectName("action_Easy")
        self.action_Medium = QtGui.QAction(parent=self)
        self.action_Medium.setObjectName("action_Medium")
        self.action_Hard = QtGui.QAction(parent=self)
        self.action_Hard.setObjectName("action_Hard")
        self.action_Expert = QtGui.QAction(parent=self)
        self.action_Expert.setObjectName("action_Expert")

        self.action_Expert.triggered.connect(lambda: self.click("expert"))
        self.action_Hard.triggered.connect(lambda: self.click("hard"))
        self.action_Medium.triggered.connect(lambda: self.click("medium"))
        self.action_Easy.triggered.connect(lambda: self.click("easy"))
        self.action_Ru.triggered.connect(lambda: self.click("ru"))
        self.actionEnglish.triggered.connect(lambda: self.click("en"))
        self.action_help.triggered.connect(self.help_form)


        self.menuDifficulty.addAction(self.action_Easy)
        self.menuDifficulty.addAction(self.action_Medium)
        self.menuDifficulty.addAction(self.action_Hard)
        self.menuDifficulty.addAction(self.action_Expert)
        self.menuLang.addAction(self.actionEnglish)
        self.menuLang.addAction(self.action_Ru)
        self.menu_Help.addAction(self.action_help)
        self.menubar.addAction(self.menuDifficulty.menuAction())
        self.menubar.addAction(self.menuLang.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowTitle("Keyboard Game")
        self.setWindowIcon(QtGui.QIcon(":/icons/typing.png"))
        self.score_label.setText("Score: 0")
        self.topScore_label.setText("Highest score: 0")
        self.time_label.setText("Time: ")
        self.menuDifficulty.setTitle("Difficulty")
        self.menuLang.setTitle("Lang")
        self.menu_Help.setTitle(" Help")
        self.action_help.setText(" About")
        self.actionEnglish.setText("En")
        self.actionEnglish.setCheckable(True)
        self.actionEnglish.setChecked(True)
        self.action_Ru.setText(" Ru")
        self.action_Ru.setCheckable(True)
        self.action_Easy.setText(" Easy")
        self.action_Easy.setCheckable(True)
        self.action_Medium.setText(" Medium")
        self.action_Medium.setCheckable(True)
        self.action_Medium.setChecked(True)
        self.action_Hard.setText(" Hard")
        self.action_Hard.setCheckable(True)
        self.action_Expert.setText(" Expert")
        self.action_Expert.setCheckable(True)
        self.start_label = QtWidgets.QLabel(parent=self.runningWidget)
        self.start_label.setText("Press Enter to Start")
        self.start_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.start_label.setStyleSheet("font-size: 24px; font-weight: 500; color: #333; border: none")
        self.start_label.setGeometry(100, 80, 470, 40)


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.signal.close.emit()

    def get_point(self):
        x = self.geometry().topLeft().x()
        y = self.geometry().topLeft().y()
        return (x, y)

    def help_form(self):
        self.help = QtWidgets.QMessageBox.about(self, "Help", "You can set difficulty and language on menu bar\nPress Esc button to stop game anytime\nAuthor: Abduhodi Tursunboyev\nMentor: Azmiddin Qurbonov\nCreated: 14/03/2023")


    def click(self, text):
        if text == "expert":
            self.action_Easy.setChecked(False)
            self.action_Medium.setChecked(False)
            self.action_Hard.setChecked(False)
            self.speed = 0.003
            self.topScore_label.setText(f"Highest score: {self.user.expert}")
        elif text == "hard":
            self.action_Easy.setChecked(False)
            self.action_Medium.setChecked(False)
            self.action_Expert.setChecked(False)
            self.speed = 0.006
            self.topScore_label.setText(f"Highest score: {self.user.hard}")
        elif text == "medium":
            self.action_Easy.setChecked(False)
            self.action_Hard.setChecked(False)
            self.action_Expert.setChecked(False)
            self.speed = 0.009
            self.topScore_label.setText(f"Highest score: {self.user.medium}")
        elif text == "easy":
            self.action_Medium.setChecked(False)
            self.action_Hard.setChecked(False)
            self.action_Expert.setChecked(False)
            self.speed = 0.02
            self.topScore_label.setText(f"Highest score: {self.user.easy}")
        elif text == "ru":
            self.actionEnglish.setChecked(False)
            self.lang = self.crylic
            self.type = 'ru'
            self.keyboard.ru_keyboard()
            self.start_label.setText("Нажмите Enter, чтобы начать")
        elif text == "en":
            self.action_Ru.setChecked(False)
            self.lang = self.latin
            self.type = 'en'
            self.keyboard.en_keyboard()
            self.start_label.setText("Press Enter to Start")


    def update_score_label(self, user: User):
        self.topScore_label.setText(f"Highest score: {user.medium}")


    def run_letter(self):
        while self.time_lcd.intValue():
            self.breaker = False
            self.running_letter.setText(random.choice(self.lang))
            x = random.randint(0, self.runningWidget.width() - 25)
            self.running_letter.setGeometry(x, 0, 25, 25)
            h = self.runningWidget.height() - 25
            for i in range(h):
                if self.breaker:
                    break
                self.running_letter.setGeometry(x, i, 25, 25)
                time.sleep(self.speed)
            else:
                self.score_minus()

        self.time_up()
        

    def time_up(self):
        score = int(self.score_label.text().split()[1])
        top = int(self.topScore_label.text().split()[-1])
        if score > top:
            self.topScore_label.setText(f"Highest score: {score}")

            if self.action_Easy.isChecked():
                self.user.easy = score
            elif self.action_Medium.isChecked():
                self.user.medium = score
            elif self.action_Hard.isChecked():
                self.user.hard = score
            elif self.action_Expert.isChecked():
                self.user.expert = score

            del self.save
            self.save = threading.Thread(target=self.save_to_server, args=(self.user,))
            self.save.start()

        self.score_label.setText("Score: 0")
        self.start_label.show()
        self.running_letter.hide()
    

    def save_to_server(self, user: User):
        if self.db.update(user):
            print("UPDATE SCORE")
        else:
            print("UPDATE FAILED!")

        
    def count_down(self):
        while self.time_lcd.intValue():
            value = self.time_lcd.intValue()
            self.time_lcd.setProperty("intValue", value - 1)
            time.sleep(1)


    def score_up(self):
        score = int(self.score_label.text().split()[1])
        self.score_label.setText(f"Score: {score + 1}")


    def score_minus(self):
        score = int(self.score_label.text().split()[1])
        self.score_label.setText(f"Score: {score - 1}")


    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        key = event.text()
        code = event.key()
        print("pressed", code)

        if self.time.is_alive():
            if self.running_letter.text() == key and code != 16777220:
                self.breaker = True
                self.score_up()
            elif code not in [32, 16777251, 16777249, 16777248, 16777252, 16777217, 16777219, 16777234, 16777235, 16777236, 16777237, 16777220, 16777216]:
                self.score_minus()


        if code == 16777220:
            self.keyboard.label_enter.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
            if not self.time.is_alive():
                if self.time_lcd.intValue() == 0:
                    del self.time
                    del self.run
                    self.time = threading.Thread(target=self.count_down)
                    self.run = threading.Thread(target=self.run_letter)
                self.time_lcd.setProperty("intValue", 60)
                self.time.start()
                self.run.start()
                self.start_label.hide()
                self.running_letter.show()


        elif code == 16777216:
            self.time_lcd.setProperty("intValue", 0)
            self.breaker = True
            

        elif code == 96 or code == 126:
            self.keyboard.label_yo.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 49 or code == 33:
            self.keyboard.label_1.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 50 or code == 64:
            self.keyboard.label_2.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 51 or code == 35:
            self.keyboard.label_3.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 52 or code == 36:
            self.keyboard.label_4.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 53 or code == 37:
            self.keyboard.label_5.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 54 or code == 94:
            self.keyboard.label_6.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 55 or code == 38:
            self.keyboard.label_7.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 56 or code == 42:
            self.keyboard.label_8.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 57 or code == 40:
            self.keyboard.label_9.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 48 or code == 41:
            self.keyboard.label_0.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 45 or code == 95:
            self.keyboard.label_minus.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 61 or code == 43:
            self.keyboard.label_equal.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777219:
            self.keyboard.label_backspace.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777217:
            self.keyboard.label_tab.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 65:
            self.keyboard.label_A.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 66:
            self.keyboard.label_B.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 67:
            self.keyboard.label_C.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 68:
            self.keyboard.label_D.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 69:
            self.keyboard.label_E.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 70:
            self.keyboard.label_F.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 71:
            self.keyboard.label_G.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 72:
            self.keyboard.label_H.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 73:
            self.keyboard.label_I.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 74:
            self.keyboard.label_J.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 75:
            self.keyboard.label_K.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 76:
            self.keyboard.label_L.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 77:
            self.keyboard.label_M.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 78:
            self.keyboard.label_N.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 79:
            self.keyboard.label_O.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 80:
            self.keyboard.label_P.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 81:
            self.keyboard.label_Q.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 82:
            self.keyboard.label_R.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 83:
            self.keyboard.label_S.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 84:
            self.keyboard.label_T.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 85:
            self.keyboard.label_U.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 86:
            self.keyboard.label_V.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 87:
            self.keyboard.label_W.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 88:
            self.keyboard.label_X.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 89:
            self.keyboard.label_Y.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 90:
            self.keyboard.label_Z.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 91:
            self.keyboard.label_left_bracket.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 93:
            self.keyboard.label_right_bracket.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 92:
            self.keyboard.label_backslash.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777252:
            self.keyboard.label_caps.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777248:
            self.keyboard.label_left_shift.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
            self.keyboard.label_right_shift.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777249:
            self.keyboard.label_left_ctrl.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
            self.keyboard.label_right_ctrl.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777251:
            self.keyboard.label_left_alt.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
            self.keyboard.label_right_alt.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 32:
            self.keyboard.label_space.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")       
        elif code == 16777234:
            self.keyboard.label_left.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777235:
            self.keyboard.label_up.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777236:
            self.keyboard.label_right.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777237:
            self.keyboard.label_down.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 59:
            self.keyboard.label_semicolon.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 39:
            self.keyboard.label_parantecy.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 44:
            self.keyboard.label_colon.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 46:
            self.keyboard.label_dot.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
        elif code == 47:
            self.keyboard.label_forwardslash.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 1px solid grey;")
       

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        key = event.text()
        code = event.key()
        # print("released", key, code)
        if code == 96 or code == 126:
            self.keyboard.label_yo.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 49 or code == 33:
            self.keyboard.label_1.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 50 or code == 64:
            self.keyboard.label_2.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 51 or code == 35:
            self.keyboard.label_3.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 52 or code == 36:
            self.keyboard.label_4.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 53 or code == 37:
            self.keyboard.label_5.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 54 or code == 94:
            self.keyboard.label_6.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 55 or code == 38:
            self.keyboard.label_7.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 56 or code == 42:
            self.keyboard.label_8.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 57 or code == 40:
            self.keyboard.label_9.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 48 or code == 41:
            self.keyboard.label_0.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 45 or code == 95:
            self.keyboard.label_minus.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 61 or code == 43:
            self.keyboard.label_equal.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777219:
            self.keyboard.label_backspace.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777217:
            self.keyboard.label_tab.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 65:
            self.keyboard.label_A.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 66:
            self.keyboard.label_B.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;; border-radius: 5px; border: 1px solid grey;")
        elif code == 67:
            self.keyboard.label_C.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;; border-radius: 5px; border: 1px solid grey;")
        elif code == 68:
            self.keyboard.label_D.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;; border-radius: 5px; border: 1px solid grey;")
        elif code == 69:
            self.keyboard.label_E.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;; border-radius: 5px; border: 1px solid grey;")
        elif code == 70:
            self.keyboard.label_F.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;; border-radius: 5px; border: 1px solid grey;")
        elif code == 71:
            self.keyboard.label_G.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;; border-radius: 5px; border: 1px solid grey;")
        elif code == 72:
            self.keyboard.label_H.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;; border-radius: 5px; border: 1px solid grey;")
        elif code == 73:
            self.keyboard.label_I.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;; border-radius: 5px; border: 1px solid grey;")
        elif code == 74:
            self.keyboard.label_J.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 75:
            self.keyboard.label_K.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 76:
            self.keyboard.label_L.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 77:
            self.keyboard.label_M.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 78:
            self.keyboard.label_N.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 79:
            self.keyboard.label_O.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 80:
            self.keyboard.label_P.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 81:
            self.keyboard.label_Q.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 82:
            self.keyboard.label_R.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 83:
            self.keyboard.label_S.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 84:
            self.keyboard.label_T.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 85:
            self.keyboard.label_U.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 86:
            self.keyboard.label_V.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 87:
            self.keyboard.label_W.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 88:
            self.keyboard.label_X.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 89:
            self.keyboard.label_Y.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 90:
            self.keyboard.label_Z.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 91:
            self.keyboard.label_left_bracket.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 93:
            self.keyboard.label_right_bracket.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 92:
            self.keyboard.label_backslash.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777252:
            self.keyboard.label_caps.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777248:
            self.keyboard.label_left_shift.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
            self.keyboard.label_right_shift.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777249:
            self.keyboard.label_left_ctrl.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
            self.keyboard.label_right_ctrl.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777251:
            self.keyboard.label_left_alt.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
            self.keyboard.label_right_alt.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 32:
            self.keyboard.label_space.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777220:
            self.keyboard.label_enter.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777234:
            self.keyboard.label_left.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777235:
            self.keyboard.label_up.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777236:
            self.keyboard.label_right.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 16777237:
            self.keyboard.label_down.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 59:
            self.keyboard.label_semicolon.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 39:
            self.keyboard.label_parantecy.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 44:
            self.keyboard.label_colon.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 46:
            self.keyboard.label_dot.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
        elif code == 47:
            self.keyboard.label_forwardslash.setStyleSheet("background-color: white; color: black; border-radius: 5px; border: 1px solid grey;")
