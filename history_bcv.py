import json
import os
from datetime import datetime

import pyBCV  # Asegúrate que sea pyBCV (mayúsculas importan)

ARCHIVO_DATOS = "historial_tasas.json"


def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def guardar_datos(diccionario):
    try:
        with open(ARCHIVO_DATOS, "w") as archivo:
            json.dump(diccionario, archivo, indent=4)
    except IOError as e:
        print(f"❌ Error al guardar en disco: {e}")


def obtener_tasa_bcv():
    try:
        bcv = pyBCV.Currency()
        tasa_texto = bcv.get_rate(currency_code="USD")
        return float(tasa_texto.replace(",", "."))
    except Exception as e:
        print(f"⚠️ No se pudo conectar con el BCV: {e}")
        return None


def menu_interactivo():
    """Esta función solo corre en tu Arch Linux"""
    historico_tasas = cargar_datos()
    while True:
        print("\n" + "═" * 35)
        print("    GESTOR CAMBIARIO PRO (JSON)")
        print("═" * 35)
        print("[1] Consultar Tasa / Convertir")
        print("[2] Dashboard Histórico")
        print("[3] Salir")

        opcion = input("\nSeleccione una opción: ")
        if opcion == "1":
            tasa = obtener_tasa_bcv()
            if tasa:
                fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                historico_tasas[fecha_hoy] = tasa
                guardar_datos(historico_tasas)
                print(f"✨ Tasa actual: {tasa} Bs.")
                try:
                    monto_usd = float(input("Cantidad de USD a cambiar: "))
                    print(f">>> Total: {monto_usd * tasa:.2f} Bs.")
                except ValueError:
                    print("❌ Entrada inválida.")
        elif opcion == "2":
            # ... (tu código de mostrar histórico igual)
            for fecha, valor in historico_tasas.items():
                print(f"{fecha:<22} | {valor:<10.2f}")
        elif opcion == "3":
            break


# --- LÓGICA DE EJECUCIÓN ---
if __name__ == "__main__":
    import sys

    # Si el programa se corre con el argumento 'auto', es GitHub trabajando
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        tasa = obtener_tasa_bcv()
        if tasa:
            historico = cargar_datos()
            fecha = datetime.now().strftime("%d/%m/%Y")
            historico[fecha] = tasa
            guardar_datos(historico)
            print("Automatización: Tasa guardada.")
    else:
        # Si no hay argumentos, es que tú lo abriste en tu PC
        menu_interactivo()
