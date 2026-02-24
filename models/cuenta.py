from enum import Enum
from datetime import datetime

class TipoCuenta(Enum):
    AHORRO = "Ahorro"
    CORRIENTE = "Corriente"

class EstadoCuenta(Enum):
    ACTIVA = "Activa"
    BLOQUEADA = "Bloqueada"

class Cuenta:
    def __init__(self, id_cuenta, id_propietario, tipo, saldo_inicial=0):
        self.id_cuenta = id_cuenta
        self.id_propietario = id_propietario
        self.tipo = tipo if isinstance(tipo, TipoCuenta) else TipoCuenta(tipo)
        self.saldo = saldo_inicial
        self.estado = EstadoCuenta.ACTIVA
        self.fecha_creacion = datetime.now()
    
    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if self.estado != EstadoCuenta.ACTIVA:
            raise ValueError("La cuenta no está activa")
        self.saldo += monto
        return True
    
    def retirar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if self.estado != EstadoCuenta.ACTIVA:
            raise ValueError("La cuenta no está activa")
        if self.saldo < monto:
            raise ValueError("Saldo insuficiente")
        self.saldo -= monto
        return True
    
    def cambiar_estado(self):
        if self.estado == EstadoCuenta.ACTIVA:
            self.estado = EstadoCuenta.BLOQUEADA
        else:
            self.estado = EstadoCuenta.ACTIVA