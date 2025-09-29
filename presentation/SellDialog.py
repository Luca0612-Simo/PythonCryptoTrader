from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QMainWindow,QTableWidgetItem,QDialog,QFileDialog,QMessageBox
from business import Logic, MonedaLogic
from decimal import Decimal
from screens.sellDialog_ui import Ui_Dialog

class SellDialog (QDialog, Ui_Dialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.username = username

        self.cargarMonedasUsuario()
        self.SellBtn.clicked.connect(self.SellBtnClick)

    def cargarMonedasUsuario(self):
        usuario = Logic.serial.cargarUnUsuario(self.username)

        if usuario and "Cuentas" in usuario:
            monedas = list(usuario["Cuentas"].keys())
            monedas.remove("ARS")
            self.CryptoBox
            self.CryptoBox.addItems(monedas)

    def SellBtnClick(self):
        try:
            monto = Decimal(self.SellTxt.text())
            if monto <= 0:
                QMessageBox.warning(self, "Error", "No se puede vender un monto igual o menor a cero")
                return
        except:
            QMessageBox.warning(self, "Error", "Monto invalido")
            return
        
        moneda=self.CryptoBox.currentText().upper()

        resultado = Logic.venderMoneda(self.username, moneda, monto)

        if resultado == "ok":
            QMessageBox.information(self, "Éxito", f"Vendiste {monto} {moneda}")
            self.accept()
        elif resultado == "sin_saldo":
            QMessageBox.warning(self, "Error", "No tenés saldo suficiente")
        elif resultado == "no_hay_cuenta":
            QMessageBox.warning(self, "Error", f"No tenés una cuenta para {moneda}")
        elif resultado == "moneda_invalida":
            QMessageBox.warning(self, "Error", "Esta moneda no es válida")
        else:
            QMessageBox.critical(self, "Error", "Hubo un error en la venta")