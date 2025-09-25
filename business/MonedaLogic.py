from decimal import Decimal
import requests

class moneda:
    def __init__(self, apikey):
        self.apiKey = apikey
        self.url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={apikey}"

    def ValidarMoneda(self, monedaCodigo: str) -> bool:
        tasas = self.obtenerTasas()
        return monedaCodigo.upper() in tasas

    def obtenerTasas(self):
        res = requests.get(self.url)
        datos = res.json()
        return datos["rates"]

    def convertir(self, monto : Decimal, org : str, dst : str) -> Decimal:
        if org == dst:
            return monto
    
        tasas = self.obtenerTasas()

        tasaOrg = Decimal(tasas[org])
        tasaDst = Decimal(tasas[dst])

        return monto * (tasaDst / tasaOrg)