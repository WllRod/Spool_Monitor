from PyQt5.QtGui import QPixmap, QCursor, QFontDatabase, QFont, QPainter, QIcon
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow,
    QWidget, 
    QFrame, 
    QHBoxLayout, 
    QPushButton, 
    QMainWindow,
    QVBoxLayout, 
    QLabel, 
    QLineEdit,
    QProgressBar,
    QDialog,
    QMessageBox)
from PyQt5.QtCore import QSize, QRect, Qt, QDir, QTimer, QDate, pyqtSignal, pyqtSlot
from PyQt5.QtSvg import QSvgRenderer, QSvgWidget
import sys
from subprocess import Popen, CREATE_NEW_CONSOLE, STDOUT, PIPE, DEVNULL
import threading, queue
import os
import time

class Line_Edit(QLineEdit):

    buttonClicked   = pyqtSignal(bool)
    def __init__(self):
        QLineEdit.__init__(self)
        
        self.setMaximumSize(QSize(340, 25))
        self.setStyleSheet("""
        QLineEdit{
            margin-left: 7px;
            background: white;
            border-radius: 4px;
            border: 1px solid;
            border-color: grey;
            font-size: 15px;
        }
        """)
        self.button = QPushButton()
        self.button.setStyleSheet("""
        QPushButton{
            background: transparent;
            border: none;
        }
        """)
        self.button.setIcon(QIcon("assets\\show_password.png"))
        self.button.setIconSize(QSize(40, 50))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setCheckable(True)
        self.button.toggled.connect(self.change_icon)

        layout  = QHBoxLayout(self)
        layout.addWidget(self.button, 0, Qt.AlignRight)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
    
    @pyqtSlot(bool)
    def change_icon(self, checked):
        if(checked):
            self.button.setIcon(QIcon("assets\\hide_password.png"))
        else:
            self.button.setIcon(QIcon("assets\\show_password.png"))

class Login_Screen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARX Sistemas")
        self.setWindowIcon(QIcon("assets\\ico.ico"))
        #t1  = threading.Thread(target=self.r.start)
        #t1.start()
        self.email          = None
        self.password       = None 
        self.password_input = Line_Edit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.handle_password)
        self.password_input.button.clicked.connect(self.change_type)
        self.centralWidget      = QWidget()
        self.centralWidget.setStyleSheet("background-color: rgb(20, 20, 20);")
        self.verticalLayout_1   = QVBoxLayout(self.centralWidget)
        
        self.verticalLayout_1.setContentsMargins(0, 100, 0, 0)
        self.verticalLayout_1.setSpacing(0)
        
        self.label  = QLabel()
        
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(QSize(500, 100))
        w   = self.label.width()
        h   = self.label.height()
        self.pixmap = QPixmap("assets\\logo.png")
        self.label.setPixmap(self.pixmap.scaled(w, h, Qt.KeepAspectRatio))
        self.verticalLayout_1.addWidget(self.label, alignment=Qt.AlignHCenter)
        
        self.frame_1    = QFrame()
        
        self.frame_1.setMinimumSize(QSize(350, 400))
        self.frame_1.setStyleSheet("""
        QFrame{
            border: 1px solid;
            border-color: white;
            color: white;
            border-radius: 2;
            background: rgb(30, 30, 30);
        }
        """)
        self.verticalLayout_login_card  = QVBoxLayout(self.frame_1)
        self.verticalLayout_login_card.setSpacing(0)
        self.verticalLayout_login_card.setContentsMargins(0, 0, 0, 0)
        self.title_label    = QLabel("Log in")
        self.title_label.setStyleSheet("""
        QLabel{
            border: 0;
            font-size: 30px;
        }
        """)
        self.title_label.setMaximumHeight(90)
        self.error_label    = QLabel("Usuário e/ou Senha inválidos")
        self.error_label.setMaximumSize(QSize(340, 50))
        self.error_label.setStyleSheet("""
        QLabel{
            margin-left: 5px;
            font-size: 20px;
            border-color: red;
            color: red;
        }
        """)
        self.error_label.hide()
        self.email_label    = QLabel("Usuário")
        self.email_label.setMaximumHeight(30)
        self.email_label.setStyleSheet("""
        QLabel{
            margin-left: 5px;
            font-size: 20px;
            border: 0;
        }
        """)
        
        self.email_input    = QLineEdit()
        self.email_input.textChanged.connect(self.handle_email)
        self.email_input.setStyleSheet("""
        QLineEdit{
            margin-left: 7px;
            background: white;
            border-radius: 4px;
            border: 1px solid;
            border-color: grey;
            font-size: 15px;
        }
        """)
        self.email_input.setMaximumSize(QSize(340, 25))
        self.password_label = QLabel("Senha")
        self.password_label.setMaximumHeight(30)
        self.password_label.setStyleSheet("""
        QLabel{
            margin-left: 5px;
            font-size: 20px;
            border: 0;
        }
        """)
        
        self.button_frame   = QFrame()
        self.button_frame.setStyleSheet("border: 0;")
        
        self.button_frame.setMaximumHeight(100)

        self.verticalLayout_button_frame    = QVBoxLayout(self.button_frame)
        self.verticalLayout_button_frame.setSpacing(0)
        self.verticalLayout_button_frame.setContentsMargins(0, 0, 0, 0)

        self.button = QPushButton("ENTRAR")
        self.button.clicked.connect(self.submit)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet("""
        QPushButton{
            margin-left: 5px;
            background-color: rgb(75, 160, 245);
            border: 0;
            font-size: 15px;
            border-radius: 2px;
        }
        """)
        self.button.setMaximumSize(QSize(340, 25))
        self.verticalLayout_button_frame.addWidget(self.button)
        self.verticalLayout_login_card.addWidget(self.title_label, alignment=Qt.AlignHCenter)
        self.verticalLayout_login_card.addWidget(self.error_label)
        self.verticalLayout_login_card.addWidget(self.email_label)
        self.verticalLayout_login_card.addWidget(self.email_input)
        self.verticalLayout_login_card.addWidget(self.password_label)
        self.verticalLayout_login_card.addWidget(self.password_input)
        self.verticalLayout_login_card.addWidget(self.button_frame)
        
        

        self.verticalLayout_1.addWidget(self.frame_1, alignment=Qt.AlignCenter)

        self.setCentralWidget(self.centralWidget)
        self.showMaximized()
    def change_type(self, val):
        print(val)
        if(val  == True):
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def handle_email(self, text):
        self.error_label.hide()
        self.email  = text
    
    def handle_password(self, text):
        self.error_label.hide()
        self.password   = text
    
    def submit(self):
        self.close()
    
    def return_password(self):
        return self.password
    # def login(self):
    #     self.q  = queue.Queue()
    #     t1      = threading.Thread(target=self.sql.login, args=(self.email, self.password, self.q,))
    #     t1.start()
    #     if(self.q.get()):
               
    #             perm    = self.sql.return_perm(self.email)[0][0]
                
    #             self.close_actual_window()
                
    #             self.r.hide_screen(perm)
               
                
    #             self.r.start_screen()
    #     else:
    #         self.error_label.show()
    
    def close_actual_window(self):
        self.close()

def start_gui():
    App = QApplication(sys.argv)
    window = Login_Screen()
    App.exec_()
    return window.return_password()