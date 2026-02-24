from typing import List, Optional
from models.cuenta import Cuenta, TipoCuenta, EstadoCuenta
from models.transaccion import Transaccion, TipoTransaccion
from models.transferencia import Transferencia
from services.archivo_service import ArchivoService
from datetime import datetime
import uuid

class BancoService:
    def __init__(self):
        self.cuentas = self._cargar_cuentas()
        self.transacciones = self._cargar_transacciones()
        self.transferencias = self._cargar_transferencias()
        self.contador_transaccion = len(self.transacciones)
        self.contador_transferencia = len(self.transferencias)
    
    def _cargar_cuentas(self):
        cuentas_data = ArchivoService.cargar_cuentas()
        cuentas = []
        for c in cuentas_data:
            cuenta = Cuenta(
                c['id_cuenta'],
                c['id_propietario'],
                c['tipo'],
                float(c['saldo'])
            )
            cuenta.estado = EstadoCuenta(c['estado'])
            cuentas.append(cuenta)
        return cuentas
    
    def _cargar_transacciones(self):
        return ArchivoService.cargar_transacciones()
    
    def _cargar_transferencias(self):
        return ArchivoService.cargar_transferencias()
    
    def crear_cuenta(self, id_propietario, tipo, saldo_inicial=0):
        # Encontrar el próximo número de cuenta con formato ACC######
        max_num = 0
        for c in self.cuentas:
            if c.id_cuenta.startswith('ACC'):
                try:
                    num = int(c.id_cuenta[3:])  # Extraer número después de 'ACC'
                    if num > max_num:
                        max_num = num
                except:
                    pass
        
        nuevo_num = max_num + 1
        id_cuenta = f"ACC{nuevo_num:06d}"  # Formato ACC000001, ACC000002, etc.
        
        cuenta = Cuenta(id_cuenta, id_propietario, tipo, saldo_inicial)
        self.cuentas.append(cuenta)
        self._guardar_cuentas()
        return cuenta
    
    def obtener_cuentas_cliente(self, id_cliente):
        return [c for c in self.cuentas if c.id_propietario == id_cliente]
    
    def buscar_cuenta(self, id_cuenta):
        for c in self.cuentas:
            if c.id_cuenta == id_cuenta:
                return c
        return None
    
    def depositar(self, id_cuenta, monto):
        cuenta = self.buscar_cuenta(id_cuenta)
        if not cuenta:
            raise ValueError("Cuenta no encontrada")
        
        cuenta.depositar(monto)
        self._registrar_transaccion(id_cuenta, TipoTransaccion.DEPOSITO, monto, "Depósito")
        self._guardar_cuentas()
        return True
    
    def retirar(self, id_cuenta, monto):
        cuenta = self.buscar_cuenta(id_cuenta)
        if not cuenta:
            raise ValueError("Cuenta no encontrada")
        
        cuenta.retirar(monto)
        self._registrar_transaccion(id_cuenta, TipoTransaccion.RETIRO, monto, "Retiro")
        self._guardar_cuentas()
        return True
    
    def transferir(self, id_cuenta_origen, id_cuenta_destino, monto):
        if id_cuenta_origen == id_cuenta_destino:
            raise ValueError("No puedes transferir a la misma cuenta")
        
        origen = self.buscar_cuenta(id_cuenta_origen)
        destino = self.buscar_cuenta(id_cuenta_destino)
        
        if not origen or not destino:
            raise ValueError("Una de las cuentas no existe")
        
        if origen.estado != EstadoCuenta.ACTIVA or destino.estado != EstadoCuenta.ACTIVA:
            raise ValueError("Una de las cuentas no está activa")
        
        # Retirar de origen
        origen.retirar(monto)
        
        # Depositar en destino
        destino.depositar(monto)
        
        # Registrar transacciones
        self._registrar_transaccion(id_cuenta_origen, TipoTransaccion.TRANSFERENCIA_ENVIADA, 
                                   monto, f"Transferencia a {id_cuenta_destino}")
        self._registrar_transaccion(id_cuenta_destino, TipoTransaccion.TRANSFERENCIA_RECIBIDA, 
                                   monto, f"Transferencia de {id_cuenta_origen}")
        
        # Registrar transferencia
        self.contador_transferencia += 1
        transferencia = Transferencia(
            f"TR{self.contador_transferencia:06d}",
            id_cuenta_origen, id_cuenta_destino, monto
        )
        self.transferencias.append(transferencia.to_dict())
        ArchivoService.guardar_transferencias(self.transferencias)
        
        self._guardar_cuentas()
        return True
    
    def _registrar_transaccion(self, id_cuenta, tipo, monto, descripcion):
        self.contador_transaccion += 1
        transaccion = Transaccion(
            f"TX{self.contador_transaccion:06d}",
            id_cuenta, tipo, monto, descripcion
        )
        self.transacciones.append(transaccion.to_dict())
        ArchivoService.guardar_transacciones(self.transacciones)
    
    def _guardar_cuentas(self):
        cuentas_data = []
        for c in self.cuentas:
            cuentas_data.append({
                'id_cuenta': c.id_cuenta,
                'id_propietario': c.id_propietario,
                'tipo': c.tipo.value,
                'saldo': c.saldo,
                'estado': c.estado.value,
                'fecha_creacion': c.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
            })
        ArchivoService.guardar_cuentas(cuentas_data)
    
    def bloquear_activar_cuenta(self, id_cuenta):
        cuenta = self.buscar_cuenta(id_cuenta)
        if cuenta:
            cuenta.cambiar_estado()
            self._guardar_cuentas()
            return True
        return False
    
    def obtener_historial(self, id_cuenta):
        return [t for t in self.transacciones if t['id_cuenta'] == id_cuenta]
    
    def obtener_todas_cuentas(self):
        return self.cuentas
    
    def obtener_todas_transacciones(self):
        return self.transacciones
    
    def obtener_todas_transferencias(self):
        return self.transferencias