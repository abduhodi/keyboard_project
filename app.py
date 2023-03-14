from widgets.main import MainWindow
from widgets.sign_in import SignIn
from widgets.sign_up import SignUp
from PyQt6.QtWidgets import QApplication
import sys



if __name__ == "__main__":
    app = QApplication(sys.argv)

    sign_in = SignIn()
    sign_up = SignUp()
    main = MainWindow()

    def signin():
        main.user = sign_in.user
        main.update_score_label(main.user)
        point = sign_in.get_point()
        main.setGeometry(point[0], point[1], 720, 550)
    
    def signup():
        main.user = sign_up.user
        main.update_score_label(main.user)
        point = sign_up.get_point()
        main.setGeometry(point[0], point[1], 720, 550)
    
    def main_def():
       point = main.get_point()
       sign_in.setGeometry(point[0], point[1], 400, 500)

    def signin_geo():
        point = sign_in.get_point()
        sign_up.setGeometry(point[0], point[1], 400, 500)
    
    def signup_geo():
        point = sign_up.get_point()
        sign_in.setGeometry(point[0], point[1], 400, 500)

    
    sign_in.show()
    
    sign_in.signal.sign_up_signal.connect(sign_up.show)
    sign_in.signal.sign_up_signal.connect(signin_geo)
    sign_in.signal.main_signal.connect(main.show)
    sign_in.signal.main_signal.connect(signin)
    
    sign_up.signal.sign_in_signal.connect(sign_in.show)
    sign_up.signal.sign_up_signal.connect(signup_geo)
    sign_up.signal.main_signal.connect(main.show)
    sign_up.signal.main_signal.connect(signup)

    main.signal.close.connect(sign_in.show)
    main.signal.close.connect(main_def)

    sys.exit(app.exec())