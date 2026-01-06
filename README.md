# 📊 Monitor de Tasa BCV Automatizado

Este proyecto es un gestor cambiario desarrollado en Python que consulta la tasa oficial del **Banco Central de Venezuela (BCV)** y mantiene un histórico de datos automatizado.

## 🚀 Características
- **Consulta en Tiempo Real:** Obtiene la tasa oficial directamente del BCV usando la librería `pyBCV`.
- **Persistencia de Datos:** Guarda cada consulta en un archivo `historial_tasas.json` para análisis posterior.
- **Automatización Total:** Configurado con **GitHub Actions** para registrar la tasa de forma autónoma de Lunes a Viernes a las 9:00 AM (HLV).
- **Modo Dual:** - `Interactivo`: Para uso manual y cálculos de conversión en PC.
  - `Automático`: Ejecución silenciosa para servidores.

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.10+
- **Librerías:** `pyBCV`, `json`, `datetime`
- **Infraestructura:** GitHub Actions (CI/CD)
- **Sistema Operativo Local:** Arch Linux

## 📂 Estructura del Proyecto
- `history_bcv.py`: Script principal con lógica de negocio.
- `historial_tasas.json`: Base de datos en formato JSON.
- `.github/workflows/main.yml`: Receta de automatización para el servidor.
- `requirements.txt`: Dependencias del sistema.

## 🔧 Instalación y Uso Local
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Ejecutar el programa: `python history_bcv.py`.

---
*Proyecto desarrollado como parte de prácticas de automatización y lógica de programación.*
