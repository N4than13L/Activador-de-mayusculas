# Overlay CapsLock

Overlay CapsLock es una herramienta ligera en Python que muestra en pantalla el estado de la tecla **Caps Lock**.  
Incluye opciones avanzadas de personalización, guardado automático de configuración y creación de un instalador profesional para Windows.

---

## 🚀 Características
- ✅ Muestra en pantalla si **Caps Lock** está activado o no.
- ✅ Ventana flotante movible y siempre visible.
- ✅ Menú contextual con clic derecho:
  - Cambiar tema (oscuro, claro, azul, verde).
  - Cambiar opacidad.
  - Cambiar tipografía y tamaño.
- ✅ **Hover interactivo:** cambia el cursor al pasar sobre la ventana.
- ✅ **Guardado automático**: recuerda posición, colores, fuente, tamaño y opacidad.
- ✅ Compatible con **Windows, Linux y macOS**.
- ✅ **Instalador profesional para Windows** con auto-inicio opcional.

---

## 🖥️ Requisitos
- **Python 3.8 o superior** (solo para ejecutar desde código fuente).
- Librerías usadas (todas son parte de la librería estándar de Python):
  - `tkinter` (para la ventana gráfica).
  - `ctypes` (detección de Caps Lock en Windows).
  - `subprocess` (detección en Linux/macOS).
  - `json`, `os`, `threading`, `time`.

---

## 📦 Instalación

### 🔹 Opción 1: Ejecutar desde Python
1. Clonar o descargar el proyecto.
2. Crear un entorno virtual (recomendado):
   ```bash
   python -m venv env
