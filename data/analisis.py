import csv
import numpy as np
from datetime import datetime

ARCHIVO = "transacciones.csv"

def cargar_datos():
    cuentas = []
    montos = []
    fechas = []
    tipos = []

    with open(ARCHIVO, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cuentas.append(int(row["cuenta_id"]))
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


        def detectar_anomalias(montos):
    media = np.mean(montos)
    desviacion = np.std(montos)

    z = (montos - media) / desviacion

    anomalos = np.where(np.abs(z) > 3)

    print("\nTransacciones anómalas:")
    print(montos[anomalos])


    

