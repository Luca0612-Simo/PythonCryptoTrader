from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QMainWindow,QTableWidgetItem,QDialog,QFileDialog,QMessageBox
from business import Logic, MonedaLogic
from decimal import Decimal
from screens.buyDialog_ui import Ui_Dialog

class BuyDialog(QDialog, Ui_Dialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.username = username
        self.cargarMonedas()

        self.BuyBtn.clicked.connect(self.BuyBtnClick)

    def cargarMonedas(self):
        try:
            tasas = Logic.monedas.obtenerTasas()
            monedas = list(tasas.keys())

            self.CryptoBox.clear()
            self.CryptoBox.addItems(monedas)
        except Exception as e:
            QMessageBox.warning(self, "Error", "No se pudieron cargar las monedas")

    def BuyBtnClick(self):
        try:
            monto = Decimal (self.buyTxt.text())
            if monto <= 0:
                QMessageBox.warning(self, "Error", "El monto no puede ser igual o menor a cero")
                return
        except:
            QMessageBox.warning(self, "Error", "Monto invalido")
            return
        
        moneda= self.CryptoBox.currentText().upper()

        resultado= Logic.comprarMoneda(self.username, moneda, monto)

        if resultado == "ok":
            QMessageBox.information(self, "Éxito", f"Compraste {monto} {moneda}")
            self.accept()
        elif resultado == "sin_saldo":
            QMessageBox.warning(self, "Error", "No tenés saldo suficiente en ARS")
        elif resultado == "no_hay_cuenta":
            QMessageBox.warning(self, "Error", f"No hay una cuenta para {moneda}")
        elif resultado == "moneda_invalida":
            QMessageBox.warning(self, "Error", "La moneda seleccionada no es válida")
        else:
            QMessageBox.critical(self, "Error", "Hubo un error en la compra")
