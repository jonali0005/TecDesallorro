"""
🐾 Mascota de Escritorio
━━━━━━━━━━━━━━━━━━━━━━━━
Una mascota virtual que vive en tu escritorio.
¡Aliméntala o empezará a gritar!

Requisitos: Python 3.8+ con tkinter (incluido en la mayoría de instalaciones)
Ejecutar: python mascota_escritorio.py
"""

import tkinter as tk
import random
import math
import time


# ──────────────────────────────────────────────
#  CONFIGURACIÓN GENERAL (fácil de ajustar)
# ──────────────────────────────────────────────
CONFIG = {
    "hambre_max": 100,          # Nivel máximo de hambre
    "hambre_velocidad": 0.05,   # Qué tan rápido aumenta el hambre (por frame)
    "hambre_grito": 75,         # A partir de qué nivel empieza a gritar
    "comida_intervalo": 8000,   # ms entre apariciones de comida
    "comida_max": 3,            # Máximo de comidas en pantalla a la vez
    "salto_altura": 18,         # Altura máxima del saltito
    "salto_velocidad": 0.15,    # Velocidad de la animación de salto
    "move_intervalo": 40,       # ms entre frames de movimiento (25 fps)
    "nueva_dir_intervalo": 120, # frames antes de cambiar dirección
    "pet_size": 110,             # Tamaño del canvas de la mascota (px)
    "comida_size": 40,          # Tamaño del canvas de comida (px)
}

# Emojis de comida disponibles
COMIDAS = ["🍎", "🍕", "🍩", "🐟", "🍌", "🧀", "🍗", "🍓"]


# ──────────────────────────────────────────────
#  VENTANA TRANSPARENTE BASE
# ──────────────────────────────────────────────
def make_transparent_window(title=""):
    """Crea una ventana sin bordes y transparente."""
    win = tk.Toplevel() if title != "main" else tk.Tk()
    win.title(title)
    win.overrideredirect(True)          # Sin bordes
    win.attributes("-topmost", True)    # Siempre encima
    win.config(bg="white")
    try:
        win.attributes("-transparentcolor", "white")  # Windows/Mac
    except Exception:
        pass
    return win


