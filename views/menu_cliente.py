from services.banco_service import BancoService
from utils.limpiar_pantalla import limpiar_pantalla

class MenuCliente:
    def __init__(self, cliente, banco_service):
        self.cliente = cliente
        self.banco = banco_service
    
    def mostrar(self):
        while True:
            limpiar_pantalla()
            print("\n" + "="*50)
            print(f"BANCO - CLIENTE: {self.cliente.nombres} {self.cliente.apellidos}")
            print("="*50)
            print("1. Ver saldo de cuentas")
            print("2. Ver historial de movimientos")
            print("3. Depositar")
            print("4. Retirar")
            print("5. Transferir")
            print("6. Cerrar sesión")
            print("="*50)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.ver_saldo()
            elif opcion == "2":
                self.ver_historial()
            elif opcion == "3":
                self.depositar()
            elif opcion == "4":
                self.retirar()
            elif opcion == "5":
                self.transferir()
            elif opcion == "6":
                print("Sesión cerrada.")
                limpiar_pantalla()
                break
            elif opcion == "":
                print("No ingresó ninguna opción")
                input("\nPresione Enter para continuar...")
            else:
                print("Opción inválida.")
                input("\nPresione Enter para continuar...")
    
    def ver_saldo(self):
        limpiar_pantalla()
        print("\n--- SALDO DE CUENTAS ---")
        
        cuentas = self.banco.obtener_cuentas_cliente(self.cliente.id_usuario)
        
        if not cuentas:
            print("No tienes cuentas asociadas.")
            input("\nPresione Enter para continuar...")
            return
        
        for cuenta in cuentas:
            estado = "ACTIVA" if cuenta.estado.value == "Activa" else "BLOQUEADA"
            print(f"Cuenta: {cuenta.id_cuenta} | Tipo: {cuenta.tipo.value} | Saldo: ${cuenta.saldo:.2f} | {estado}")
        
        input("\nPresione Enter para continuar...")
    
    def ver_historial(self):
        limpiar_pantalla()
        print("\n--- HISTORIAL DE MOVIMIENTOS ---")
        
        cuentas = self.banco.obtener_cuentas_cliente(self.cliente.id_usuario)
        
        if not cuentas:
            print("No tienes cuentas asociadas.")
            input("\nPresione Enter para continuar...")
            return
        
        for cuenta in cuentas:
            print(f"\nCuenta: {cuenta.id_cuenta} ({cuenta.tipo.value})")
            historial = self.banco.obtener_historial(cuenta.id_cuenta)
            
            if not historial:
                print("  No hay movimientos")
                continue
            
            for trans in historial[-10:]:  # Últimas 10
                print(f"  {trans['fecha']} | {trans['tipo']:12} | ${float(trans['monto']):8.2f} | {trans['descripcion']}")
        
        input("\nPresione Enter para continuar...")
    
    def depositar(self):
        limpiar_pantalla()
        print("\n--- DEPOSITAR ---")
        print("-" * 40)
        
        cuentas = self.banco.obtener_cuentas_cliente(self.cliente.id_usuario)
        cuentas_activas = [c for c in cuentas if c.estado.value == "Activa"]
        
        if not cuentas_activas:
            print("No tienes cuentas activas.")
            input("\nPresione Enter para continuar...")
            return
        
        print("\nCuentas disponibles:")
        for i, cuenta in enumerate(cuentas_activas, 1):
            print(f"{i}. {cuenta.id_cuenta} - {cuenta.tipo.value} (${cuenta.saldo:.2f})")
        print("0. Cancelar")
        
        try:
            opcion = input("\nSeleccione cuenta (0 para cancelar): ").strip()
            
            if opcion == '':
                print("No ingresó ninguna opción")
                input("\nPresione Enter para continuar...")
                return
                
            if opcion == '0' or opcion.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            idx = int(opcion) - 1
            if idx < 0 or idx >= len(cuentas_activas):
                print("Selección inválida")
                input("\nPresione Enter para continuar...")
                return
            
            cuenta_seleccionada = cuentas_activas[idx]
            print(f"\nSaldo actual: ${cuenta_seleccionada.saldo:.2f}")
            
            monto_input = input("Monto a depositar: $").strip()
            
            if monto_input == '':
                print("No ingresó ningún monto")
                input("\nPresione Enter para continuar...")
                return
                
            if monto_input.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            monto = float(monto_input)
            
            if monto <= 0:
                print("El monto debe ser positivo")
                input("\nPresione Enter para continuar...")
                return
            
            self.banco.depositar(cuenta_seleccionada.id_cuenta, monto)
            print(f"Depósito exitoso. Nuevo saldo: ${cuenta_seleccionada.saldo:.2f}")
            
        except ValueError:
            print("Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def retirar(self):
        limpiar_pantalla()
        print("\n--- RETIRAR ---")
        print("-" * 40)
        
        cuentas = self.banco.obtener_cuentas_cliente(self.cliente.id_usuario)
        cuentas_activas = [c for c in cuentas if c.estado.value == "Activa"]
        
        if not cuentas_activas:
            print("No tienes cuentas activas.")
            input("\nPresione Enter para continuar...")
            return
        
        print("\nCuentas disponibles:")
        for i, cuenta in enumerate(cuentas_activas, 1):
            print(f"{i}. {cuenta.id_cuenta} - {cuenta.tipo.value} (${cuenta.saldo:.2f})")
        print("0. Cancelar")
        
        try:
            opcion = input("\nSeleccione cuenta (0 para cancelar): ").strip()
            
            if opcion == '':
                print("No ingresó ninguna opción")
                input("\nPresione Enter para continuar...")
                return
                
            if opcion == '0' or opcion.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            idx = int(opcion) - 1
            if idx < 0 or idx >= len(cuentas_activas):
                print("Selección inválida")
                input("\nPresione Enter para continuar...")
                return
            
            cuenta_seleccionada = cuentas_activas[idx]
            print(f"\nSaldo disponible: ${cuenta_seleccionada.saldo:.2f}")
            
            monto_input = input("Monto a retirar: $").strip()
            
            if monto_input == '':
                print("No ingresó ningún monto")
                input("\nPresione Enter para continuar...")
                return
                
            if monto_input.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            monto = float(monto_input)
            
            # Validaciones en la vista
            if monto <= 0:
                print("El monto debe ser positivo")
                input("\nPresione Enter para continuar...")
                return
                
            if monto > cuenta_seleccionada.saldo:
                print(f"Saldo insuficiente. Solo tiene disponible: ${cuenta_seleccionada.saldo:.2f}")
                input("\nPresione Enter para continuar...")
                return
            
            self.banco.retirar(cuenta_seleccionada.id_cuenta, monto)
            print(f"Retiro exitoso. Nuevo saldo: ${cuenta_seleccionada.saldo:.2f}")
            
        except ValueError:
            print("Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def transferir(self):
        limpiar_pantalla()
        print("\n--- TRANSFERIR ---")
        print("-" * 40)
        
        cuentas = self.banco.obtener_cuentas_cliente(self.cliente.id_usuario)
        cuentas_activas = [c for c in cuentas if c.estado.value == "Activa"]
        
        if not cuentas_activas:
            print("No tienes cuentas activas.")
            input("\nPresione Enter para continuar...")
            return
        
        print("\nCuentas origen:")
        for i, cuenta in enumerate(cuentas_activas, 1):
            print(f"{i}. {cuenta.id_cuenta} - {cuenta.tipo.value} (${cuenta.saldo:.2f})")
        print("0. Cancelar")
        
        try:
            opcion = input("\nSeleccione cuenta origen (0 para cancelar): ").strip()
            
            if opcion == '':
                print("No ingresó ninguna opción")
                input("\nPresione Enter para continuar...")
                return
                
            if opcion == '0' or opcion.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            idx = int(opcion) - 1
            if idx < 0 or idx >= len(cuentas_activas):
                print("Selección inválida")
                input("\nPresione Enter para continuar...")
                return
            
            cuenta_origen = cuentas_activas[idx]
            print(f"\nSaldo disponible en origen: ${cuenta_origen.saldo:.2f}")
            
            id_destino = input("ID de cuenta destino (o 'cancelar'): ").strip()
            
            if id_destino == '':
                print("No ingresó ID de destino")
                input("\nPresione Enter para continuar...")
                return
                
            if id_destino.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            # Verificar que la cuenta destino existe y está activa
            cuenta_destino = self.banco.buscar_cuenta(id_destino)
            if not cuenta_destino:
                print("La cuenta destino no existe")
                input("\nPresione Enter para continuar...")
                return
                
            if cuenta_destino.estado.value != "Activa":
                print("La cuenta destino no está activa")
                input("\nPresione Enter para continuar...")
                return
            
            # Verificar que no sea la misma cuenta
            if cuenta_origen.id_cuenta == id_destino:
                print("No puedes transferir a la misma cuenta")
                input("\nPresione Enter para continuar...")
                return
            
            monto_input = input("Monto a transferir: $").strip()
            
            if monto_input == '':
                print("No ingresó ningún monto")
                input("\nPresione Enter para continuar...")
                return
                
            if monto_input.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            monto = float(monto_input)
            
            # Validaciones en la vista
            if monto <= 0:
                print("El monto debe ser positivo")
                input("\nPresione Enter para continuar...")
                return
                
            if monto > cuenta_origen.saldo:
                print(f"Saldo insuficiente. Solo tiene disponible: ${cuenta_origen.saldo:.2f}")
                input("\nPresione Enter para continuar...")
                return
            
            self.banco.transferir(cuenta_origen.id_cuenta, id_destino, monto)
            print(f"Transferencia exitosa. Nuevo saldo: ${cuenta_origen.saldo:.2f}")
            
        except ValueError:
            print("Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        input("\nPresione Enter para continuar...")