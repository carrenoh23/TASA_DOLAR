import json
import os
import sys
from datetime import datetime

import pyBCV

ARCHIVO_DATOS = "historial_tasas.json"

# ... (Manten tus funciones cargar_datos, guardar_datos y obtener_tasa_bcv igual)


def menu_interactivo():
    """Lógica para tu terminal en Arch Linux"""
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


# --- ESTA ES LA PARTE QUE EVITA EL ERROR EN GITHUB ---
if __name__ == "__main__":
    # Si el servidor manda el argumento '--auto', ejecutamos sin preguntar nada
    if "--auto" in sys.argv:
        tasa = obtener_tasa_bcv()
        if tasa:
            historico = cargar_datos()
            fecha = datetime.now().strftime("%d/%m/%Y")
            historico[fecha] = tasa
            guardar_datos(historico)
            print(f"✅ Automatización exitosa: Tasa {tasa} guardada.")
    else:
        # Si NO hay '--auto', es porque TÚ lo abriste en tu Arch Linux
        menu_interactivo()
