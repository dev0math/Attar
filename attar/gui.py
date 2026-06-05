import sys, json, os, subprocess, signal
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from .config import Config
from .dhikr import DhikrManager
from .themes import LIGHT_THEME, DARK_THEME
from .notifier import NotificationCard


class StatCard(QFrame):
    def __init__(self, value, label, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setFixedSize(210, 125)

        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(4)
        lay.setContentsMargins(16, 16, 16, 16)

        self.value_label = QLabel(str(value))
        self.value_label.setObjectName("stat")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.desc_label = QLabel(label)
        self.desc_label.setObjectName("statLabel")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lay.addWidget(self.value_label)
        lay.addWidget(self.desc_label)

    def set_value(self, val):
        self.value_label.setText(str(val))


class ControlTab(QWidget):
    def __init__(self, config, dhikr, parent=None):
        super().__init__(parent)
        self.config = config
        self.dhikr = dhikr

        lay = QVBoxLayout(self)
        lay.setSpacing(20)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay.setContentsMargins(20, 20, 20, 20)

        title = QLabel("لوحة التحكم")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)

        subtitle = QLabel("تحكم في التذكير وتابع إحصائياتك")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(subtitle)

        lay.addSpacing(8)

        cards_lay = QHBoxLayout()
        cards_lay.setSpacing(14)
        cards_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_card = StatCard("متوقف", "الحالة")
        self.today_card = StatCard("0", "اليوم")
        self.total_card = StatCard("0", "الإجمالي")
        self.daily_card = StatCard("0", "تقدير اليوم")

        for card in (self.status_card, self.today_card, self.total_card, self.daily_card):
            cards_lay.addWidget(card)
        lay.addLayout(cards_lay)

        lay.addSpacing(4)

        btn_lay = QHBoxLayout()
        btn_lay.setSpacing(12)

        self.start_btn = QPushButton("تشغيل")
        self.start_btn.setObjectName("secondary")
        self.start_btn.setMinimumWidth(130)
        self.start_btn.setMinimumHeight(44)
        self.start_btn.clicked.connect(self.start_daemon)

        self.stop_btn = QPushButton("إيقاف")
        self.stop_btn.setObjectName("danger")
        self.stop_btn.setMinimumWidth(130)
        self.stop_btn.setMinimumHeight(44)
        self.stop_btn.clicked.connect(self.stop_daemon)

        self.test_btn = QPushButton("معاينة إشعار")
        self.test_btn.setObjectName("secondary")
        self.test_btn.setMinimumWidth(130)
        self.test_btn.setMinimumHeight(44)
        self.test_btn.clicked.connect(self.test_notify)

        btn_lay.addStretch()
        btn_lay.addWidget(self.start_btn)
        btn_lay.addWidget(self.stop_btn)
        btn_lay.addWidget(self.test_btn)
        btn_lay.addStretch()
        lay.addLayout(btn_lay)

        inter_group = QGroupBox("إعدادات التذكير")
        inter_lay = QVBoxLayout(inter_group)
        inter_lay.setSpacing(18)
        inter_lay.setContentsMargins(16, 24, 16, 16)

        slider_row = QHBoxLayout()
        slider_row.setSpacing(12)
        slider_row.addWidget(QLabel("الفترة بين كل تذكير:"))

        self.interval_label = QLabel("")
        self.interval_label.setObjectName("countLabel")
        self.interval_label.setMinimumWidth(90)
        self.interval_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        slider_row.addWidget(self.interval_label)

        self.interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.interval_slider.setRange(1, 120)
        self.interval_slider.setValue(config.get("interval"))
        self.interval_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.interval_slider.setTickInterval(15)
        self.interval_slider.valueChanged.connect(self.on_interval_change)
        slider_row.addWidget(self.interval_slider)
        inter_lay.addLayout(slider_row)

        count_row = QHBoxLayout()
        count_row.addWidget(QLabel("عدد التذكيرات المتوقع يومياً:"))
        self.count_label = QLabel("0")
        self.count_label.setObjectName("countLabel")
        count_row.addWidget(self.count_label)
        count_row.addStretch()
        inter_lay.addLayout(count_row)

        lay.addWidget(inter_group)
        lay.addStretch()

        self.refresh_stats()
        self.refresh_status()
        self.on_interval_change(self.interval_slider.value())

    def on_interval_change(self, v):
        self.config.set("interval", v)
        if v < 60:
            self.interval_label.setText(f"{v} دقيقة")
        elif v == 60:
            self.interval_label.setText("ساعة كاملة")
        else:
            hours = v / 60
            self.interval_label.setText(f"{hours:.1f} ساعة")

        count = 1440 // v if v > 0 else 0
        self.count_label.setText(str(count))
        self.daily_card.set_value(count)

    def refresh_status(self):
        pid_file = Path.home() / ".attar" / "daemon.pid"
        running = False
        if pid_file.exists():
            try:
                os.kill(int(pid_file.read_text().strip()), 0)
                running = True
            except Exception:
                pass
        self.status_card.set_value("يعمل" if running else "متوقف")
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)

    def refresh_stats(self):
        stats_file = Path.home() / ".attar" / "stats.json"
        today = QDate.currentDate().toString("yyyy-MM-dd")
        today_count, total = 0, 0
        if stats_file.exists():
            try:
                data = json.loads(stats_file.read_text())
                today_count = data.get(today, 0)
                total = sum(data.values())
            except Exception:
                pass
        self.today_card.set_value(today_count)
        self.total_card.set_value(total)
        self.daily_card.set_value(1440 // max(self.config.get("interval"), 1))

    def start_daemon(self):
        self.config.set("enabled", True)
        daemon_path = Path(__file__).parent / "daemon.py"
        proc = subprocess.Popen(
            [sys.executable, str(daemon_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        (Path.home() / ".attar" / "daemon.pid").write_text(str(proc.pid))
        QTimer.singleShot(600, self.refresh_status)

    def stop_daemon(self):
        self.config.set("enabled", False)
        pid_file = Path.home() / ".attar" / "daemon.pid"
        if pid_file.exists():
            try:
                os.kill(int(pid_file.read_text().strip()), signal.SIGTERM)
            except Exception:
                pass
            pid_file.unlink(missing_ok=True)
        QTimer.singleShot(600, self.refresh_status)

    def test_notify(self):
        dhikr_list = self.dhikr.get_active()
        text = dhikr_list[0] if dhikr_list else "سبحان الله وبحمده"
        card = NotificationCard(
            text,
            self.config.get("duration"),
            self.config.get("position"),
            self.config.get("theme")
        )
        card.show()


class DhikrTab(QWidget):
    def __init__(self, dhikr, config, parent=None):
        super().__init__(parent)
        self.dhikr = dhikr
        self.config = config

        lay = QVBoxLayout(self)
        lay.setSpacing(14)
        lay.setContentsMargins(20, 20, 20, 20)

        title = QLabel("الأذكار")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)

        subtitle = QLabel("اختر الأذكار التي تريد ظهورها في التذكيرات")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(subtitle)

        toolbar = QHBoxLayout()
        select_all_btn = QPushButton("تحديد الكل")
        select_all_btn.setObjectName("secondary")
        select_all_btn.setMaximumWidth(130)
        select_all_btn.setMinimumHeight(36)
        select_all_btn.clicked.connect(self.select_all)

        deselect_btn = QPushButton("إلغاء الكل")
        deselect_btn.setObjectName("secondary")
        deselect_btn.setMaximumWidth(130)
        deselect_btn.setMinimumHeight(36)
        deselect_btn.clicked.connect(self.deselect_all)

        toolbar.addStretch()
        toolbar.addWidget(select_all_btn)
        toolbar.addWidget(deselect_btn)
        lay.addLayout(toolbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll_widget = QWidget()
        self.scroll_lay = QVBoxLayout(scroll_widget)
        self.scroll_lay.setSpacing(6)
        self.scroll_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_lay.setContentsMargins(4, 4, 4, 4)
        scroll.setWidget(scroll_widget)
        lay.addWidget(scroll)

        self.checkboxes = []
        self.load_dhikr_list()

        info = QLabel("يجب تحديد ذكر واحد على الأقل")
        info.setObjectName("subtitle")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(info)

    def load_dhikr_list(self):
        for cb in self.checkboxes:
            self.scroll_lay.removeWidget(cb)
            cb.deleteLater()
        self.checkboxes.clear()

        all_dhikr = self.dhikr.get_all()
        active = self.config.get("active_dhikr") or all_dhikr.copy()

        for item in all_dhikr:
            cb = QCheckBox(item)
            cb.setChecked(item in active)
            cb.stateChanged.connect(self.on_checkbox_changed)
            self.checkboxes.append(cb)
            self.scroll_lay.addWidget(cb)

    def select_all(self):
        for cb in self.checkboxes:
            cb.blockSignals(True)
            cb.setChecked(True)
            cb.blockSignals(False)
        self.on_checkbox_changed()

    def deselect_all(self):
        for i, cb in enumerate(self.checkboxes):
            cb.blockSignals(True)
            cb.setChecked(i == 0)
            cb.blockSignals(False)
        self.on_checkbox_changed()

    def on_checkbox_changed(self):
        active = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        if not active:
            sender = self.sender()
            if isinstance(sender, QCheckBox):
                sender.blockSignals(True)
                sender.setChecked(True)
                sender.blockSignals(False)
                active = [sender.text()]
            elif self.checkboxes:
                self.checkboxes[0].blockSignals(True)
                self.checkboxes[0].setChecked(True)
                self.checkboxes[0].blockSignals(False)
                active = [self.checkboxes[0].text()]
        self.config.set("active_dhikr", active)
        self.dhikr.set_active(active)


class AppearanceTab(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config

        lay = QVBoxLayout(self)
        lay.setSpacing(20)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay.setContentsMargins(20, 20, 20, 20)

        title = QLabel("المظهر")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)

        theme_group = QGroupBox("وضع الألوان")
        theme_lay = QVBoxLayout(theme_group)
        theme_lay.setContentsMargins(16, 24, 16, 16)

        row = QHBoxLayout()
        row.addWidget(QLabel("الوضع:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["نهاري (فاتح)", "ليلي (داكن)"])
        self.theme_combo.setCurrentIndex(0 if config.get("theme") == "light" else 1)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.theme_combo.setMinimumWidth(180)
        row.addWidget(self.theme_combo)
        row.addStretch()
        theme_lay.addLayout(row)
        lay.addWidget(theme_group)

        preview_btn = QPushButton("معاينة الإشعار")
        preview_btn.setMinimumWidth(200)
        preview_btn.setMinimumHeight(44)
        preview_btn.clicked.connect(self.preview)
        lay.addWidget(preview_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        lay.addStretch()

    def change_theme(self, idx):
        theme = "light" if idx == 0 else "dark"
        self.config.set("theme", theme)
        win = self.window()
        if hasattr(win, "apply_theme"):
            win.apply_theme()

    def preview(self):
        card = NotificationCard(
            "سبحان الله وبحمده، سبحان الله العظيم",
            6,
            "top-right",
            self.config.get("theme")
        )
        card.show()


class SettingsTab(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config

        lay = QVBoxLayout(self)
        lay.setSpacing(20)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay.setContentsMargins(20, 20, 20, 20)

        title = QLabel("الإعدادات")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)

        auto_group = QGroupBox("بدء التشغيل")
        auto_lay = QVBoxLayout(auto_group)
        auto_lay.setContentsMargins(16, 24, 16, 16)

        self.auto_check = QCheckBox("تشغيل عطر تلقائياً مع بدء النظام")
        self.auto_check.setChecked(config.get("autostart"))
        self.auto_check.stateChanged.connect(
            lambda: config.set("autostart", self.auto_check.isChecked())
        )
        auto_lay.addWidget(self.auto_check)
        lay.addWidget(auto_group)

        notif_group = QGroupBox("إعدادات الإشعار")
        notif_lay = QVBoxLayout(notif_group)
        notif_lay.setSpacing(16)
        notif_lay.setContentsMargins(16, 24, 16, 16)

        dur_row = QHBoxLayout()
        dur_row.addWidget(QLabel("مدة ظهور الإشعار:"))
        self.dur_spin = QSpinBox()
        self.dur_spin.setRange(3, 60)
        self.dur_spin.setValue(config.get("duration"))
        self.dur_spin.setSuffix(" ثانية")
        self.dur_spin.setMinimumWidth(120)
        self.dur_spin.valueChanged.connect(lambda v: config.set("duration", v))
        dur_row.addWidget(self.dur_spin)
        dur_row.addStretch()
        notif_lay.addLayout(dur_row)

        pos_row = QHBoxLayout()
        pos_row.addWidget(QLabel("موقع الإشعار على الشاشة:"))
        self.pos_combo = QComboBox()
        self.pos_combo.addItems(["أعلى اليمين", "أعلى اليسار", "أسفل اليمين", "أسفل اليسار"])
        positions = ["top-right", "top-left", "bottom-right", "bottom-left"]
        current_pos = config.get("position")
        if current_pos in positions:
            self.pos_combo.setCurrentIndex(positions.index(current_pos))
        self.pos_combo.setMinimumWidth(180)
        self.pos_combo.currentIndexChanged.connect(
            lambda i: config.set("position", positions[i])
        )
        pos_row.addWidget(self.pos_combo)
        pos_row.addStretch()
        notif_lay.addLayout(pos_row)

        lay.addWidget(notif_group)
        lay.addStretch()


class AttarGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.dhikr = DhikrManager()

        self.setWindowTitle("عطر — Attar")
        self.setMinimumSize(980, 760)

        icon_path = Path(__file__).parent / "assets" / "icon.svg"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(72)
        hlay = QHBoxLayout(header)
        hlay.setContentsMargins(28, 0, 20, 0)
        hlay.setSpacing(12)

        logo = QLabel("عطر")
        logo.setFont(QFont("Amiri", 30, QFont.Weight.Bold))
        logo.setStyleSheet("color: #c9a227; background: transparent;")

        tagline = QLabel("مذكّر الأذكار")
        tagline.setFont(QFont("Amiri", 12))
        tagline.setStyleSheet("color: #9a8870; background: transparent; padding-top: 10px;")

        hlay.addWidget(logo)
        hlay.addWidget(tagline)
        hlay.addStretch()

        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("iconBtn")
        self.theme_btn.setToolTip("تبديل الوضع")
        self.theme_btn.clicked.connect(self.toggle_theme)
        hlay.addWidget(self.theme_btn)

        root.addWidget(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("headerSep")
        root.addWidget(sep)

        self.tabs = QTabWidget()
        self.tabs.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.tabs.setContentsMargins(0, 0, 0, 0)

        self.control_tab = ControlTab(self.config, self.dhikr)
        self.dhikr_tab = DhikrTab(self.dhikr, self.config)
        self.appearance_tab = AppearanceTab(self.config)
        self.settings_tab = SettingsTab(self.config)

        self.tabs.addTab(self.control_tab, "التحكم")
        self.tabs.addTab(self.dhikr_tab, "الأذكار")
        self.tabs.addTab(self.appearance_tab, "المظهر")
        self.tabs.addTab(self.settings_tab, "الإعدادات")

        root.addWidget(self.tabs)
        self.apply_theme()

    def apply_theme(self):
        theme = self.config.get("theme")

        if theme == "dark":
            self.setStyleSheet(DARK_THEME)
            self.theme_btn.setText("◑")
            self.theme_btn.setToolTip("التبديل إلى الوضع النهاري")
        else:
            self.setStyleSheet(LIGHT_THEME)
            self.theme_btn.setText("◐")
            self.theme_btn.setToolTip("التبديل إلى الوضع الليلي")

        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if isinstance(tab, AppearanceTab):
                tab.theme_combo.blockSignals(True)
                tab.theme_combo.setCurrentIndex(0 if theme == "light" else 1)
                tab.theme_combo.blockSignals(False)

    def toggle_theme(self):
        current = self.config.get("theme")
        self.config.set("theme", "dark" if current == "light" else "light")
        self.apply_theme()
