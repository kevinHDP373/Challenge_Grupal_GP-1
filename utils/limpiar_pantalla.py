import os
import platform

def limpiar_pantalla():
    """Limpia la pantalla de la consola según el sistema operativo"""
    # Windows
    if platform.system() == "Windows":
        os.system('cls')
    # Mac/Linux
    else:
        os.system('clear')