from datetime import datetime
from enum import Enum

class TipoTransaccion(Enum):
    DEPOSITO = "DEPOSITO"
    RETIRO = "RETIRO"
    TRANSFERENCIA_ENVIADA = "TRANSFER_OUT"
    TRANSFERENCIA_RECIBIDA = "TRANSFER_IN"

class Transaccion:
    def __init__(self, id_transaccion, id_cuenta, tipo, monto, descripcion=""):
        self.id_transaccion = id_transaccion
        self.id_cuenta = id_cuenta
        self.tipo = tipo if isinstance(tipo, TipoTransaccion) else TipoTransaccion(tipo)
        self.monto = monto
        self.fecha = datetime.now()
        self.descripcion = descripcion
    
    def to_dict(self):
        return {
            'id_transaccion': self.id_transaccion,
            'id_cuenta': self.id_cuenta,
            'tipo': self.tipo.value,
            'monto': self.monto,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'descripcion': self.descripcion
        }