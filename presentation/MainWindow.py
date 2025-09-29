from presentation.depositDialog import DepositDialog
from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QMainWindow,QTableWidgetItem,QDialog,QFileDialog,QMessageBox
from screens.Main_ui import MainWindow_ui
from business import Logic
from presentation.BuyDialog import BuyDialog
from presentation.SellDialog import SellDialog


class mainWindow (QMainWindow, MainWindow_ui):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.username = username

        self.actualizarSaldo()

        self.DepositBtn.clicked.connect(self.DepositBtnClick)
        self.BuyBtn.clicked.connect(self.BuyBtnClick)
        self.SellBtn.clicked.connect(self.SellBtnClick)

    def actualizarSaldo(self):
        usuario = Logic.serial.cargarUnUsuario(self.username)
        if usuario and "Cuentas" in usuario:
            saldo_ars = usuario["Cuentas"].get("ARS", 0)
            self.saldolbl.setText(f"Saldo: {saldo_ars} ARS")
        else:
            self.saldolbl.setText("Saldo: 0 ARS")

    def DepositBtnClick(self):
        dialog = DepositDialog(self.username)
        if dialog.exec():
            self.actualizarSaldo()
            #QMessageBox.information(self, "Operacion exitosa", "Se agrego dinero a su cuenta")

    def BuyBtnClick(self):
        dialog=BuyDialog(self.username)
        if dialog.exec():
            self.actualizarSaldo()

    def SellBtnClick(self):
        dialog = SellDialog(self.username)
        if dialog.exec():
            self.actualizarSaldo()


