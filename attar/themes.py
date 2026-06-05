LIGHT_THEME = """
QWidget {
    font-family: 'Amiri', 'Noto Sans Arabic', 'Segoe UI', sans-serif;
    font-size: 14px;
    color: #3d2e1e;
    background-color: #faf7f0;
}
QMainWindow {
    background-color: #faf7f0;
}
QTabWidget::pane {
    border: 1px solid #e0d5be;
    border-radius: 12px;
    background-color: #ffffff;
    padding: 16px;
    margin-top: -1px;
}
QTabWidget QWidget {
    background-color: transparent;
}
QTabBar::tab {
    background-color: #f2ece0;
    color: #6b5740;
    padding: 13px 30px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 3px;
    font-size: 15px;
    border: 1px solid #e0d5be;
    border-bottom: none;
}
QTabBar::tab:selected {
    background-color: #c9a227;
    color: #ffffff;
    font-weight: bold;
    border-color: #c9a227;
}
QTabBar::tab:hover:!selected {
    background-color: #e8ddc8;
    color: #4a3520;
}
QPushButton {
    background-color: #c9a227;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 11px 28px;
    font-weight: bold;
    font-size: 14px;
    letter-spacing: 0.3px;
}
QPushButton:hover {
    background-color: #b8941f;
}
QPushButton:pressed {
    background-color: #9e7d18;
}
QPushButton:disabled {
    background-color: #ddd5c0;
    color: #a09080;
}
QPushButton#danger {
    background-color: #b83228;
    color: #ffffff;
}
QPushButton#danger:hover {
    background-color: #a22820;
}
QPushButton#danger:pressed {
    background-color: #8a1f18;
}
QPushButton#danger:disabled {
    background-color: #e8dcc8;
    color: #a09080;
}
QPushButton#secondary {
    background-color: #ede5d4;
    color: #4a3520;
    border: 1px solid #d4c9b0;
}
QPushButton#secondary:hover {
    background-color: #dfd4be;
}
QPushButton#secondary:pressed {
    background-color: #d0c5ae;
}
QPushButton#iconBtn {
    background-color: transparent;
    color: #c9a227;
    font-size: 16px;
    border: 1.5px solid #c9a227;
    border-radius: 22px;
    padding: 0px;
    min-width: 44px;
    max-width: 44px;
    min-height: 44px;
    max-height: 44px;
    font-weight: bold;
}
QPushButton#iconBtn:hover {
    background-color: #c9a227;
    color: #fff;
}
QPushButton#iconBtn:pressed {
    background-color: #b8941f;
    color: #fff;
}
QPushButton#closeBtn {
    background-color: transparent;
    color: #b83228;
    font-size: 16px;
    border: 1.5px solid #b83228;
    border-radius: 22px;
    padding: 0px;
    min-width: 44px;
    max-width: 44px;
    min-height: 44px;
    max-height: 44px;
    font-weight: bold;
}
QPushButton#closeBtn:hover {
    background-color: #b83228;
    color: #fff;
}
QLineEdit, QSpinBox, QComboBox {
    border: 2px solid #ddd5c0;
    border-radius: 8px;
    padding: 9px 12px;
    background-color: #ffffff;
    color: #3d2e1e;
    font-size: 14px;
    selection-background-color: #c9a227;
    selection-color: #ffffff;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border-color: #c9a227;
    background-color: #fffdf7;
}
QLineEdit:hover, QSpinBox:hover, QComboBox:hover {
    border-color: #c9a22780;
}
QSpinBox::up-button, QSpinBox::down-button {
    border: none;
    padding: 2px;
    background-color: transparent;
}
QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}
QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #ddd5c0;
    border-radius: 8px;
    selection-background-color: #c9a227;
    selection-color: #ffffff;
    padding: 4px;
    outline: none;
}
QListWidget {
    border: 2px solid #ddd5c0;
    border-radius: 10px;
    background-color: #ffffff;
    padding: 6px;
    outline: none;
    font-size: 15px;
}
QListWidget::item {
    padding: 13px 16px;
    border-radius: 6px;
    margin: 2px 0;
    border-bottom: 1px solid #f0ebe0;
}
QListWidget::item:last-child {
    border-bottom: none;
}
QListWidget::item:selected {
    background-color: #c9a227;
    color: #ffffff;
    border-radius: 6px;
    border-bottom: none;
}
QListWidget::item:hover:!selected {
    background-color: #f5f0e5;
}
QScrollBar:vertical {
    background-color: #f0ebe0;
    width: 8px;
    border-radius: 4px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background-color: #c9a22760;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #c9a227;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
QLabel#title {
    font-size: 26px;
    font-weight: bold;
    color: #c9a227;
    letter-spacing: 0.5px;
}
QLabel#subtitle {
    font-size: 14px;
    color: #9a8870;
}
QLabel#stat {
    font-size: 36px;
    font-weight: bold;
    color: #c9a227;
}
QLabel#statLabel {
    font-size: 12px;
    color: #9a8870;
    letter-spacing: 0.3px;
}
QLabel#countLabel {
    font-size: 20px;
    font-weight: bold;
    color: #c9a227;
}
QFrame#card {
    background-color: #ffffff;
    border: 1px solid #e8ddc8;
    border-radius: 16px;
}
QFrame#card:hover {
    border-color: #c9a22780;
    background-color: #fffdf8;
}
QCheckBox {
    spacing: 10px;
    font-size: 14px;
    color: #3d2e1e;
}
QCheckBox::indicator {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid #ddd5c0;
    background-color: #ffffff;
}
QCheckBox::indicator:hover {
    border-color: #c9a227;
}
QCheckBox::indicator:checked {
    background-color: #c9a227;
    border-color: #c9a227;
    image: none;
}
QCheckBox::indicator:checked:hover {
    background-color: #b8941f;
}
QSlider::groove:horizontal {
    height: 6px;
    background: #e8ddc8;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    width: 22px;
    height: 22px;
    background: #c9a227;
    border-radius: 11px;
    margin: -8px 0;
    border: 2px solid #ffffff;
}
QSlider::handle:horizontal:hover {
    background: #b8941f;
    width: 24px;
    height: 24px;
    border-radius: 12px;
    margin: -9px 0;
}
QSlider::sub-page:horizontal {
    background: #c9a227;
    border-radius: 3px;
}
QGroupBox {
    color: #3d2e1e;
    border: 1px solid #e0d5be;
    border-radius: 10px;
    margin-top: 14px;
    padding-top: 22px;
    padding-left: 12px;
    padding-right: 12px;
    padding-bottom: 12px;
    font-weight: bold;
    font-size: 14px;
    background-color: #fdfaf4;
}
QGroupBox::title {
    color: #c9a227;
    subcontrol-origin: margin;
    subcontrol-position: top right;
    padding: 0 8px;
    right: 16px;
}
QToolTip {
    background-color: #3d2e1e;
    color: #faf7f0;
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
}
"""

