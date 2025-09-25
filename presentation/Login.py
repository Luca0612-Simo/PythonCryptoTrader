from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QMainWindow,QTableWidgetItem,QDialog,QFileDialog,QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence
from screens.Login_ui import Ui_MainWindow
import sys 
from business.Logic import login
from presentation.Register import RegisterWindow
class LoginWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.IngresarBtn.clicked.connect(self.IngresarBtnClick)
        self.RegistrarseBtn.clicked.connect(self.RegistrarseBtnClick)

    def IngresarBtnClick(self):
        username = self.UserTxt.text().strip()
        password = self.PassTxt.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "No puede haber campos vacios")
            return
        
        if login(username, password):
            QMessageBox.information(self, "Exito", "Login exitoso")

        else:
            QMessageBox.warning(self, "Error", "Datos incorrectos")

    def RegistrarseBtnClick(self):
        dialog = RegisterWindow()
        if dialog.exec():
            QMessageBox.information(self, "Listo", "Ahora inicie sesion")