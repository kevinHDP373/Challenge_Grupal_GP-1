# archivo: analisis/anomalias.py
import csv
import numpy as np
from datetime import datetime
from services.archivo_service import ArchivoService
from datetime import datetime

ARCHIVO = "data/transacciones.csv"

def cargar_datos():
    cuentas = []
    montos = []
    fechas = []
    tipos = []

    with open(ARCHIVO, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cuentas.append(row["id_cuenta"])
            montos.append(float(row["monto"]))
            fechas.append(row["fecha"])
            tipos.append(row["tipo"])

    return np.array(cuentas), np.array(montos), np.array(fechas), np.array(tipos)


def estadisticas_por_cuenta(cuentas, montos, tipos):
    cuentas_unicas = np.unique(cuentas)

    for c in cuentas_unicas:
        mask = cuentas == c
        montos_cuenta = montos[mask]
        tipos_cuenta = tipos[mask]

        depositos = montos_cuenta[tipos_cuenta == "DEPOSITO"]
        gastos = montos_cuenta[tipos_cuenta != "DEPOSITO"]

        total_dep = np.sum(depositos)
        promedio = np.mean(montos_cuenta)
        desviacion = np.std(montos_cuenta)

        p50 = np.percentile(montos_cuenta, 50)
        p90 = np.percentile(montos_cuenta, 90)
        p99 = np.percentile(montos_cuenta, 99)

        ratio = total_dep / np.sum(gastos) if np.sum(gastos) > 0 else total_dep

        print("\nCuenta:", c)
        print("Total depósitos:", total_dep)
        print("Promedio:", promedio)
        print("Desviación:", desviacion)
        print("Percentiles:", p50, p90, p99)
        print("Ratio dep/gastos:", ratio)

class DetectorAnomalias:
    @staticmethod
    def detectar_anomalias(montos):
            media = np.mean(montos)
            desviacion = np.std(montos)
            z = (montos - media) / desviacion
            anomalos = np.where(np.abs(z) > 3)
            print("\nTransacciones anómalas:")
            print(montos[anomalos])

    @staticmethod
    def detectar_structuring():
        transacciones = ArchivoService.cargar_transacciones()
        if not transacciones:
            return []

        cuentas = np.array([t["id_cuenta"] for t in transacciones])
        tipos = np.array([t["tipo"] for t in transacciones])
        montos = np.array([float(t["monto"]) for t in transacciones])
        fechas = np.array([t["fecha"][:10] for t in transacciones])  # YYYY-MM-DD

        mask = (tipos == "DEPOSITO") & (montos <= 50)

        cuentas_f = cuentas[mask]
        fechas_f = fechas[mask]

        if len(cuentas_f) == 0:
            return []

        combinaciones = np.char.add(cuentas_f, "_" + fechas_f)
        uniques, counts = np.unique(combinaciones, return_counts=True)

        anomalas = uniques[counts >= 4]

        resultado = []
        for item in anomalas:
            cuenta, fecha = item.split("_")
            resultado.append({
                "tipo_anomalia": "STRUCTURING",
                "id_cuenta": cuenta,
                "fecha": fecha
            })

        return resultado

    @staticmethod
    def detectar_actividad_nocturna():
        transacciones = ArchivoService.cargar_transacciones()
        if not transacciones:
            return []

        cuentas = np.array([t["id_cuenta"] for t in transacciones])
        fechas_full = np.array([t["fecha"] for t in transacciones])

        horas = np.array([
            datetime.strptime(f, "%Y-%m-%d %H:%M:%S").hour
            for f in fechas_full
        ])

        fechas = np.array([f[:10] for f in fechas_full])

        mask_nocturno = (horas >= 21) | (horas < 4)

        cuentas_n = cuentas[mask_nocturno]
        fechas_n = fechas[mask_nocturno]

        if len(cuentas_n) == 0:
            return []

        combinaciones = np.char.add(cuentas_n, "_" + fechas_n)
        uniques, counts = np.unique(combinaciones, return_counts=True)

        resultado = []

        cuentas_unicas = np.unique(cuentas_n)

        for cuenta in cuentas_unicas:
            mask_cuenta = np.char.startswith(uniques, cuenta + "_")
            dias = uniques[mask_cuenta]
            valores = counts[mask_cuenta]

            if len(valores) < 2:
                continue

            media = np.mean(valores)
            std = np.std(valores)

            if std == 0:
                continue

            z_scores = (valores - media) / std

            dias_anomalos = dias[np.abs(z_scores) > 2]

            for d in dias_anomalos:
                _, fecha = d.split("_")
                resultado.append({
                    "tipo_anomalia": "ACTIVIDAD_NOCTURNA",
                    "id_cuenta": cuenta,
                    "fecha": fecha
                })

        return resultado