DARK_THEME = """
QWidget {
    font-family: 'Amiri', 'Noto Sans Arabic', 'Segoe UI', sans-serif;
    font-size: 14px;
    color: #e8dcc8;
    background-color: #141414;
}
QMainWindow {
    background-color: #141414;
}
QTabWidget::pane {
    border: 1px solid #2e2e2e;
    border-radius: 12px;
    background-color: #1e1e1e;
    padding: 16px;
    margin-top: -1px;
}
QTabWidget QWidget {
    background-color: transparent;
}
QTabBar::tab {
    background-color: #1e1e1e;
    color: #9a8870;
    padding: 13px 30px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 3px;
    font-size: 15px;
    border: 1px solid #2e2e2e;
    border-bottom: none;
}
QTabBar::tab:selected {
    background-color: #c9a227;
    color: #141414;
    font-weight: bold;
    border-color: #c9a227;
}
QTabBar::tab:hover:!selected {
    background-color: #2a2a2a;
    color: #e8dcc8;
}
QPushButton {
    background-color: #c9a227;
    color: #141414;
    border: none;
    border-radius: 10px;
    padding: 11px 28px;
    font-weight: bold;
    font-size: 14px;
    letter-spacing: 0.3px;
}
QPushButton:hover {
    background-color: #d4b43a;
}
QPushButton:pressed {
    background-color: #b8941f;
}
QPushButton:disabled {
    background-color: #2a2a2a;
    color: #5a4a38;
}
QPushButton#danger {
    background-color: #b83228;
    color: #ffffff;
}
QPushButton#danger:hover {
    background-color: #d04030;
}
QPushButton#danger:pressed {
    background-color: #9e2820;
}
QPushButton#danger:disabled {
    background-color: #2a2a2a;
    color: #5a4a38;
}
QPushButton#secondary {
    background-color: #2a2a2a;
    color: #e8dcc8;
    border: 1px solid #3a3a3a;
}
QPushButton#secondary:hover {
    background-color: #343434;
}
QPushButton#secondary:pressed {
    background-color: #3e3e3e;
}
QPushButton#iconBtn {
    background-color: transparent;
    color: #c9a227;
    font-size: 16px;
    border: 1.5px solid #c9a22780;
    border-radius: 22px;
    padding: 0px;
    min-width: 44px;
    max-width: 44px;
    min-height: 44px;
    max-height: 44px;
    font-weight: bold;
}
QPushButton#iconBtn:hover {
    background-color: #c9a22720;
    border-color: #c9a227;
    color: #c9a227;
}
QPushButton#iconBtn:pressed {
    background-color: #c9a22740;
}
QPushButton#closeBtn {
    background-color: transparent;
    color: #e05040;
    font-size: 16px;
    border: 1.5px solid #e0504080;
    border-radius: 22px;
    padding: 0px;
    min-width: 44px;
    max-width: 44px;
    min-height: 44px;
    max-height: 44px;
    font-weight: bold;
}
QPushButton#closeBtn:hover {
    background-color: #e0504020;
    border-color: #e05040;
}
QLineEdit, QSpinBox, QComboBox {
    border: 2px solid #2e2e2e;
    border-radius: 8px;
    padding: 9px 12px;
    background-color: #1e1e1e;
    color: #e8dcc8;
    font-size: 14px;
    selection-background-color: #c9a227;
    selection-color: #141414;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border-color: #c9a227;
    background-color: #222218;
}
QLineEdit:hover, QSpinBox:hover, QComboBox:hover {
    border-color: #c9a22760;
}
QSpinBox::up-button, QSpinBox::down-button {
    border: none;
    padding: 2px;
    background-color: transparent;
}
QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}
QComboBox QAbstractItemView {
    background-color: #1e1e1e;
    border: 1px solid #2e2e2e;
    border-radius: 8px;
    selection-background-color: #c9a227;
    selection-color: #141414;
    padding: 4px;
    outline: none;
}
QListWidget {
    border: 2px solid #2e2e2e;
    border-radius: 10px;
    background-color: #1e1e1e;
    padding: 6px;
    outline: none;
    font-size: 15px;
}
QListWidget::item {
    padding: 13px 16px;
    border-radius: 6px;
    margin: 2px 0;
    border-bottom: 1px solid #2a2a2a;
}
QListWidget::item:last-child {
    border-bottom: none;
}
QListWidget::item:selected {
    background-color: #c9a227;
    color: #141414;
    border-radius: 6px;
    border-bottom: none;
}
QListWidget::item:hover:!selected {
    background-color: #252525;
}
QScrollBar:vertical {
    background-color: #1e1e1e;
    width: 8px;
    border-radius: 4px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background-color: #c9a22740;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #c9a227;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
QLabel#title {
    font-size: 26px;
    font-weight: bold;
    color: #c9a227;
    letter-spacing: 0.5px;
}
QLabel#subtitle {
    font-size: 14px;
    color: #7a6a5a;
}
QLabel#stat {
    font-size: 36px;
    font-weight: bold;
    color: #c9a227;
}
QLabel#statLabel {
    font-size: 12px;
    color: #7a6a5a;
    letter-spacing: 0.3px;
}
QLabel#countLabel {
    font-size: 20px;
    font-weight: bold;
    color: #c9a227;
}
QFrame#card {
    background-color: #1e1e1e;
    border: 1px solid #2e2e2e;
    border-radius: 16px;
}
QFrame#card:hover {
    border-color: #c9a22760;
    background-color: #222218;
}
QCheckBox {
    spacing: 10px;
    font-size: 14px;
    color: #e8dcc8;
}
QCheckBox::indicator {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid #3a3a3a;
    background-color: #1e1e1e;
}
QCheckBox::indicator:hover {
    border-color: #c9a22780;
}
QCheckBox::indicator:checked {
    background-color: #c9a227;
    border-color: #c9a227;
}
QCheckBox::indicator:checked:hover {
    background-color: #d4b43a;
}
QSlider::groove:horizontal {
    height: 6px;
    background: #2a2a2a;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    width: 22px;
    height: 22px;
    background: #c9a227;
    border-radius: 11px;
    margin: -8px 0;
    border: 2px solid #141414;
}
QSlider::handle:horizontal:hover {
    background: #d4b43a;
    width: 24px;
    height: 24px;
    border-radius: 12px;
    margin: -9px 0;
}
QSlider::sub-page:horizontal {
    background: #c9a22780;
    border-radius: 3px;
}
QGroupBox {
    color: #e8dcc8;
    border: 1px solid #2e2e2e;
    border-radius: 10px;
    margin-top: 14px;
    padding-top: 22px;
    padding-left: 12px;
    padding-right: 12px;
    padding-bottom: 12px;
    font-weight: bold;
    font-size: 14px;
    background-color: #191919;
}
QGroupBox::title {
    color: #c9a227;
    subcontrol-origin: margin;
    subcontrol-position: top right;
    padding: 0 8px;
    right: 16px;
}
QToolTip {
    background-color: #e8dcc8;
    color: #141414;
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
}
"""
