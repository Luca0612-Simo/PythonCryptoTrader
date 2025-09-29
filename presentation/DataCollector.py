
from business.Logic import user, login, registrarUsuario, depositar, crearMoneda, comprarMoneda, venderMoneda
import maskpass
from decimal import Decimal, InvalidOperation
import time

class dataCollector:
    
    eleccion = input ('Ingrese 1 si quiere registrarse. Ingrese 2 si quiere logearse \n')
    if eleccion == "1":
        print('Regístrese:')

        username = input('Ingrese su usuario: \n')
        password = maskpass.advpass(prompt="Ingrese su contraseña: \n", mask="*")
        passwordAgain = maskpass.advpass(prompt="Ingrese su contraseña de nuevo: \n", mask="*")
        

        if username == "" or password == "":
            print("No se puede registrar un usuario vacio")
        else:
            if password == passwordAgain:
                resultado = registrarUsuario(username,password)
                if not resultado:
                    print("Este usuario ya existe")
                    
                else:
                    
                    print("Registro exitoso")
            else:
                print("Las contraseñas no coinciden. Registro fallido")

    elif eleccion == "2" :
        print("Login:")
        username = input('Ingrese su usuario: \n')
        password = maskpass.advpass(prompt="Ingrese su contraseña: \n", mask="*")

        if login(username, password):
            print("Login exitoso")

            while eleccion != "0":

                eleccion = input("¿Que operación desea realizar? \n"
                                "0-SALIR \n"
                                "1-DEPOSITAR PESOS \n" 
                                "2-CREAR UNA CUENTA EN OTRA MONEDA \n"
                                "3-COMPRAR MONEDA CON PESOS ARGENTINOS \n"
                                "4-VENDER MONEDA PARA RECIBIR PESOS ARGENTINOS\n")
                
                

                if eleccion == "1":
                    montoAdepositar = Decimal (input("¿Cuánto desea depositar? \n"))

                    print(f"¿Seguro que desea depositar {montoAdepositar}? (si o no)")
                    Tinicio = time.time()
                    rta=input()

                    if(time.time() - Tinicio) > 120:
                        print ("La operacion se canceló porque se superó el tiempo de espera")
                    
                    elif rta.lower() == 'si':
                        if montoAdepositar <= 0:
                            print("No se puede depostiar un monto menor o igual a 0")
                        else:
                            depositar(username, montoAdepositar)
                            print(f"¡Exito! Ingresaste {montoAdepositar} a tu cuenta en ARS")
                        
                    elif rta.lower()== 'no':
                        print("Se canceló la operación")
                    else:
                        print("Debe escribir si o no")
                    
                    

                elif eleccion == "2":
                    otraMoneda = input("Indique la moneda que quiera añadir a su cuenta. Ej:(USD-JPY-EUR) \n")

                    print(f"¿Seguro que desea añadir {otraMoneda} a su cuenta? (si o no)")

                    Tinicio = time.time()
                    rta=input()

                    if(time.time() - Tinicio) > 120:
                        print ("La operación se canceló porque se superó el tiempo de espera")
                    
                    elif rta.lower() == 'si':
                        resultado = crearMoneda(username, otraMoneda)
                        
                        if resultado == "invalida":
                            print(f"{otraMoneda} no existe")
                        elif resultado == "ya_existe":
                            print(f"ya existe una cuenta en {otraMoneda}")
                        elif resultado == "ok":
                            print(f"La moneda {otraMoneda} fue añadida correctamente")
                        
                    elif rta.lower()== 'no':
                        print("Se canceló la operación")
                    else:
                        print("Debe escribir si o no")
                    
                    

                elif eleccion == "3":
                    dst = input("Indique la moneda que desee comprar. Ej:(USD-EUR-JPY) \n").upper()

                    try:
                        montoAcomprar = input(f"¿Cuántos {dst} desea comprar? \n").replace(",", ".")
                        cantidadDst = Decimal(montoAcomprar)
                        
                        
                    except InvalidOperation:
                        print("El monto ingresado no es válido")
                        continue

                    if cantidadDst <= 0:
                            print("No se puede comprar una moneda con una cantidad menor o igual a 0")
                    else:            
                        print("¿Seguro que desea realizar la operación? ('si' o 'no')")

                        Tinicio = time.time()
                        rta = input()

                        if(time.time() - Tinicio) > 120:
                            print ("La operacion se canceló porque se superó el tiempo de espera")
                        
                        elif rta.lower() == 'si':
                            resultado = comprarMoneda(username, dst, cantidadDst) 

                            if  resultado == "moneda_invalida":
                                print("No es posible comprar esa moneda")
                            elif resultado == "no_hay_cuenta":
                                print(f"el usuario no tiene una cuenta en {dst}")
                            elif resultado == "sin_saldo":
                                print("Saldo insuficiente")
                            elif resultado == "ok":    
                                print(f"¡Su compra de {dst} se realizó exitosamente!")
                        
                        elif rta.lower()== 'no':
                            print("Se canceló la operación")
                        else:
                            print("Debe escribir si o no")    


                    

                elif eleccion == "4":
                    org = input("Indique la moneda que desea vender. Ej:(USD-EUR-JPY) \n").upper()
                    try:
                        montoAvender = input(f"Cuantos {org} desea vender? \n").replace(",", ".")
                        cantidadOrg = Decimal(montoAvender)
                    except InvalidOperation:
                        print("El monto ingresado no es válido")
                        continue
                    if cantidadOrg <= 0:
                            print("No se puede vender una moneda con una cantidad menor o igual a 0")
                    else:            
                        print(f"¿Seguro que que quiere vender {org}? (si o no)")  
                    
                        Tinicio = time.time()
                        rta = input()

                        if(time.time() - Tinicio) > 120:
                            print ("La operacion se canceló porque se superó el tiempo de espera")
                        
                        elif rta.lower() == 'si':
                            resultado = venderMoneda(username, org, cantidadOrg) 

                            if  resultado == "moneda_invalida":
                                print("No es posible comprar esa moneda")
                            elif resultado == "sin_saldo":
                                print("Saldo insuficiente")
                            elif resultado == "no_hay_cuenta":
                                print(f"El usuario no tiene una cuenta en {org}")
                            elif resultado == "ok":    
                                print("¡Su venta se ha realizado exitosamente!")

                        elif rta.lower()== 'no':
                            print("Se canceló la operación")
                        else:
                            print("Debe escribir si o no") 

                
        else:
            print("Acceso denegado")

    else:
        print('Debe de seleccionar o 1 para registarse o 2 para logearse')