# ──────────────────────────────────────────────
#  CLASE: COMIDA
# ──────────────────────────────────────────────
class Comida:
    def __init__(self, root, emoji, x, y, on_eaten):
        self.root = root
        self.emoji = emoji
        self.on_eaten = on_eaten          # Callback cuando la come
        self._drag_offset = (0, 0)
        self._being_dragged = False

        size = CONFIG["comida_size"]
        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.config(bg="white")
        try:
            self.win.attributes("-transparentcolor", "white")
        except Exception:
            pass

        self.canvas = tk.Canvas(self.win, width=size, height=size,
                                bg="white", highlightthickness=0)
        self.canvas.pack()
        self.label = self.canvas.create_text(size // 2, size // 2,
                                             text=emoji, font=("Arial", 24))
        self.win.geometry(f"{size}x{size}+{x}+{y}")

        # Drag & Drop
        self.canvas.bind("<ButtonPress-1>", self._drag_start)
        self.canvas.bind("<B1-Motion>", self._drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self._drag_end)

        # Pequeña animación de aparición
        self._appear_scale = 0.3
        self._animate_appear()

    def _animate_appear(self):
        if self._appear_scale < 1.0:
            self._appear_scale = min(1.0, self._appear_scale + 0.08)
            s = int(CONFIG["comida_size"] * self._appear_scale)
            self.canvas.config(width=s, height=s)
            self.canvas.coords(self.label, s // 2, s // 2)
            self.root.after(20, self._animate_appear)
        else:
            self.canvas.config(width=CONFIG["comida_size"],
                               height=CONFIG["comida_size"])
            self.canvas.coords(self.label,
                               CONFIG["comida_size"] // 2,
                               CONFIG["comida_size"] // 2)

    def _drag_start(self, e):
        self._drag_offset = (e.x, e.y)
        self._being_dragged = True

    def _drag_motion(self, e):
        nx = self.win.winfo_x() + e.x - self._drag_offset[0]
        ny = self.win.winfo_y() + e.y - self._drag_offset[1]
        self.win.geometry(f"+{nx}+{ny}")

    def _drag_end(self, e):
        self._being_dragged = False

    def get_center(self):
        """Devuelve el centro de la comida en coordenadas de pantalla."""
        x = self.win.winfo_x() + CONFIG["comida_size"] // 2
        y = self.win.winfo_y() + CONFIG["comida_size"] // 2
        return x, y

    def destroy(self):
        try:
            self.win.destroy()
        except Exception:
            pass


# ──────────────────────────────────────────────
#  CLASE: MASCOTA
# ──────────────────────────────────────────────
class Mascota:
    # Estados posibles
    NORMAL   = "normal"
    FELIZ    = "feliz"
    HAMBRE   = "hambre"
    GRITANDO = "gritando"

    def __init__(self):
        # ── Ventana principal (oculta, solo para ciclo de vida)
        self.root = tk.Tk()
        self.root.withdraw()

        # ── Ventana de la mascota
        self.win = make_transparent_window("main")
        size = CONFIG["pet_size"]
        self.canvas = tk.Canvas(self.win, width=size, height=size,
                                bg="white", highlightthickness=0)
        self.canvas.pack()

        # Texto principal (emoji de la mascota)
        self.pet_text = self.canvas.create_text(
            size // 2, size // 2, text="🐱", font=("Arial", 36))
        # Burbuja de estado (texto flotante)
        self.bubble_text = self.canvas.create_text(
            size // 2, 8, text="", font=("Arial", 12), fill="#333333")

        # ── Estado interno
        self.hambre = 0.0
        self.estado = self.NORMAL
        self._estado_anterior = self.NORMAL

        # ── Posición y movimiento
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.x = float(random.randint(100, sw - 200))
        self.y = float(random.randint(100, sh - 200))
        self.vx = random.choice([-1.5, 1.5])
        self.vy = 0.0
        self.dir_timer = 0

        # ── Salto
        self.salto_phase = 0.0          # 0..2π ciclo continuo
        self.base_y = self.y            # Y de referencia para el salto

        # ── Comidas activas
        self.comidas: list[Comida] = []

        # ── Arrastre de la propia mascota
        self._drag_offset = (0, 0)
        self.canvas.bind("<ButtonPress-1>", self._drag_start)
        self.canvas.bind("<B1-Motion>", self._drag_motion)

        # ── Iniciar ciclos
        self._posicionar()
        self._loop_movimiento()
        self._loop_hambre()
        self._loop_comida()
        self._loop_colision_comida()

        self.root.mainloop()

    # ── Drag mascota ──────────────────────────
    def _drag_start(self, e):
        self._drag_offset = (e.x, e.y)

    def _drag_motion(self, e):
        nx = self.win.winfo_x() + e.x - self._drag_offset[0]
        ny = self.win.winfo_y() + e.y - self._drag_offset[1]
        self.x = float(nx)
        self.y = float(ny)
        self.base_y = self.y
        self._posicionar()

    # ── Posicionamiento ───────────────────────
    def _posicionar(self):
        self.win.geometry(f"+{int(self.x)}+{int(self.y)}")

    # ── Loop de movimiento ────────────────────
    def _loop_movimiento(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        size = CONFIG["pet_size"]

        # Cambio de dirección aleatorio
        self.dir_timer += 1
        if self.dir_timer >= CONFIG["nueva_dir_intervalo"]:
            self.dir_timer = 0
            self.vx = random.uniform(-2.5, 2.5)
            # Pequeña probabilidad de quedarse quieto
            if random.random() < 0.15:
                self.vx = 0.0

        # Rebotar en bordes
        if self.x <= 0 or self.x >= sw - size:
            self.vx *= -1
        if self.y <= 30 or self.y >= sh - size - 50:
            self.base_y = max(30.0, min(self.base_y, float(sh - size - 50)))

        # Mover base
        self.x += self.vx
        self.x = max(0.0, min(self.x, float(sw - size)))

        # Animación de salto sinusoidal
        self.salto_phase += CONFIG["salto_velocidad"]
        offset_y = -abs(math.sin(self.salto_phase)) * CONFIG["salto_altura"]
        self.y = self.base_y + offset_y

        self._posicionar()
        self._actualizar_apariencia()

        self.root.after(CONFIG["move_intervalo"], self._loop_movimiento)

    # ── Apariencia según estado ───────────────
    def _actualizar_apariencia(self):
        emojis = {
            self.NORMAL:   "🐱",
            self.FELIZ:    "😸",
            self.HAMBRE:   "🙀",
            self.GRITANDO: "😱",
        }
        burbujas = {
            self.NORMAL:   "",
            self.FELIZ:    "¡Ñam!",
            self.HAMBRE:   "😿 hambre",
            self.GRITANDO: "¡¡HAMBREEE!!",
        }
        self.canvas.itemconfig(self.pet_text, text=emojis.get(self.estado, "🐱"))
        self.canvas.itemconfig(self.bubble_text, text=burbujas.get(self.estado, ""))

    # ── Loop de hambre ────────────────────────
    def _loop_hambre(self):
        self.hambre = min(CONFIG["hambre_max"],
                          self.hambre + CONFIG["hambre_velocidad"])

        if self.hambre >= CONFIG["hambre_grito"]:
            self.estado = self.GRITANDO
        elif self.hambre >= CONFIG["hambre_grito"] * 0.7:
            self.estado = self.HAMBRE
        elif self.estado not in (self.FELIZ,):
            self.estado = self.NORMAL

        # Si estaba feliz, volver a normal después de un rato
        if self.estado == self.FELIZ and self.hambre > 5:
            self.estado = self.NORMAL

        self.root.after(50, self._loop_hambre)

    # ── Spawn de comida ───────────────────────
    def _loop_comida(self):
        if len(self.comidas) < CONFIG["comida_max"]:
            self._spawn_comida()
        self.root.after(CONFIG["comida_intervalo"], self._loop_comida)

    def _spawn_comida(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        emoji = random.choice(COMIDAS)
        x = random.randint(50, sw - 100)
        y = random.randint(50, sh - 100)
        c = Comida(self.root, emoji, x, y, self._on_eaten)
        self.comidas.append(c)

    def _on_eaten(self, comida):
        """Callback cuando la mascota come algo."""
        self.hambre = max(0.0, self.hambre - 40)
        self.estado = self.FELIZ
        if comida in self.comidas:
            self.comidas.remove(comida)
        comida.destroy()

    # ── Detección de colisión comida-mascota ──
    def _loop_colision_comida(self):
        px = self.x + CONFIG["pet_size"] // 2
        py = self.y + CONFIG["pet_size"] // 2

        for comida in list(self.comidas):
            try:
                cx, cy = comida.get_center()
                dist = math.hypot(px - cx, py - cy)
                # Si la comida está siendo arrastrada cerca de la mascota
                if comida._being_dragged and dist < 55:
                    self._on_eaten(comida)
                    break
                # O si cayó encima de la mascota
                elif not comida._being_dragged and dist < 40:
                    self._on_eaten(comida)
                    break
            except Exception:
                if comida in self.comidas:
                    self.comidas.remove(comida)

        self.root.after(100, self._loop_colision_comida)


# ──────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("🐾 Mascota de Escritorio iniciando...")
    print("   • La mascota saltará por tu pantalla")
    print("   • Aparecerá comida cada ~8 segundos")
    print("   • Arrastra la comida hasta la mascota para alimentarla")
    print("   • Si no la alimentas... ¡gritará!")
    print("   • Cierra la terminal para salir\n")
    Mascota()
