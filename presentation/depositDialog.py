from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QMainWindow,QTableWidgetItem,QDialog,QFileDialog,QMessageBox
from business import Logic
from decimal import Decimal
from screens.depositDialog_ui import Ui_Dialog

class DepositDialog (QDialog, Ui_Dialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.username = username

        self.DepositBtn.clicked.connect(self.DepositBtnClick)

    def DepositBtnClick(self):
        try:
            monto = Decimal(self.depositTxt.text())
            if monto <= 0:
                QMessageBox.warning(self, "Error", "No podes ingresar una cantidad menor a cero")
                return
        except:
            QMessageBox.warning(self, "Error", "Monto invalido")
            return
        
        try:
            Logic.depositar(self.username, monto)
            QMessageBox.information(self, "Exito", "El deposito se hizo correctamente")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", "No se pudo hacer el deposito")