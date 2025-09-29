from PyQt6.QtWidgets import QDialog, QMessageBox
from screens.CreateCryptoDialog_ui import Ui_Dialog
from business import Logic

class CreateCryptoDialog(QDialog, Ui_Dialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.username = username

        self.cargarMonedas()
        self.CreateBtn.clicked.connect(self.CreateBtnClick)

    def cargarMonedas(self):
        try:
            tasas = Logic.monedas.obtenerTasas()
            monedas = list(tasas.keys())

            self.CryptoBox.clear()
            self.CryptoBox.addItems(monedas)
        except Exception as e:
            QMessageBox.warning(self, "Error", "No se pudieron cargar las monedas")

    def CreateBtnClick(self):
        moneda = self.CryptoBox.currentText().upper()
        resultado = Logic.crearMoneda(self.username, moneda)

        if resultado == "ok":
            QMessageBox.information(self, "Éxito", f"Se creó la cuenta en {moneda}")
            self.accept()
        elif resultado == "ya_existe":
            QMessageBox.warning(self, "Aviso", f"Ya existe una cuenta en {moneda}")
        elif resultado == "invalida":
            QMessageBox.warning(self, "Error", "La moneda no es válida")
        else:
            QMessageBox.critical(self, "Error", "No se pudo crear la cuenta")