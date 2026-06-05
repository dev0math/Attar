import sys
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect, QApplication, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QParallelAnimationGroup
from PyQt6.QtGui import QFont, QFontMetrics

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
        bg      = "#1e1e1e" if is_dark else "#ffffff"
        fg      = "#e8dcc8" if is_dark else "#3d2e1e"
        gold    = "#c9a227"
        hint_fg = "#5a4a38" if is_dark else "#b0a090"
        border  = "#c9a22760" if is_dark else "#c9a22745"

        CARD_W = 460

        outer = QVBoxLayout(self)
        outer.setContentsMargins(10, 10, 10, 10)
        outer.setSpacing(0)

        container = QFrame(self)
        container.setObjectName("notif_container")
        container.setStyleSheet(f"""
            QFrame#notif_container {{
                background-color: {bg};
                border: 1.5px solid {gold};
                border-radius: 22px;
            }}
            QLabel {{ background: transparent; }}
        """)
        container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        container.setFixedWidth(CARD_W - 20)

        inner = QVBoxLayout(container)
        inner.setContentsMargins(24, 18, 24, 14)
        inner.setSpacing(0)

        basmala = QLabel("﷽")
        basmala.setAlignment(Qt.AlignmentFlag.AlignCenter)
        basmala.setFont(QFont("Amiri", 20))
        basmala.setStyleSheet(f"color: {gold};")
        basmala.setFixedHeight(36)
        inner.addWidget(basmala)

        inner.addSpacing(10)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background-color: {gold}35; border: none;")
        inner.addWidget(sep)

        inner.addSpacing(14)

        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setWordWrap(True)
        lbl.setFont(QFont("Amiri", 16, QFont.Weight.Bold))
        lbl.setStyleSheet(f"color: {fg}; line-height: 160%;")
        lbl.setTextFormat(Qt.TextFormat.PlainText)
        lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        lbl.setMinimumHeight(32)
        inner.addWidget(lbl)

        inner.addSpacing(14)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFixedHeight(1)
        sep2.setStyleSheet(f"background-color: {border}; border: none;")
        inner.addWidget(sep2)

        inner.addSpacing(10)

        hint = QLabel("انقر للإغلاق")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setFont(QFont("Amiri", 10))
        hint.setFixedHeight(18)
        hint.setStyleSheet(f"color: {hint_fg};")
        inner.addWidget(hint)

        outer.addWidget(container)

        self.setFixedWidth(CARD_W)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.adjustSize()

    def _setup_position(self, position):
        self.adjustSize()
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

        if "top" in position:
            self.start_pos = QPoint(x, -(h + 60))
        else:
            self.start_pos = QPoint(x, screen.height() + 60)

        self.move(self.start_pos)

    def _setup_animations(self, position):
        self.op_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.op_effect)
        self.op_effect.setOpacity(0)

        self._in_pos = QPropertyAnimation(self, b"pos")
        self._in_pos.setDuration(600)
        self._in_pos.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._in_pos.setStartValue(self.start_pos)
        self._in_pos.setEndValue(self.end_pos)

        self._in_op = QPropertyAnimation(self.op_effect, b"opacity")
        self._in_op.setDuration(380)
        self._in_op.setStartValue(0.0)
        self._in_op.setEndValue(1.0)

        self._out_pos = QPropertyAnimation(self, b"pos")
        self._out_pos.setDuration(420)
        self._out_pos.setEasingCurve(QEasingCurve.Type.InCubic)
        self._out_pos.setEndValue(self.start_pos)
        self._out_pos.finished.connect(self.close)

        self._out_op = QPropertyAnimation(self.op_effect, b"opacity")
        self._out_op.setDuration(420)
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
    text = args[0] if args else "اللهم صل على محمد وعلى آل محمد كما صليت على إبراهيم وعلى آل إبراهيم إنك حميد مجيد"
    dur  = int(args[1]) if len(args) > 1 else 8
    pos  = args[2] if len(args) > 2 else "top-right"
    thm  = args[3] if len(args) > 3 else "light"
    card = NotificationCard(text, dur, pos, thm)
    card.show()
    sys.exit(app.exec())
