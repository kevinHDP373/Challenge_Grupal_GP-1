from abc import ABC, abstractmethod
import hashlib

class Usuario(ABC):
    def __init__(self, id_usuario, nombres, apellidos, dui, pin):
        self.id_usuario = id_usuario
        self.nombres = nombres
        self.apellidos = apellidos
        self.dui = dui
        self._pin_hash = self._hash_pin(pin)
    
    def _hash_pin(self, pin):
        return hashlib.sha256(str(pin).encode()).hexdigest()
    
    def verificar_pin(self, pin):
        return self._pin_hash == self._hash_pin(pin)
    
    @abstractmethod
    def get_rol(self):
        pass

class Administrador(Usuario):
    def __init__(self, id_usuario, nombres, apellidos, dui, pin):
        super().__init__(id_usuario, nombres, apellidos, dui, pin)
    
    def get_rol(self):
        return "ADMIN"

class Cliente(Usuario):
    def __init__(self, id_usuario, nombres, apellidos, dui, pin):
        super().__init__(id_usuario, nombres, apellidos, dui, pin)
        self.cuentas = []
    
    def get_rol(self):
        return "CLIENTE"
    
    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)