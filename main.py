import sys
import platform
import tkinter as tk
import threading
import time
import json
import os

# Archivo de configuración persistente
CONFIG_FILE = "config_overlay.json"

# Configuración por defecto
config_default = {
    "fuente": "Arial",
    "tamaño_fuente": 14,
    "color_fondo": "black",
    "color_texto": "white",
    "opacidad": 0.8
}

# --- Cargar configuración previa si existe ---
def cargar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return config_default.copy()

# --- Guardar configuración ---
def guardar_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# Cargar configuración inicial
config = cargar_config()

# Detectar sistema operativo
SO = platform.system()

# --- Función para leer Caps Lock según el sistema ---
if SO == "Windows":
    import ctypes
    def capslock_activo():
        return bool(ctypes.WinDLL("User32.dll").GetKeyState(0x14) & 1)

elif SO == "Linux":
    import subprocess
    def capslock_activo():
        try:
            estado = subprocess.check_output("xset q | grep Caps", shell=True).decode()
            return "on" in estado
        except:
            return False

elif SO == "Darwin":  # macOS
    import subprocess
    def capslock_activo():
        try:
            estado = subprocess.check_output(
                "hidutil eventstatus | grep CAPS", shell=True
            ).decode()
            return "= 1" in estado
        except:
            return False
else:
    print("Sistema operativo no soportado.")
    sys.exit(1)

# --- Actualizar mensaje dinámico ---
def actualizar_mensaje():
    while True:
        if capslock_activo():
            etiqueta.config(text="Caps Lock: Activado", fg=config["color_texto"])
        else:
            etiqueta.config(text="Caps Lock: Desactivado", fg=config["color_texto"])
        time.sleep(0.3)

# --- Movimiento ventana ---
def empezar_mover(event):
    ventana.x_click = event.x
    ventana.y_click = event.y

def mover_ventana(event):
    x = ventana.winfo_x() + (event.x - ventana.x_click)
    y = ventana.winfo_y() + (event.y - ventana.y_click)
    ventana.geometry(f"+{x}+{y}")

# --- Menú contextual ---
def mostrar_menu(event):
    menu_opciones.tk_popup(event.x_root, event.y_root)

def cerrar_overlay():
    ventana.destroy()
    sys.exit(0)

# --- Cambiar tema ---
def cambiar_tema(fondo, texto):
    config["color_fondo"] = fondo
    config["color_texto"] = texto
    ventana.configure(bg=fondo)
    etiqueta.configure(bg=fondo, fg=texto)
    guardar_config()

# --- Cambiar opacidad ---
def cambiar_opacidad(valor):
    config["opacidad"] = valor
    ventana.attributes("-alpha", valor)
    guardar_config()

# --- Cambiar tipografía y ajustar tamaño ---
def cambiar_tipografia(fuente, tamaño):
    config["fuente"] = fuente
    config["tamaño_fuente"] = tamaño
    etiqueta.config(font=(fuente, tamaño))
    guardar_config()

    # Ajustar tamaño ventana automáticamente
    nuevo_ancho = max(200, tamaño * 18)
    nuevo_alto = max(50, tamaño * 5)
    ventana.geometry(f"{nuevo_ancho}x{nuevo_alto}+{ventana.winfo_x()}+{ventana.winfo_y()}")

# --- Hover cursor ---
def cursor_hover(event):
    ventana.config(cursor="hand2")

def cursor_normal(event):
    ventana.config(cursor="arrow")

# --- Crear ventana ---
ventana = tk.Tk()
ventana.title("Estado de Caps Lock")
ventana.overrideredirect(True)
ventana.attributes("-topmost", True)
ventana.attributes("-alpha", config["opacidad"])
ventana.configure(bg=config["color_fondo"])

# Tamaño inicial basado en fuente
ancho_inicial = max(200, config["tamaño_fuente"] * 18)
alto_inicial = max(50, config["tamaño_fuente"] * 5)
pos_x = ventana.winfo_screenwidth() - ancho_inicial - 60
pos_y = ventana.winfo_screenheight() - alto_inicial - 60
ventana.geometry(f"{ancho_inicial}x{alto_inicial}+{pos_x}+{pos_y}")

# Etiqueta principal
etiqueta = tk.Label(ventana, text="Caps Lock: Desactivado",
                    font=(config["fuente"], config["tamaño_fuente"]),
                    fg=config["color_texto"], bg=config["color_fondo"])
etiqueta.pack(expand=True, fill="both")

# Eventos
etiqueta.bind("<Button-1>", empezar_mover)
etiqueta.bind("<B1-Motion>", mover_ventana)
etiqueta.bind("<Button-3>", mostrar_menu)
etiqueta.bind("<Enter>", cursor_hover)
etiqueta.bind("<Leave>", cursor_normal)

# --- Menú contextual principal ---
menu_opciones = tk.Menu(ventana, tearoff=0, bg="gray15", fg="white",
                        activebackground="gray30", activeforeground="white")
menu_opciones.add_command(label="Cerrar", command=cerrar_overlay)

# Submenú: Cambiar tema con vista previa
menu_tema = tk.Menu(menu_opciones, tearoff=0)
temas = [
    ("Oscuro (Negro)", "black", "white"),
    ("Claro (Blanco)", "white", "black"),
    ("Azul", "#13133E", "#16CDFF"),
    ("Verde", "#0F2F0F", "#4EFF86"),
    ("Rojo", "#2F0F0F", "#F84A4A"),
    ("Morado", "#290F2F", "#A34DFF"),
    ("Naranja", "#2F210F", "#FF9524"),
    ("Amarillo", "#2F3219", "#B6C13D")
]
for nombre, fondo, texto in temas:
    menu_tema.add_command(
        label=nombre,
        command=lambda f=fondo, t=texto: cambiar_tema(f, t),
        foreground=texto,
        background=fondo if fondo != "white" else "gray90",
        font=("Arial", 11)
    )

# Submenú: Cambiar opacidad con vista previa
menu_opacidad = tk.Menu(menu_opciones, tearoff=0)
niveles_opacidad = [
    ("100%", 1.0),
    ("80%", 0.8),
    ("60%", 0.6),
    ("40%", 0.4)
]
for nombre, valor in niveles_opacidad:
    brillo = int(255 * valor)
    color_preview = f"#{brillo:02x}{brillo:02x}{brillo:02x}"
    menu_opacidad.add_command(
        label=nombre,
        command=lambda v=valor: cambiar_opacidad(v),
        foreground=color_preview,
        font=("Arial", 11)
    )

# Submenú: Tipografía con vista previa
menu_fuente = tk.Menu(menu_opciones, tearoff=0)
fuentes = [
    ("Arial Pequeño", "Arial", 12),
    ("Arial Grande", "Arial", 20),
    ("Courier Mediano", "Courier", 16),
    ("Verdana Grande", "Verdana", 22),
    ("Times Extra Grande", "Times", 26)
]
for nombre, fuente, tamaño in fuentes:
    menu_fuente.add_command(
        label=nombre,
        command=lambda f=fuente, t=tamaño: cambiar_tipografia(f, t),
        font=(fuente, 12)
    )

# Añadir submenús
menu_opciones.add_cascade(label="Cambiar Tema", menu=menu_tema)
menu_opciones.add_cascade(label="Cambiar Opacidad", menu=menu_opacidad)
menu_opciones.add_cascade(label="Tipografía y Tamaño", menu=menu_fuente)

# Hilo de actualización
threading.Thread(target=actualizar_mensaje, daemon=True).start()

ventana.mainloop()
