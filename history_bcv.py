import json
import os
from datetime import datetime

import pyBCV

# CONFIGURACIÓN: Nombre del archivo donde guardaremos los datos
ARCHIVO_DATOS = "historial_tasas.json"


def cargar_datos():
    """Carga el historial desde el archivo JSON si existe."""
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def guardar_datos(diccionario):
    """Guarda el diccionario actual en el archivo JSON."""
    try:
        with open(ARCHIVO_DATOS, "w") as archivo:
            json.dump(diccionario, archivo, indent=4)
    except IOError as e:
        print(f"❌ Error al guardar en disco: {e}")


def obtener_tasa_bcv():
    """Consulta la tasa oficial y la limpia."""
    try:
        bcv = pyBCV.Currency()
        tasa_texto = bcv.get_rate(currency_code="USD")
        return float(tasa_texto.replace(",", "."))
    except Exception as e:
        print(f"⚠️ No se pudo conectar con el BCV: {e}")
        return None


# --- INICIO DEL PROGRAMA ---
# Cargamos lo que haya guardado de sesiones anteriores
historico_tasas = cargar_datos()

while True:
    print("\n" + "═" * 35)
    print("   GESTOR CAMBIARIO PRO (JSON)")
    print("═" * 35)
    print("[1] Consultar Tasa / Convertir")
    print("[2] Dashboard Histórico")
    print("[3] Salir")

    opcion = input("\nSeleccione una opción: ")

    if opcion == "1":
        tasa = obtener_tasa_bcv()
        if tasa:
            fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Guardamos la tasa en nuestro diccionario
            historico_tasas[fecha_hoy] = tasa
            # Guardamos inmediatamente en el archivo .json
            guardar_datos(historico_tasas)

            print(f"✨ Tasa actual: {tasa} Bs.")
            try:
                monto_usd = float(input("Cantidad de USD a cambiar: "))
                print(f">>> Total: {monto_usd * tasa:.2f} Bs.")
            except ValueError:
                print("❌ Entrada inválida. Use números.")

    elif opcion == "2":
        print(f"\n{'FECHA Y HORA':<22} | {'TASA (Bs)':<10}")
        print("─" * 35)
        if not historico_tasas:
            print("Historial vacío.")
        else:
            # Mostramos los datos cargados del JSON
            for fecha, valor in historico_tasas.items():
                print(f"{fecha:<22} | {valor:<10.2f}")
        print("─" * 35)

    elif opcion == "3":
        print("Finalizando sistema. Datos protegidos en .json")
        break

# Parte de automatizacion de programa
if __name__ == "__main__":
    # Si detecta que NO hay una persona (modo automático)
    # simplemente graba la tasa y se cierra.
    tasa = obtener_tasa_bcv()
    if tasa:
        historico = cargar_datos()
        fecha = datetime.now().strftime("%d/%m/%Y")
        historico[fecha] = tasa
        guardar_datos(historico)
