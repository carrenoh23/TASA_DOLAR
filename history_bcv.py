import json
import os
import sys
from datetime import datetime

import pyBCV

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
        # Nota: Asegúrate de que pyBCV esté bien instalado en el servidor
        tasa_texto = bcv.get_rate(currency_code="USD", prettify=False)
        return float(tasa_texto.replace(",", "."))
    except Exception as e:
        print(f"⚠️ No se pudo conectar con el BCV: {e}")
        return None


def menu_interactivo():
    historico_tasas = cargar_datos()
    while True:
        print("\n" + "═" * 35)
        print("    GESTOR CAMBIARIO PRO (JSON)")
        print("═" * 35)
        print("[1] Consultar Tasa / Convertir\n[2] Dashboard Histórico\n[3] Salir")

        try:
            opcion = input("\nSeleccione una opción: ")
            if opcion == "1":
                tasa = obtener_tasa_bcv()
                if tasa:
                    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    historico_tasas[fecha_hoy] = tasa
                    guardar_datos(historico_tasas)
                    print(f"✨ Tasa actual: {tasa} Bs.")
            elif opcion == "2":
                for fecha, valor in historico_tasas.items():
                    print(f"{fecha:<22} | {valor:<10.2f}")
            elif opcion == "3":
                break
        except EOFError:
            break


# --- BLOQUE DE EJECUCIÓN (Siempre al final del archivo) ---
if __name__ == "__main__":
    if "--auto" in sys.argv:
        print("🤖 Iniciando modo automático...")
        tasa = obtener_tasa_bcv()
        if tasa:
            historico = cargar_datos()
            # Usamos solo la fecha para el histórico automático (evita duplicados diarios)
            fecha = datetime.now().strftime("%d/%m/%Y")
            historico[fecha] = tasa
            guardar_datos(historico)
            print(f"✅ Tasa {tasa} guardada correctamente.")
    else:
        menu_interactivo()
