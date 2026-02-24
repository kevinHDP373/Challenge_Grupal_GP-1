import os
import sys
from services.auth_service import AuthService
from services.banco_service import BancoService
from services.archivo_service import ArchivoService
from views.menu_cliente import MenuCliente
from views.menu_admin import MenuAdmin
from models.usuario import Cliente
from utils.limpiar_pantalla import limpiar_pantalla

class AplicacionBancaria:
    def __init__(self):
        ArchivoService.asegurar_directorios()
        self.auth_service = AuthService()
        self.banco_service = BancoService()
    
    def iniciar(self):
        limpiar_pantalla()
        print("\n" + "="*60)
        print("BIENVENIDO AL SISTEMA BANCARIO")
        print("="*60)
        
        while True:
            print("\n--- MENU PRINCIPAL ---")
            print("1. Iniciar sesión")
            print("2. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.login()
            elif opcion == "2":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida.")
                input("\nPresione Enter para continuar...")
                limpiar_pantalla()
    
    def login(self):
        limpiar_pantalla()
        print("\n--- INICIAR SESIÓN ---")
        print("Rol Administrador: utiliza username (ej. CP0001)")
        print("Rol Cliente: utiliza DUI (ej. 2751715-2)")
        
        print("\nIngresa credenciales de acceso")
        identificador = input("Usuario: ")
        pin = input("PIN: ")
        
        usuario = self.auth_service.login(identificador, pin)
        
        if usuario:
            limpiar_pantalla()
            print(f"Bienvenido {usuario.nombres} {usuario.apellidos}")
            
            if usuario.get_rol() == "ADMIN":
                menu = MenuAdmin(usuario, self.banco_service, self.auth_service)
                menu.mostrar()
            else:
                menu = MenuCliente(usuario, self.banco_service)
                menu.mostrar()
        else:
            print("Identificador o PIN incorrecto")
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()

def mostrar_instrucciones():
    limpiar_pantalla()
    print("\n" + "="*60)
    print("INSTRUCCIONES DE USO")
    print("="*60)
    print("   Credenciales de prueba:")
    print("   Admin: CP0001 / 1234")
    print("   Clientes: ver archivo data/usuarios.csv")
    print("="*60)

if __name__ == "__main__":
    # Verificar si existen datos
    if not os.path.exists("data/usuarios.csv"):
        print("No se encontraron datos. Ejecutando generador de datos semilla...")
        import subprocess
        subprocess.run([sys.executable, "seed_data/generar_seed.py"])
    
    # Mostrar instrucciones
    mostrar_instrucciones()
    input("\nPresione Enter para continuar...")
    
    # Iniciar aplicación
    app = AplicacionBancaria()
    app.iniciar()