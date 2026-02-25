import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from services.archivo_service import ArchivoService
from datetime import datetime

def asegurar_directorio():
    ruta = "outputs/plots"
    os.makedirs(ruta, exist_ok=True)
    return ruta

def serie_temporal_total():
    asegurar_directorio()
    transacciones = ArchivoService.cargar_transacciones()

    fechas = []
    montos = []

    for t in transacciones:
        fecha = t["fecha"][:10]
        monto = float(t["monto"])
        tipo = t["tipo"]

        if tipo == "DEPOSITO":
            montos.append(monto)
        else:
            montos.append(-monto)

        fechas.append(fecha)

    fechas = np.array(fechas)
    montos = np.array(montos)

    fechas_unicas = np.unique(fechas)
    totales = []

    for f in fechas_unicas:
        totales.append(np.sum(montos[fechas == f]))

    plt.figure(figsize=(10, 5))
    plt.plot(fechas_unicas, totales)
    plt.xticks(fechas_unicas[::max(1, len(fechas_unicas)//10)], rotation=45)
    plt.title("Serie temporal - Total neto del banco por día")
    plt.xlabel("Fecha")
    plt.ylabel("Total neto ($)")
    plt.tight_layout()

    plt.savefig("outputs/plots/serie_temporal.png")
    plt.close()

def heatmap_actividad():
    asegurar_directorio()
    transacciones = ArchivoService.cargar_transacciones()

    cuentas = [t["id_cuenta"] for t in transacciones]
    fechas = [t["fecha"][:10] for t in transacciones]

    cuentas = np.array(cuentas)
    fechas = np.array(fechas)

    cuentas_unicas = np.unique(cuentas)[:10]
    fechas_unicas = np.unique(fechas)
    fechas_unicas = fechas_unicas[::max(1, len(fechas_unicas)//15)]

    matriz = np.zeros((len(cuentas_unicas), len(fechas_unicas)))

    for i, c in enumerate(cuentas_unicas):
        for j, f in enumerate(fechas_unicas):
            matriz[i, j] = np.sum((cuentas == c) & (fechas == f))

    plt.figure(figsize=(12, 6))
    sns.heatmap(matriz, xticklabels=fechas_unicas, yticklabels=cuentas_unicas)
    plt.title("Heatmap de actividad por cuenta")
    plt.xlabel("Fecha")
    plt.ylabel("Cuenta")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("outputs/plots/heatmap.png")
    plt.close()

def boxplot_depositos_por_tipo():
    asegurar_directorio()
    transacciones = ArchivoService.cargar_transacciones()

    depositos_ahorro = []
    depositos_corriente = []

    for t in transacciones:
        if t["tipo"] == "DEPOSITO":
            monto = float(t["monto"])
            tipo_cuenta = t["tipo"]

            if tipo_cuenta == "AHORRO":
                depositos_ahorro.append(monto)
            else:
                depositos_corriente.append(monto)

    plt.figure(figsize=(6, 5))
    plt.boxplot([depositos_ahorro, depositos_corriente],
                labels=["Ahorro", "Corriente"])

    plt.title("Distribución de depósitos por tipo de cuenta")
    plt.xlabel("Tipo de cuenta")
    plt.ylabel("Monto depósito ($)")
    plt.tight_layout()

    plt.savefig("outputs/plots/boxplot.png")
    plt.close()

def scatter_depositos_vs_gastos():
    asegurar_directorio()
    transacciones = ArchivoService.cargar_transacciones()

    resumen = {}

    for t in transacciones:
        cuenta = t["id_cuenta"]
        monto = float(t["monto"])
        tipo = t["tipo"]

        if cuenta not in resumen:
            resumen[cuenta] = {"dep": 0, "gas": 0}

        if tipo == "DEPOSITO":
            resumen[cuenta]["dep"] += monto
        else:
            resumen[cuenta]["gas"] += monto

    depositos = []
    gastos = []

    for cuenta in resumen:
        depositos.append(resumen[cuenta]["dep"])
        gastos.append(resumen[cuenta]["gas"])

    plt.figure(figsize=(6, 5))
    plt.scatter(depositos, gastos)
    plt.title("Scatter: Depósitos vs Gastos por cuenta")
    plt.xlabel("Total depósitos ($)")
    plt.ylabel("Total gastos ($)")
    plt.tight_layout()

    plt.savefig("outputs/plots/scatter.png")
    plt.close()