import bcrypt
from data.DataHelper import serializer
from decimal import Decimal
import requests

from business.MonedaLogic import moneda

monedas = moneda(f"4c1f0ea2701847ff9c5a7886279d5d35")

class user:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "Username": self.username,
            "Password": bcrypt.hashpw(self.password.encode(),bcrypt.gensalt()).decode(), 
            "Cuentas":{
                "ARS": 0.0}
                     
        }

serial = serializer()
        
def registrarUsuario(username, password):
        if serial.cargarUnUsuario(username)is not None:
            return False

        nuevoUsuario = user(username, password)
        usuario_dict = nuevoUsuario.to_dict()

        try:
            serial.guardarUnUsuario(usuario_dict)
            return True
        except Exception as e:
            return False

def login(username, password):
    usuario=serial.cargarUnUsuario(username)
    

    if usuario:
        if bcrypt.checkpw(password.encode(),usuario['Password'].encode()):
            return True
    return False

def depositar(username, monto):
    
    usuario = serial.cargarUnUsuario(username)

    if not usuario:
        return False

    if "Cuentas" not in usuario:
        usuario["Cuentas"] = {}

    if "ARS" not in usuario["Cuentas"]:
        usuario["Cuentas"]["ARS"] = Decimal("0.00")

    usuario ["Cuentas"]["ARS"] += monto
    serial.guardarUnUsuario(usuario)
    serial.actualizarUsuario(usuario)


def crearMoneda(username, otraMoneda):

    otraMoneda = otraMoneda.upper()

    if not monedas.ValidarMoneda(otraMoneda):
        return "invalida"

    usuario = serial.cargarUnUsuario(username)

    if otraMoneda in usuario["Cuentas"]:
        return "ya_existe"

    usuario["Cuentas"][otraMoneda] = Decimal("0.00")
    serial.guardarUnUsuario(usuario)
    serial.actualizarUsuario(usuario)
    return "ok"



def comprarMoneda (username, dst, montoDestino):

    org = "ARS"

    usuario = serial.cargarUnUsuario(username)
    
    if dst not in usuario["Cuentas"]:
        return "no_hay_cuenta"

    try:
        pesosNecesarios = monedas.convertir(montoDestino, dst, org)
    except KeyError:
        return "moneda_invalida"
    
    pesosDisponibles = usuario["Cuentas"].get("ARS", Decimal("0.00"))

    if pesosDisponibles < pesosNecesarios:
        return "sin_saldo"
        
    
    usuario["Cuentas"]["ARS"] -= pesosNecesarios
    usuario["Cuentas"][dst] = usuario["Cuentas"].get(dst, Decimal("0.00")) + montoDestino

    serial.guardarUnUsuario(usuario)
    serial.actualizarUsuario(usuario)
    return "ok"

def venderMoneda(username, orgVenta, montoOrigen):

    orgVenta = orgVenta.upper()
    
    usuario = serial.cargarUnUsuario(username)

    if orgVenta not in usuario["Cuentas"]:
        return "no_hay_cuenta"
    
    saldoDisponible = usuario["Cuentas"].get(orgVenta,Decimal("0.00"))

    if saldoDisponible < montoOrigen:
        return "sin_saldo"

    try:
        montoPesos = monedas.convertir(montoOrigen, orgVenta, "ARS")
    except Exception as e:
        return "moneda_invalida"
    
    usuario["Cuentas"][orgVenta] -= montoOrigen
    usuario["Cuentas"]["ARS"] = usuario["Cuentas"].get("ARS", Decimal("0.00")) + montoPesos
    serial.guardarUnUsuario(usuario)
    serial.actualizarUsuario(usuario)
    return "ok"



    
    

                


