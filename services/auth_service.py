from models.usuario import Administrador, Cliente
from services.archivo_service import ArchivoService

class AuthService:
    def __init__(self):
        self.usuario_actual = None
        self.usuarios = []
        self.contador_admin = 0
        self.cargar_usuarios()
    
    def cargar_usuarios(self):
        datos_usuarios = ArchivoService.cargar_usuarios()
        for u in datos_usuarios:
            if u['rol'] == 'ADMIN':
                self.contador_admin = max(self.contador_admin, int(u['id'].split('_')[1]) if '_' in u['id'] else 0)
    
    def generar_id_admin(self, nombres, apellidos):
        self.contador_admin += 1
        siglas = nombres[0].upper() + apellidos[0].upper()
        return f"{siglas}_{self.contador_admin:04d}"
    
    def login(self, identificador, pin):
        datos_usuarios = ArchivoService.cargar_usuarios()
        
        for u in datos_usuarios:
            if (u['rol'] == 'ADMIN' and u['id'] == identificador) or \
               (u['rol'] == 'CLIENTE' and u['dui'] == identificador):
                
                # Verificar PIN (en producción usar hash)
                if u['pin_hash'] == pin:  # Simplificado, debería comparar hash
                    if u['rol'] == 'ADMIN':
                        self.usuario_actual = Administrador(
                            u['id'], u['nombres'], u['apellidos'], u['dui'], pin
                        )
                    else:
                        self.usuario_actual = Cliente(
                            u['id'], u['nombres'], u['apellidos'], u['dui'], pin
                        )
                    return self.usuario_actual
        return None
    
    def logout(self):
        self.usuario_actual = None