from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QMainWindow,QTableWidgetItem,QDialog,QFileDialog,QMessageBox
from screens.Register_ui import Ui_RegisterDialog
from business.Logic import registrarUsuario

class RegisterWindow(QDialog, Ui_RegisterDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.RegistroBtn.clicked.connect(self.RegistroBtnClick)

    def RegistroBtnClick(self):
        username = self.UserTxt.text().strip()
        password = self.PassTxt.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "No puede haber campos vacios")
            return
        if registrarUsuario(username, password):
            QMessageBox.information(self, "Exito", "Registro exitoso")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "El usuario ya existe")