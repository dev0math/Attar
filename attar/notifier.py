import sys
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect, QApplication, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QParallelAnimationGroup
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath

class NotificationCard(QWidget):
    def __init__(self, text, duration=8, position="top-right", theme="light"):
        super().__init__()
        self.duration = duration
        self._closing = False

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self._setup_ui(text, theme)
        self._setup_position(position)
        self._setup_animations(position)

        QTimer.singleShot(duration * 1000, self.hide_card)

    def _setup_ui(self, text, theme):
        is_dark = theme == "dark"

        bg = "#1e1e1e" if is_dark else "#ffffff"
        fg = "#e8dcc8" if is_dark else "#3d2e1e"
        border = "#c9a227"
        hint_color = "#7a6a5a" if is_dark else "#9a8870"

        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 12, 12, 12)

        container = QFrame(self)
        container.setObjectName("notif_container")
        container.setStyleSheet(f"""
            QFrame#notif_container {{
                background-color: {bg};
                border: 1.5px solid {border};
                border-radius: 20px;
            }}
        """)

        shadow_style = f"border: none; background-color: transparent;"

        inner = QVBoxLayout(container)
        inner.setContentsMargins(28, 22, 28, 18)
        inner.setSpacing(10)

        basmala = QLabel("﷽")
        basmala.setAlignment(Qt.AlignmentFlag.AlignCenter)
        basmala.setFont(QFont("Amiri", 22))
        basmala.setStyleSheet(f"color: {border}; background: transparent;")

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {border}40; background-color: {border}25; border: none; max-height: 1px;")

        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setWordWrap(True)
        lbl.setFont(QFont("Amiri", 17, QFont.Weight.Bold))
        lbl.setStyleSheet(f"color: {fg}; background: transparent; line-height: 1.5;")

        hint_row = QHBoxLayout()
        hint_row.setContentsMargins(0, 0, 0, 0)

        dot = QLabel("•")
        dot.setStyleSheet(f"color: {hint_color}; background: transparent; font-size: 10px;")
        hint = QLabel("انقر للإغلاق")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setFont(QFont("Amiri", 10))
        hint.setStyleSheet(f"color: {hint_color}; background: transparent;")
        dot2 = QLabel("•")
        dot2.setStyleSheet(f"color: {hint_color}; background: transparent; font-size: 10px;")

        hint_row.addStretch()
        hint_row.addWidget(dot)
        hint_row.addSpacing(6)
        hint_row.addWidget(hint)
        hint_row.addSpacing(6)
        hint_row.addWidget(dot2)
        hint_row.addStretch()

        inner.addWidget(basmala)
        inner.addWidget(sep)
        inner.addWidget(lbl)
        inner.addLayout(hint_row)

        outer.addWidget(container)
        self.setFixedSize(440, 190)

    def _setup_position(self, position):
        screen = QApplication.primaryScreen().geometry()
        margin = 28
        w, h = self.width(), self.height()
        pos_map = {
            "top-right":    (screen.width() - w - margin, margin),
            "top-left":     (margin, margin),
            "bottom-right": (screen.width() - w - margin, screen.height() - h - margin),
            "bottom-left":  (margin, screen.height() - h - margin),
        }
        x, y = pos_map.get(position, pos_map["top-right"])
        self.end_pos = QPoint(x, y)
        offset = -(h + 60) if "top" in position else (screen.height() + 60)
        self.start_pos = QPoint(x, offset if "top" in position else screen.height() + 60)
        self.move(self.start_pos)

    def _setup_animations(self, position):
        self.op_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.op_effect)
        self.op_effect.setOpacity(0)

        self._in_pos = QPropertyAnimation(self, b"pos")
        self._in_pos.setDuration(650)
        self._in_pos.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._in_pos.setStartValue(self.start_pos)
        self._in_pos.setEndValue(self.end_pos)

        self._in_op = QPropertyAnimation(self.op_effect, b"opacity")
        self._in_op.setDuration(400)
        self._in_op.setStartValue(0.0)
        self._in_op.setEndValue(1.0)

        self._out_pos = QPropertyAnimation(self, b"pos")
        self._out_pos.setDuration(450)
        self._out_pos.setEasingCurve(QEasingCurve.Type.InCubic)
        self._out_pos.setEndValue(self.start_pos)
        self._out_pos.finished.connect(self.close)

        self._out_op = QPropertyAnimation(self.op_effect, b"opacity")
        self._out_op.setDuration(450)
        self._out_op.setEndValue(0.0)

        self._in_group = QParallelAnimationGroup(self)
        self._in_group.addAnimation(self._in_pos)
        self._in_group.addAnimation(self._in_op)

        self._out_group = QParallelAnimationGroup(self)
        self._out_group.addAnimation(self._out_pos)
        self._out_group.addAnimation(self._out_op)

    def showEvent(self, event):
        super().showEvent(event)
        self._in_group.start()

    def hide_card(self):
        if self._closing:
            return
        self._closing = True
        self._in_group.stop()
        self._out_pos.setStartValue(self.pos())
        self._out_op.setStartValue(self.op_effect.opacity())
        self._out_group.start()

    def mousePressEvent(self, event):
        self.hide_card()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    args = sys.argv[1:]
    text = args[0] if args else "سبحان الله وبحمده، سبحان الله العظيم"
    dur = int(args[1]) if len(args) > 1 else 8
    pos = args[2] if len(args) > 2 else "top-right"
    thm = args[3] if len(args) > 3 else "light"
    card = NotificationCard(text, dur, pos, thm)
    card.show()
    sys.exit(app.exec())
