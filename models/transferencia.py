from datetime import datetime

class Transferencia:
    def __init__(self, id_transferencia, id_cuenta_origen, id_cuenta_destino, monto):
        self.id_transferencia = id_transferencia
        self.id_cuenta_origen = id_cuenta_origen
        self.id_cuenta_destino = id_cuenta_destino
        self.monto = monto
        self.fecha = datetime.now()
    
    def to_dict(self):
        return {
            'id_transferencia': self.id_transferencia,
            'id_cuenta_origen': self.id_cuenta_origen,
            'id_cuenta_destino': self.id_cuenta_destino,
            'monto': self.monto,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S')
        }