from services.banco_service import BancoService
from services.archivo_service import ArchivoService
""" from analisis.estadisticas import EstadisticasService
from analisis.anomalias import DetectorAnomalias
from analisis.visualizaciones import Visualizador
from grafos.red_transferencias import RedTransferencias """
from models.cuenta import TipoCuenta
from models.usuario import Cliente
from views.analisis import DetectorAnomalias
from views.analisis import cargar_datos
from views.analisis import estadisticas_por_cuenta
from utils.limpiar_pantalla import limpiar_pantalla
import uuid

class MenuAdmin:
    def __init__(self, admin, banco_service, auth_service):
        self.admin = admin
        self.banco = banco_service
        self.auth = auth_service
    
    def mostrar(self):
        while True:
            limpiar_pantalla()
            print("\n" + "="*50)
            print(f"BANCO - ADMINISTRADOR: {self.admin.nombres} {self.admin.apellidos}")
            print("="*50)
            print("1. Crear cliente")
            print("2. Crear cuenta para cliente")
            print("3. Bloquear/activar cuenta")
            print("4. Listar usuarios/cuentas")
            print("5. Módulo de analítica")
            print("6. Salir")
            print("="*50)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.crear_cliente()
            elif opcion == "2":
                self.crear_cuenta()
            elif opcion == "3":
                self.bloquear_activar_cuenta()
            elif opcion == "4":
                self.listar_usuarios_cuentas()
            elif opcion == "5":
                self.modulo_analitica()
            elif opcion == "6":
                print("Sesión cerrada.")
                limpiar_pantalla()
                break
            elif opcion == "":
                print("No ingresó ninguna opción")
                input("\nPresione Enter para continuar...")
            else:
                print("Opción inválida.")
                input("\nPresione Enter para continuar...")
    
    def crear_cliente(self):
        limpiar_pantalla()
        print("\n--- CREAR NUEVO CLIENTE ---")
        print("(Escriba 'cancelar' en cualquier campo para salir)")
        print("-" * 40)
        
        nombres = input("Nombres: ").strip()
        if nombres == '':
            print("No ingresó ningún nombre")
            input("\nPresione Enter para continuar...")
            return
        if nombres.lower() == 'cancelar':
            print("Operación cancelada")
            input("\nPresione Enter para continuar...")
            return
        
        apellidos = input("Apellidos: ").strip()
        if apellidos == '':
            print("No ingresó ningún apellido")
            input("\nPresione Enter para continuar...")
            return
        if apellidos.lower() == 'cancelar':
            print("Operación cancelada")
            input("\nPresione Enter para continuar...")
            return
        
        dui = input("DUI (formato 00000000-0): ").strip()
        if dui == '':
            print("No ingresó ningún DUI")
            input("\nPresione Enter para continuar...")
            return
        if dui.lower() == 'cancelar':
            print("Operación cancelada")
            input("\nPresione Enter para continuar...")
            return
        
        pin = input("PIN (4 dígitos): ").strip()
        if pin == '':
            print("No ingresó ningún PIN")
            input("\nPresione Enter para continuar...")
            return
        if pin.lower() == 'cancelar':
            print("Operación cancelada")
            input("\nPresione Enter para continuar...")
            return
        
        if len(pin) != 4 or not pin.isdigit():
            print("El PIN debe tener 4 dígitos")
            input("\nPresione Enter para continuar...")
            return
        
        # Cargar usuarios existentes
        usuarios = ArchivoService.cargar_usuarios()
        
        # Verificar DUI único
        for u in usuarios:
            if u['dui'] == dui:
                print("Ya existe un usuario con ese DUI")
                input("\nPresione Enter para continuar...")
                return
        
        # Generar ID para cliente (iniciales + número)
        apellido1, apellido2 = apellidos.split()[0], apellidos.split()[-1] if len(apellidos.split()) > 1 else apellidos
        iniciales = nombres[0].upper() + apellido1[0].upper() + apellido2[0].upper()
        
        # Encontrar el próximo número disponible
        clientes_existentes = [u for u in usuarios if u['rol'] == 'CLIENTE']
        max_num = 0
        for c in clientes_existentes:
            if c['id'][:3] == iniciales:  # Mismas iniciales
                try:
                    num = int(c['id'][3:])
                    if num > max_num:
                        max_num = num
                except:
                    pass
        
        nuevo_num = max_num + 1
        id_cliente = f"{iniciales}{nuevo_num:04d}"
        
        # Agregar nuevo cliente
        nuevo_cliente = {
            'id': id_cliente,
            'nombres': nombres,
            'apellidos': apellidos,
            'dui': dui,
            'pin_hash': pin,
            'rol': 'CLIENTE'
        }
        
        usuarios.append(nuevo_cliente)
        ArchivoService.guardar_usuarios(usuarios)
        
        print(f"Cliente creado exitosamente. ID: {id_cliente}")
        input("\nPresione Enter para continuar...")
    
    def crear_cuenta(self):
        limpiar_pantalla()
        print("\n--- CREAR CUENTA PARA CLIENTE ---")
        print("-" * 40)
        
        # Mostrar clientes disponibles
        usuarios = ArchivoService.cargar_usuarios()
        clientes = [u for u in usuarios if u['rol'] == 'CLIENTE']
        
        if not clientes:
            print("No hay clientes registrados.")
            input("\nPresione Enter para continuar...")
            return
        
        print("\nClientes disponibles:")
        for i, c in enumerate(clientes, 1):
            print(f"{i}. {c['nombres']} {c['apellidos']} (ID: {c['id']})")
        print("0. Cancelar")
        
        try:
            opcion = input("\nSeleccione cliente (0 para cancelar): ").strip()
            
            if opcion == '':
                print("No ingresó ninguna opción")
                input("\nPresione Enter para continuar...")
                return
                
            if opcion == '0' or opcion.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            idx = int(opcion) - 1
            if idx < 0 or idx >= len(clientes):
                print("Selección inválida")
                input("\nPresione Enter para continuar...")
                return
            
            id_cliente = clientes[idx]['id']
            
            print("\nTipo de cuenta:")
            print("1. Ahorro")
            print("2. Corriente")
            print("0. Cancelar")
            tipo_opcion = input("Seleccione tipo: ").strip()
            
            if tipo_opcion == '':
                print("No ingresó ninguna opción")
                input("\nPresione Enter para continuar...")
                return
                
            if tipo_opcion == '0' or tipo_opcion.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            if tipo_opcion not in ['1', '2']:
                print("Opción inválida")
                input("\nPresione Enter para continuar...")
                return
            
            tipo = TipoCuenta.AHORRO if tipo_opcion == "1" else TipoCuenta.CORRIENTE
            
            saldo_input = input("Saldo inicial: $").strip()
            
            if saldo_input == '':
                print("No ingresó ningún monto")
                input("\nPresione Enter para continuar...")
                return
                
            if saldo_input.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            saldo_inicial = float(saldo_input)
            if saldo_inicial < 0:
                print("El saldo inicial no puede ser negativo")
                input("\nPresione Enter para continuar...")
                return
            
            cuenta = self.banco.crear_cuenta(id_cliente, tipo, saldo_inicial)
            print(f"Cuenta creada exitosamente. ID: {cuenta.id_cuenta}")
            
        except ValueError:
            print("Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def bloquear_activar_cuenta(self):
        limpiar_pantalla()
        print("\n--- BLOQUEAR/ACTIVAR CUENTA ---")
        print("-" * 40)
        
        cuentas = self.banco.obtener_todas_cuentas()
        
        if not cuentas:
            print("No hay cuentas registradas.")
            input("\nPresione Enter para continuar...")
            return
        
        print("\nCuentas:")
        for i, c in enumerate(cuentas, 1):
            estado = "BLOQUEADA" if c.estado.value == "Bloqueada" else "ACTIVA"
            print(f"{i}. {c.id_cuenta} - Prop: {c.id_propietario} | {estado} | Saldo: ${c.saldo:.2f}")
        print("0. Cancelar")
        
        try:
            opcion = input("\nSeleccione cuenta (0 para cancelar): ").strip()
            
            if opcion == '':
                print("No ingresó ninguna opción")
                input("\nPresione Enter para continuar...")
                return
                
            if opcion == '0' or opcion.lower() == 'cancelar':
                print("Operación cancelada")
                input("\nPresione Enter para continuar...")
                return
            
            idx = int(opcion) - 1
            if idx < 0 or idx >= len(cuentas):
                print("Selección inválida")
                input("\nPresione Enter para continuar...")
                return
            
            cuenta = cuentas[idx]
            estado_anterior = cuenta.estado.value
            
            self.banco.bloquear_activar_cuenta(cuenta.id_cuenta)
            nuevo_estado = "ACTIVADA" if estado_anterior == "Bloqueada" else "BLOQUEADA"
            
            print(f"Cuenta {nuevo_estado}")
            
        except ValueError:
            print("Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def listar_usuarios_cuentas(self):
        limpiar_pantalla()
        print("\n--- LISTADO DE USUARIOS Y CUENTAS ---")
        
        usuarios = ArchivoService.cargar_usuarios()
        cuentas = self.banco.obtener_todas_cuentas()
        
        print(f"\nTotal usuarios: {len(usuarios)}")
        print(f"Total cuentas: {len(cuentas)}")
        
        print("\n" + "-"*50)
        for u in usuarios:
            rol = "ADMIN" if u['rol'] == 'ADMIN' else "CLIENTE"
            print(f"{rol} | {u['id']} | {u['nombres']} {u['apellidos']} | DUI: {u['dui']}")
            
            if u['rol'] == 'CLIENTE':
                cuentas_cliente = [c for c in cuentas if c.id_propietario == u['id']]
                if cuentas_cliente:
                    for c in cuentas_cliente:
                        estado = "ACT" if c.estado.value == "Activa" else "BLO"
                        print(f"  └─ {estado} {c.id_cuenta} | {c.tipo.value} | ${c.saldo:.2f}")
                else:
                    print("  └─ Sin cuentas")
            print()
        
        input("\nPresione Enter para continuar...")

    def modulo_analitica(self):
        limpiar_pantalla()
        print("\n--- MÓDULO DE ANALÍTICA ---")
        print("-" * 40)

        print("1. Estadísticas por cuenta")
        print("2. Detectar anomalías por monto (Z-score)")
        print("3. Detectar Structuring")
        print("4. Detectar Actividad Nocturna")
        print("0. Volver")

        opcion = input("\nSeleccione una opción: ").strip()
        #ESTADÍSTICAS
        if opcion == "1":
            try:
                cuentas, montos, fechas, tipos = cargar_datos()
                estadisticas_por_cuenta(cuentas, montos, tipos)
            except Exception as e:
                print("Error al cargar datos:", e)
                self.modulo_analitica()
        #Z-SCORE ANOMALÍAS
        elif opcion == "2":
            try:
                _, montos, _, _ = cargar_datos()
                DetectorAnomalias.detectar_anomalias(montos)
            except Exception as e:
                print("Error al analizar anomalías:", e)
                self.modulo_analitica()
        #STRUCTURING
        elif opcion == "3":
            resultados = DetectorAnomalias.detectar_structuring()

            if not resultados:
                print("\nNo se detectaron casos de structuring.")
                self.modulo_analitica()
            else:
                print("\nCasos detectados:")
                for r in resultados:
                    print(f"Cuenta: {r['id_cuenta']} | Fecha: {r['fecha']}")
        #ACTIVIDAD NOCTURNA
        elif opcion == "4":
            resultados = DetectorAnomalias.detectar_actividad_nocturna()

            if not resultados:
                print("\nNo se detectó actividad nocturna inusual.")
                self.modulo_analitica()
            else:
                print("\nCasos detectados:")
                for r in resultados:
                    print(f"Cuenta: {r['id_cuenta']} | Fecha: {r['fecha']}")
        elif opcion == "0":
            return self.mostrar()
        else:
            print("Opción inválida.")

        input("\nPresione Enter para continuar...")
    
    
"""     def modulo_analitica(self):
        while True:
            limpiar_pantalla()
            print("\n" + "="*50)
            print("MÓDULO DE ANALÍTICA")
            print("="*50)
            print("1. Estadísticas por usuario")
            print("2. Dashboard administrador")
            print("3. Detección de anomalías")
            print("4. Generar visualizaciones")
            print("5. Análisis de red de transferencias")
            print("6. Exportar reportes")
            print("7. Volver")
            print("="*50)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.estadisticas_usuario()
            elif opcion == "2":
                self.dashboard_admin()
            elif opcion == "3":
                self.detectar_anomalias()
            elif opcion == "4":
                self.generar_visualizaciones()
            elif opcion == "5":
                self.analisis_red()
            elif opcion == "6":
                self.exportar_reportes()
            elif opcion == "7":
                break
            elif opcion == "":
                print("❌ No ingresó ninguna opción")
                input("\nPresione Enter para continuar...")
            else:
                print("Opción inválida.")
                input("\nPresione Enter para continuar...")
    
    def estadisticas_usuario(self):
        limpiar_pantalla()
        print("\n--- ESTADÍSTICAS POR USUARIO ---")
        
        transacciones = self.banco.obtener_todas_transacciones()
        usuarios = ArchivoService.cargar_usuarios()
        cuentas = self.banco.obtener_todas_cuentas()
        
        # Mapear cuentas a usuarios
        cuentas_por_usuario = {}
        for c in cuentas:
            if c.id_propietario not in cuentas_por_usuario:
                cuentas_por_usuario[c.id_propietario] = []
            cuentas_por_usuario[c.id_propietario].append(c.id_cuenta)
        
        # Calcular estadísticas por usuario
        for usuario in usuarios:
            if usuario['rol'] == 'CLIENTE':
                print(f"\n👤 {usuario['nombres']} {usuario['apellidos']} (ID: {usuario['id']})")
                
                cuentas_usuario = cuentas_por_usuario.get(usuario['id'], [])
                transacciones_usuario = [
                    t for t in transacciones 
                    if t['id_cuenta'] in cuentas_usuario
                ]
                
                if transacciones_usuario:
                    stats = EstadisticasService.calcular_estadisticas_usuario(transacciones_usuario)
                    
                    print(f"  Total depósitos: ${stats['total_depositos']:.2f}")
                    print(f"  Promedio diario: ${stats['promedio_diario']:.2f}")
                    print(f"  Desviación estándar: ${stats['desviacion']:.2f}")
                    print(f"  Percentiles: p50=${stats['p50']:.2f}, p90=${stats['p90']:.2f}, p99=${stats['p99']:.2f}")
                    print(f"  Ratio depósitos/gastos: {stats['ratio']:.2f}")
                else:
                    print("  Sin transacciones")
        
        input("\nPresione Enter para continuar...")
    
    def dashboard_admin(self):
        limpiar_pantalla()
        print("\n--- DASHBOARD ADMINISTRADOR ---")
        
        transacciones = self.banco.obtener_todas_transacciones()
        stats = EstadisticasService.calcular_estadisticas_admin(transacciones)
        
        print("\n📊 TOP 5 DÍAS PICO (por número de transacciones):")
        for fecha, count in stats['top_dias_pico']:
            print(f"  {fecha}: {count} transacciones")
        
        print("\n💰 TOTAL DIARIO DEL BANCO (últimos 5 días):")
        dias_ordenados = sorted(stats['transacciones_por_dia'].items(), reverse=True)[:5]
        for fecha, datos in dias_ordenados:
            print(f"  {fecha}: Dep: ${datos['depositos']:.2f} | Gas: ${datos['gastos']:.2f} | Neto: ${datos['total']:.2f}")
        
        print("\n🏆 TOP 10 CUENTAS POR DEPÓSITOS:")
        for cuenta, monto in stats['top_cuentas_depositos'][:5]:
            print(f"  {cuenta}: ${monto:.2f}")
        
        print("\n💸 TOP 10 CUENTAS POR GASTOS:")
        for cuenta, monto in stats['top_cuentas_gastos'][:5]:
            print(f"  {cuenta}: ${monto:.2f}")
        
        input("\nPresione Enter para continuar...")
    
    def detectar_anomalias(self):
        limpiar_pantalla()
        print("\n--- DETECCIÓN DE ANOMALÍAS ---")
        
        transacciones = self.banco.obtener_todas_transacciones()
        anomalias = DetectorAnomalias.detectar_todas(transacciones)
        
        print(f"\n🔍 Z-SCORE (|z|>3): {len(anomalias['zscore'])} anomalías")
        for a in anomalias['zscore'][:5]:
            print(f"  • {a['descripcion']}")
        
        print(f"\n💰 STRUCTURING: {len(anomalias['structuring'])} anomalías")
        for a in anomalias['structuring'][:5]:
            print(f"  • Cuenta {a['cuenta']}: {a['descripcion']}")
        
        print(f"\n🌙 ACTIVIDAD NOCTURNA: {len(anomalias['nocturnas'])} anomalías")
        for a in anomalias['nocturnas'][:5]:
            print(f"  • {a['descripcion']}")
        
        total = sum(len(v) for v in anomalias.values())
        print(f"\n📋 TOTAL ANOMALÍAS DETECTADAS: {total}")
        
        input("\nPresione Enter para continuar...")
    
    def generar_visualizaciones(self):
        limpiar_pantalla()
        print("\n--- GENERAR VISUALIZACIONES ---")
        
        transacciones = self.banco.obtener_todas_transacciones()
        cuentas = self.banco.obtener_todas_cuentas()
        
        Visualizador.generar_todos(transacciones, cuentas)
        
        input("\nPresione Enter para continuar...")
    
    def analisis_red(self):
        limpiar_pantalla()
        print("\n--- ANÁLISIS DE RED DE TRANSFERENCIAS ---")
        
        transferencias = self.banco.obtener_todas_transferencias()
        
        if not transferencias:
            print("No hay transferencias registradas para analizar.")
            input("\nPresione Enter para continuar...")
            return
        
        red = RedTransferencias(transferencias)
        red.imprimir_metricas()
        red.visualizar()
        
        input("\nPresione Enter para continuar...")
    
    def exportar_reportes(self):
        limpiar_pantalla()
        print("\n--- EXPORTAR REPORTES ---")
        
        import csv
        
        transacciones = self.banco.obtener_todas_transacciones()
        anomalias = DetectorAnomalias.detectar_todas(transacciones)
        
        # Reporte de anomalías
        with open('outputs/reporte_anomalias.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Tipo', 'Cuenta', 'Fecha', 'Descripción'])
            
            for a in anomalias['zscore']:
                writer.writerow(['Z-Score', a['cuenta'], a['fecha'], a['descripcion']])
            for a in anomalias['structuring']:
                writer.writerow(['Structuring', a['cuenta'], a['fecha'], a['descripcion']])
            for a in anomalias['nocturnas']:
                writer.writerow(['Nocturna', a['cuenta'], a['fecha'], a['descripcion']])
        
        print("✅ Reportes exportados a outputs/reporte_anomalias.csv")
        input("\nPresione Enter para continuar...") """