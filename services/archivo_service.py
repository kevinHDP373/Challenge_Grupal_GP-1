import csv
import os
from typing import List, Dict, Any
from models.usuario import Administrador, Cliente
from models.cuenta import Cuenta, TipoCuenta, EstadoCuenta
from models.transaccion import Transaccion, TipoTransaccion
from models.transferencia import Transferencia

class ArchivoService:
    RUTA_USUARIOS = "data/usuarios.csv"
    RUTA_CUENTAS = "data/cuentas.csv"
    RUTA_TRANSACCIONES = "data/transacciones.csv"
    RUTA_TRANSFERENCIAS = "data/transferencias.csv"
    
    @staticmethod
    def asegurar_directorios():
        os.makedirs("data", exist_ok=True)
        os.makedirs("outputs/plots", exist_ok=True)
    
    @staticmethod
    def guardar_usuarios(usuarios: List[Dict]):
        with open(ArchivoService.RUTA_USUARIOS, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'nombres', 'apellidos', 'dui', 'pin_hash', 'rol'])
            writer.writeheader()
            for u in usuarios:
                writer.writerow(u)
    
    @staticmethod
    def cargar_usuarios():
        if not os.path.exists(ArchivoService.RUTA_USUARIOS):
            return []
        with open(ArchivoService.RUTA_USUARIOS, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    @staticmethod
    def guardar_cuentas(cuentas: List[Dict]):
        with open(ArchivoService.RUTA_CUENTAS, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id_cuenta', 'id_propietario', 'tipo', 'saldo', 'estado', 'fecha_creacion'])
            writer.writeheader()
            for c in cuentas:
                writer.writerow(c)
    
    @staticmethod
    def cargar_cuentas():
        if not os.path.exists(ArchivoService.RUTA_CUENTAS):
            return []
        with open(ArchivoService.RUTA_CUENTAS, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    @staticmethod
    def guardar_transacciones(transacciones: List[Dict]):
        with open(ArchivoService.RUTA_TRANSACCIONES, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id_transaccion', 'id_cuenta', 'tipo', 'monto', 'fecha', 'descripcion'])
            writer.writeheader()
            for t in transacciones:
                writer.writerow(t)
    
    @staticmethod
    def cargar_transacciones():
        if not os.path.exists(ArchivoService.RUTA_TRANSACCIONES):
            return []
        with open(ArchivoService.RUTA_TRANSACCIONES, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    @staticmethod
    def guardar_transferencias(transferencias: List[Dict]):
        with open(ArchivoService.RUTA_TRANSFERENCIAS, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id_transferencia', 'id_cuenta_origen', 'id_cuenta_destino', 'monto', 'fecha'])
            writer.writeheader()
            for t in transferencias:
                writer.writerow(t)
    
    @staticmethod
    def cargar_transferencias():
        if not os.path.exists(ArchivoService.RUTA_TRANSFERENCIAS):
            return []
        with open(ArchivoService.RUTA_TRANSFERENCIAS, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)