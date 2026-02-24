import csv
import random
import hashlib
from datetime import datetime, timedelta
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generar_dui():
    return f"{random.randint(1000000, 9999999)}-{random.randint(0, 9)}"

def generar_pin():
    return f"{random.randint(1000, 9999)}"

def generar_fecha_aleatoria(inicio, fin):
    delta = fin - inicio
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 24*3600 - 1)
    return inicio + timedelta(days=random_days, seconds=random_seconds)

def generar_seed():
    print("Generando datos semilla...")
    
    # Crear directorios
    os.makedirs("data", exist_ok=True)
    
    # 1. Generar usuarios
    usuarios = []
    contador_admin = 0
    
    # Función para generar ID de admin con siglas (SIN GUION BAJO)
    def generar_id_admin(nombres, apellidos):
        nonlocal contador_admin
        contador_admin += 1
        siglas = nombres[0].upper() + apellidos[0].upper()
        return f"{siglas}{contador_admin:04d}"
    
    # Administradores (varios, con diferentes siglas)
    admins_data = [
        ("Carlos", "Perez"),
        ("Maria", "Garcia"),
        ("Jose", "Martinez"),
        ("Ana", "Lopez"),
        ("Pedro", "Rodriguez")
    ]
    
    print("\nCreando administradores:")
    for nombres, apellidos in admins_data:
        admin = {
            'id': generar_id_admin(nombres, apellidos),
            'nombres': nombres,
            'apellidos': apellidos,
            'dui': generar_dui(),
            'pin_hash': '1234',  # Mismo PIN para pruebas
            'rol': 'ADMIN'
        }
        usuarios.append(admin)
        print(f"  ✓ {admin['id']} - {nombres} {apellidos}")
    
    # Clientes
    nombres_m = ['Juan', 'Carlos', 'Luis', 'Miguel', 'Jose', 'Pedro', 'Manuel', 'Francisco', 'David', 'Jorge']
    nombres_f = ['Maria', 'Ana', 'Laura', 'Sofia', 'Carmen', 'Isabel', 'Elena', 'Patricia', 'Rosa', 'Marta']
    apellidos = ['Perez', 'Garcia', 'Lopez', 'Martinez', 'Rodriguez', 'Gonzalez', 'Hernandez', 'Torres', 'Sanchez', 'Ramirez']
    
    clientes = []
    print("\nCreando clientes:")
    for i in range(1, 21):
        if i % 2 == 0:
            nombres = random.choice(nombres_m)
        else:
            nombres = random.choice(nombres_f)
        
        apellido1 = random.choice(apellidos)
        apellido2 = random.choice(apellidos)
        while apellido2 == apellido1:  # Evitar mismos apellidos
            apellido2 = random.choice(apellidos)
        apellidos_comp = f"{apellido1} {apellido2}"
        
        # Generar ID con iniciales (primera letra de nombres + primera de cada apellido)
        iniciales = nombres[0].upper() + apellido1[0].upper() + apellido2[0].upper()
        id_cliente = f"{iniciales}{i:04d}"
        
        cliente = {
            'id': id_cliente,
            'nombres': nombres,
            'apellidos': apellidos_comp,
            'dui': generar_dui(),
            'pin_hash': generar_pin(),
            'rol': 'CLIENTE'
        }
        usuarios.append(cliente)
        clientes.append(cliente)
        if i <= 5:  # Mostrar solo primeros 5
            print(f"  ✓ {cliente['id']} - {nombres} {apellidos_comp}")
    print(f"  ... y {len(clientes)-5} clientes más")
    
    # Guardar usuarios
    with open('data/usuarios.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'nombres', 'apellidos', 'dui', 'pin_hash', 'rol'])
        writer.writeheader()
        writer.writerows(usuarios)
    
    print(f"\n✓ Total usuarios guardados: {len(usuarios)}")
    
    # 2. Generar cuentas
    cuentas = []
    tipos = ['Ahorro', 'Corriente']
    contador_cuentas = 0
    
    for cliente in clientes:
        # Cada cliente tiene 1-3 cuentas
        num_cuentas = random.randint(1, 3)
        for j in range(num_cuentas):
            contador_cuentas += 1
            saldo_inicial = round(random.uniform(100, 5000), 2)
            estado = 'Activa' if random.random() < 0.9 else 'Bloqueada'  # 90% activas
            
            cuenta = {
                'id_cuenta': f"ACC{contador_cuentas:06d}",
                'id_propietario': cliente['id'],
                'tipo': random.choice(tipos),
                'saldo': saldo_inicial,
                'estado': estado,
                'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            cuentas.append(cuenta)
    
    # Guardar cuentas
    with open('data/cuentas.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id_cuenta', 'id_propietario', 'tipo', 'saldo', 'estado', 'fecha_creacion'])
        writer.writeheader()
        writer.writerows(cuentas)
    
    print(f"✓ Total cuentas generadas: {len(cuentas)}")
    
    # 3. Generar transacciones
    transacciones = []
    contador_trans = 0
    fecha_inicio = datetime(2026, 1, 1)
    fecha_fin = datetime(2026, 2, 28)
    
    # Mapear cuentas a IDs
    ids_cuentas = [c['id_cuenta'] for c in cuentas]
    
    for cuenta_id in ids_cuentas:
        # Cada cuenta tiene 10-50 transacciones
        num_trans = random.randint(10, 50)
        saldo_actual = 500  # Simular saldo
        
        for k in range(num_trans):
            contador_trans += 1
            fecha = generar_fecha_aleatoria(fecha_inicio, fecha_fin)
            
            # Decidir tipo de transacción
            tipo_prob = random.random()
            if tipo_prob < 0.4:  # 40% depósitos
                tipo = 'DEPOSITO'
                monto = round(random.uniform(10, 500), 2)
                saldo_actual += monto
            elif tipo_prob < 0.7:  # 30% retiros
                tipo = 'RETIRO'
                monto = round(random.uniform(5, 200), 2)
                if monto <= saldo_actual:
                    saldo_actual -= monto
                else:
                    monto = saldo_actual * 0.5  # No exceder saldo
                    saldo_actual -= monto
            else:  # 30% transferencias (se manejarán aparte)
                tipo = random.choice(['TRANSFER_IN', 'TRANSFER_OUT'])
                monto = round(random.uniform(20, 300), 2)
                if tipo == 'TRANSFER_IN':
                    saldo_actual += monto
                elif tipo == 'TRANSFER_OUT' and monto <= saldo_actual:
                    saldo_actual -= monto
                else:
                    monto = saldo_actual * 0.3
                    saldo_actual -= monto
            
            transaccion = {
                'id_transaccion': f"TX{contador_trans:06d}",
                'id_cuenta': cuenta_id,
                'tipo': tipo,
                'monto': round(monto, 2),
                'fecha': fecha.strftime('%Y-%m-%d %H:%M:%S'),
                'descripcion': f"{tipo} automático"
            }
            transacciones.append(transaccion)
    
    # Agregar algunas transacciones anómalas para probar detección
    
    # Anomalía Z-Score: depósito muy grande
    cuenta_anom = random.choice(ids_cuentas)
    fecha_anom = datetime(2026, 2, 15, 10, 0, 0)
    contador_trans += 1
    transacciones.append({
        'id_transaccion': f"TX{contador_trans:06d}",
        'id_cuenta': cuenta_anom,
        'tipo': 'DEPOSITO',
        'monto': 5000,
        'fecha': fecha_anom.strftime('%Y-%m-%d %H:%M:%S'),
        'descripcion': 'Depósito anómalo grande'
    })
    
    # Structuring: múltiples depósitos pequeños
    cuenta_struct = random.choice([c for c in ids_cuentas if c != cuenta_anom])
    fecha_struct = datetime(2026, 2, 20, 9, 0, 0)
    for i in range(5):
        contador_trans += 1
        transacciones.append({
            'id_transaccion': f"TX{contador_trans:06d}",
            'id_cuenta': cuenta_struct,
            'tipo': 'DEPOSITO',
            'monto': 45 + i,
            'fecha': (fecha_struct + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S'),
            'descripcion': 'Depósito pequeño'
        })
    
    # Actividad nocturna
    cuenta_nocturna = random.choice([c for c in ids_cuentas if c not in [cuenta_anom, cuenta_struct]])
    for i in range(6):
        contador_trans += 1
        hora = 22 + i if i < 3 else i - 2
        # Corregir horas inválidas
        if hora >= 24:
            hora = hora - 24
        transacciones.append({
            'id_transaccion': f"TX{contador_trans:06d}",
            'id_cuenta': cuenta_nocturna,
            'tipo': random.choice(['DEPOSITO', 'RETIRO']),
            'monto': round(random.uniform(20, 100), 2),
            'fecha': (datetime(2026, 2, 25, hora, random.randint(0, 59), 0)).strftime('%Y-%m-%d %H:%M:%S'),
            'descripcion': 'Actividad nocturna'
        })
    
    # Guardar transacciones
    with open('data/transacciones.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id_transaccion', 'id_cuenta', 'tipo', 'monto', 'fecha', 'descripcion'])
        writer.writeheader()
        writer.writerows(transacciones)
    
    print(f"✓ Total transacciones generadas: {len(transacciones)}")
    
    # 4. Generar transferencias
    transferencias = []
    contador_transf = 0
    
    # Crear transferencias entre cuentas
    num_transferencias = random.randint(30, 50)
    for i in range(num_transferencias):
        origen = random.choice(ids_cuentas)
        destino = random.choice([c for c in ids_cuentas if c != origen])
        monto = round(random.uniform(10, 200), 2)
        fecha = generar_fecha_aleatoria(datetime(2026, 1, 15), datetime(2026, 2, 20))
        
        contador_transf += 1
        transferencia = {
            'id_transferencia': f"TR{contador_transf:06d}",
            'id_cuenta_origen': origen,
            'id_cuenta_destino': destino,
            'monto': monto,
            'fecha': fecha.strftime('%Y-%m-%d %H:%M:%S')
        }
        transferencias.append(transferencia)
    
    # Guardar transferencias
    with open('data/transferencias.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id_transferencia', 'id_cuenta_origen', 'id_cuenta_destino', 'monto', 'fecha'])
        writer.writeheader()
        writer.writerows(transferencias)
    
    print(f"✓ Total transferencias generadas: {len(transferencias)}")
    
    # Mostrar credenciales
    print("\n" + "="*60)
    print("✅ DATOS SEMILLA GENERADOS EXITOSAMENTE")
    print("="*60)
    
    print("\n👑 ADMINISTRADORES:")
    for i, (nombres, apellidos) in enumerate(admins_data, 1):
        siglas = nombres[0].upper() + apellidos[0].upper()
        print(f"  • {nombres} {apellidos}: {siglas}{i:04d} / PIN: 1234")
    
    print("\n👤 CLIENTES (primeros 5):")
    for i, c in enumerate(clientes[:5]):
        print(f"  • {c['id']}: {c['nombres']} {c['apellidos']} - DUI: {c['dui']}, PIN: {c['pin_hash']}")
    print(f"  ... y {len(clientes)-5} clientes más")
    
    print("\nArchivos generados en /data:")
    print("  • usuarios.csv")
    print("  • cuentas.csv")
    print("  • transacciones.csv")
    print("  • transferencias.csv")

if __name__ == "__main__":
    generar_seed()