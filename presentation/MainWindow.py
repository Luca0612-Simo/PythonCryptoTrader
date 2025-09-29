from presentation.depositDialog import DepositDialog
from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QMainWindow,QTableWidgetItem,QDialog,QFileDialog,QMessageBox
from screens.Main_ui import MainWindow_ui
from business import Logic
from presentation.BuyDialog import BuyDialog
from presentation.SellDialog import SellDialog
from PyQt6.QtCore import QStringListModel
from presentation.CreateCryptoDialog import CreateCryptoDialog

class mainWindow (QMainWindow, MainWindow_ui):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.username = username

        self.Cryptos = QStringListModel()
        self.CryptoList.setModel(self.Cryptos)

        self.actualizarSaldo()
        self.actualizarListaMonedas()

        self.DepositBtn.clicked.connect(self.DepositBtnClick)
        self.BuyBtn.clicked.connect(self.BuyBtnClick)
        self.SellBtn.clicked.connect(self.SellBtnClick)
        self.CreateBtn.clicked.connect(self.CreateBtnClick)

    def actualizarSaldo(self):
        usuario = Logic.serial.cargarUnUsuario(self.username)
        if not usuario or "Cuentas" not in usuario:
            self.saldolbl.setText("Saldo: 0 ARS")
            return

        saldo_ars = usuario["Cuentas"].get("ARS", 0)
        self.saldolbl.setText(f"Saldo: {saldo_ars} ARS")

        # cuentas = usuario["Cuentas"]

        # self.CryptoList.setRowCount(len(cuentas))
        # self.CryptoList.setColumnCount(2)
        # self.CryptoList.setHorizontalHeaderLabels(["Moneda", "Saldo"])

        # for row, (moneda, saldo) in enumerate(cuentas.items()):
        #     self.CryptoList.setItem(row, 0, QTableWidgetItem(moneda))
        #     self.CryptoList.setItem(row, 1, QTableWidgetItem(str(saldo)))

    def actualizarListaMonedas(self):
        usuario = Logic.serial.cargarUnUsuario(self.username)
        if usuario and "Cuentas" in usuario:
            items = []
            for moneda, saldo in usuario["Cuentas"].items():
                if saldo != 0:
                    items.append(f"{moneda}: {saldo}")
            self.Cryptos.setStringList(items)
        else:
            self.Cryptos.setStringList([])

    def DepositBtnClick(self):
        dialog = DepositDialog(self.username)
        if dialog.exec():
            self.actualizarSaldo()
            #QMessageBox.information(self, "Operacion exitosa", "Se agrego dinero a su cuenta")

    def BuyBtnClick(self):
        dialog=BuyDialog(self.username)
        if dialog.exec():
            self.actualizarListaMonedas()

    def SellBtnClick(self):
        dialog = SellDialog(self.username)
        if dialog.exec():
            self.actualizarSaldo()

    def CreateBtnClick(self):
        dialog= CreateCryptoDialog(self.username)
        if dialog.exec():
            self.actualizarListaMonedas()


