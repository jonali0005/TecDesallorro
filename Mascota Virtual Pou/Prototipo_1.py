import os
import random
import math
import sys
import win32con
import win32gui
from dataclasses import dataclass

from PySide6 import QtCore, QtGui, QtWidgets

# -----------------------------
# Config
# -----------------------------
SPRITES_DIR = os.path.join(os.path.dirname(__file__), "sprits")

FPS = 60
ANIM_FPS = 12

PET_SIZE = 128                 # tamaño del sprite (cuadrado)
SPEED = 260.0                  # px/seg
HOP_HEIGHT = 28                # altura del “saltito”
HOP_FREQ = 2.2                 # frecuencia del salto (más alto = más rápido)
TARGET_CHANGE_MIN = 1.2        # segundos
TARGET_CHANGE_MAX = 3.0

ALWAYS_ON_TOP = True
CLICK_THROUGH_WINDOWS = True   # requiere pywin32

# -----------------------------
# Windows click-through helper
# -----------------------------
def try_enable_click_through_windows(widget: QtWidgets.QWidget):
    """
    Hace la ventana transparente a clics en Windows.
    Requiere pywin32. Si no está, no pasa nada.
    """
    try:
        import win32con
        import win32gui
    except Exception:
        return  # no disponible

    hwnd = int(widget.winId())
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

    # WS_EX_LAYERED: permite transparencia
    # WS_EX_TRANSPARENT: hace click-through (los clicks "atraviesan")
    # WS_EX_TOOLWINDOW: evita aparecer en Alt+Tab
    ex_style |= (win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOOLWINDOW)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    # Asegura que el alpha funcione (255 = opaco, pero fondo es transparente por Qt)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)


@dataclass
class Target:
    x: float
    y: float


class DesktopPet(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(PET_SIZE, PET_SIZE)

        # Ventana sin bordes + transparente
        flags = QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool
        if ALWAYS_ON_TOP:
            flags |= QtCore.Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)

        # Cargar sprites
        self.frames = self.load_frames(SPRITES_DIR)
        self.frame_index = 0
        self.frame_timer = 0.0

        # Estado de movimiento
        self.posf = QtCore.QPointF(300, 300)
        self.target = self.random_target()
        self.change_target_in = random.uniform(TARGET_CHANGE_MIN, TARGET_CHANGE_MAX)

        # Para el saltito (fase)
        self.hop_phase = random.random() * math.pi * 2

        # Timer principal
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(int(1000 / FPS))

        self.last_time = QtCore.QElapsedTimer()
        self.last_time.start()

        # Pantallas
        self.screen_geo = QtGui.QGuiApplication.primaryScreen().availableGeometry()

        # Colocar inicial
        self.move(int(self.posf.x()), int(self.posf.y()))
        self.show()

        # Click-through en Windows (opcional)
        if CLICK_THROUGH_WINDOWS and sys.platform.startswith("win"):
            QtCore.QTimer.singleShot(50, lambda: try_enable_click_through_windows(self))

    def load_frames(self, folder: str):
        frames = []
        if os.path.isdir(folder):
            for name in sorted(os.listdir(folder)):
                if name.lower().endswith(".png"):
                    pix = QtGui.QPixmap(os.path.join(folder, name))
                    if not pix.isNull():
                        frames.append(pix.scaled(
                            PET_SIZE, PET_SIZE,
                            QtCore.Qt.KeepAspectRatio,
                            QtCore.Qt.SmoothTransformation
                        ))
        return frames

    def random_target(self) -> Target:
        g = self.screen_geo
        margin = 20
        x = random.randint(g.left() + margin, g.right() - PET_SIZE - margin)
        y = random.randint(g.top() + margin, g.bottom() - PET_SIZE - margin)
        return Target(float(x), float(y))

    def tick(self):
        # dt en segundos
        ms = self.last_time.restart()
        dt = ms / 1000.0
        if dt <= 0:
            return

        # Actualizar objetivo cada cierto tiempo
        self.change_target_in -= dt
        if self.change_target_in <= 0:
            self.target = self.random_target()
            self.change_target_in = random.uniform(TARGET_CHANGE_MIN, TARGET_CHANGE_MAX)

        # Movimiento hacia objetivo
        dx = self.target.x - self.posf.x()
        dy = self.target.y - self.posf.y()
        dist = math.hypot(dx, dy)

        if dist > 3:
            vx = (dx / dist) * SPEED
            vy = (dy / dist) * SPEED
            self.posf.setX(self.posf.x() + vx * dt)
            self.posf.setY(self.posf.y() + vy * dt)
        else:
            # Si llegó, elegir otro pronto
            self.change_target_in = min(self.change_target_in, 0.25)

        # Mantener dentro de pantalla
        g = self.screen_geo
        x = max(g.left(), min(self.posf.x(), g.right() - PET_SIZE))
        y = max(g.top(),  min(self.posf.y(), g.bottom() - PET_SIZE))
        self.posf = QtCore.QPointF(x, y)

        # Saltito (offset vertical)
        self.hop_phase += dt * HOP_FREQ * 2 * math.pi
        hop = abs(math.sin(self.hop_phase)) * HOP_HEIGHT  # 0..HOP_HEIGHT

        # Animación frames
        self.frame_timer += dt
        if self.frames:
            if self.frame_timer >= (1.0 / ANIM_FPS):
                self.frame_timer = 0.0
                self.frame_index = (self.frame_index + 1) % len(self.frames)

        # Mover ventana (y hop hacia arriba)
        self.move(int(self.posf.x()), int(self.posf.y() - hop))
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if self.frames:
            # Dibujar sprite actual centrado
            pix = self.frames[self.frame_index]
            x = (self.width() - pix.width()) // 2
            y = (self.height() - pix.height()) // 2
            painter.drawPixmap(x, y, pix)
        else:
            # Si no hay sprites, dibuja un "blob" simpático
            rect = QtCore.QRectF(14, 22, self.width() - 28, self.height() - 44)
            painter.setBrush(QtGui.QColor(135, 210, 180, 220))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawEllipse(rect)

            # Ojos
            painter.setBrush(QtGui.QColor(30, 30, 30, 230))
            painter.drawEllipse(QtCore.QPointF(self.width() * 0.42, self.height() * 0.48), 8, 8)
            painter.drawEllipse(QtCore.QPointF(self.width() * 0.58, self.height() * 0.48), 8, 8)

            # Brillos
            painter.setBrush(QtGui.QColor(255, 255, 255, 220))
            painter.drawEllipse(QtCore.QPointF(self.width() * 0.40, self.height() * 0.46), 3, 3)
            painter.drawEllipse(QtCore.QPointF(self.width() * 0.56, self.height() * 0.46), 3, 3)

            # Sonrisa
            pen = QtGui.QPen(QtGui.QColor(30, 30, 30, 220), 3)
            painter.setPen(pen)
            painter.drawArc(int(self.width()*0.40), int(self.height()*0.60), 40, 24, 0, 180 * 16)


def main():
    app = QtWidgets.QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()