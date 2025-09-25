import sqlobject as SO
from decimal import Decimal


DB_URI = 'mysql://guest:1234@localhost/data_db'
SO.sqlhub.processConnection = SO.connectionForURI(DB_URI)

class Usuario(SO.SQLObject):
    username = SO.StringCol(length=100, unique=True)
    password = SO.StringCol(length=100)
    cuentas = SO.MultipleJoin("Cuenta")

class Cuenta(SO.SQLObject):
    usuario = SO.ForeignKey("Usuario")
    moneda = SO.StringCol(length=5)
    saldo = SO.DecimalCol(size=20, precision=10, default=Decimal("0.00"))

Usuario.createTable(ifNotExists=True)
Cuenta.createTable(ifNotExists=True)

class serializer:
    def cargarUsuario(self):
        usuarios = []
        for u in Usuario.select():
            cuentas = {c.moneda: str(c.saldo) for c in u.cuentas}
            usuarios.append({
                "Username": u.username,
                "Password": u.password,
                "Cuentas": cuentas
            })
        return usuarios

    def guardarUsuario(self, usuarios_dict_list):
        for u in usuarios_dict_list:
            usuario = Usuario(username=u["Username"], password=u["Password"])
            for moneda, saldo in u.get("Cuentas", {}).items():
                Cuenta(usuario=usuario, moneda=moneda, saldo=Decimal(saldo))

    def guardarUnUsuario(self, usuario_dict):
        try:
            u = Usuario.selectBy(username=usuario_dict["Username"]).getOne()
        except SO.SQLObjectNotFound:
            u = Usuario(username=usuario_dict["Username"], password=usuario_dict["Password"])

        u.password = usuario_dict["Password"]
        for moneda, saldo in usuario_dict.get("Cuentas", {}).items():
            cuenta = self._obtenerCuenta(u, moneda)
            if cuenta:
                cuenta.saldo = Decimal(saldo)
                cuenta.syncUpdate()
            else:
                Cuenta(usuario=u, moneda=moneda, saldo=Decimal(saldo))

    def cargarUnUsuario(self, username):
        try:
            u = Usuario.selectBy(username=username).getOne()
            cuentas = {c.moneda: Decimal(str(c.saldo)) for c in u.cuentas}
            return {
                "Username": u.username,
                "Password": u.password,
                "Cuentas": cuentas
            }
        except SO.SQLObjectNotFound:
            return None

    def actualizarUsuario(self, usuario_dict):
        u = Usuario.selectBy(username=usuario_dict["Username"]).getOne()
        for moneda, saldo in usuario_dict["Cuentas"].items():
            cuenta = self._obtenerCuenta(u, moneda)
            if cuenta:
                cuenta.saldo = Decimal(saldo)
                cuenta.syncUpdate()
            else:
                Cuenta(usuario=u, moneda=moneda, saldo=Decimal(saldo))

    def _obtenerCuenta(self, usuario, moneda):
        for c in usuario.cuentas:
            if c.moneda == moneda:
                return c
        return None

# import json
# import os
# from urllib import request

# from decimal import Decimal

# class serializer:

#     def cargarUsuario(self):
        
#         if not os.path.exists("usuarios"):
#             os.makedirs("usuarios")
#         path = os.path.join("usuarios", "users.json")
#         if not os.path.exists(path):
#             return []
#         with open(path, "r", encoding="utf-8") as f:
#             return json.load(f)

#     def guardarUsuario(self,usuarios):
#         if not os.path.exists("usuarios"):
#             os.makedirs("usuarios")
#         path = os.path.join("usuarios", "users.json")

#         with open(path, "w", encoding="utf-8") as f:
#             json.dump(usuarios, f, ensure_ascii=False, indent=4)



#     def guardarUnUsuario(self, usuario_dict):
#         username = usuario_dict["Username"]
#         if not os.path.exists("usuarios"):
#             os.makedirs("usuarios")

#         cuentas = usuario_dict.get("Cuentas", {})
#         for moneda, saldo in cuentas.items():
#             if isinstance(saldo, Decimal):
#                 cuentas[moneda] = str(saldo)

#         path = os.path.join("usuarios", f"{username}.json")
#         with open(path, "w", encoding="utf-8") as f:
#             json.dump(usuario_dict, f, ensure_ascii=False, indent=4)

            

#     def cargarUnUsuario(self, username):
#         path = os.path.join("usuarios", f"{username}.json")
#         if not os.path.exists(path):
#             return None
        
#         with open(path, "r", encoding="utf-8") as f:
#             datos = json.load(f)
        
#         if "Cuentas" in datos:
#             for moneda, saldo in datos["Cuentas"].items():
#                 datos["Cuentas"][moneda] = Decimal(saldo)
#         return datos
    
#     def actualizarUsuario(self, usuarioActualizado):
#         usuarios = self.cargarUsuario()

#         for i, u in enumerate(usuarios):
#             if u["Username"] == usuarioActualizado["Username"]:
#                 usuarios[i] = usuarioActualizado
#                 break
#         self.guardarUsuario(usuarios)
        
    

    

    