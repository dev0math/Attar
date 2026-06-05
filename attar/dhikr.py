import json
from pathlib import Path

DEFAULT = [
    "سبحان الله وبحمده",
    "سبحان الله العظيم",
    "لا إله إلا الله وحده لا شريك له",
    "اللهم صل على محمد",
    "أستغفر الله العظيم وأتوب إليه",
    "لا حول ولا قوة إلا بالله",
    "سبحان الله والحمد لله ولا إله إلا الله والله أكبر",
    "الحمد لله",
    "الله أكبر",
    "سبحان الله وبحمده سبحان الله العظيم",
    "اللهم اغفر لي ولوالدي",
    "رب اغفر لي وتب علي إنك أنت التواب الرحيم",
    "اللهم إني أسألك علماً نافعاً ورزقاً طيباً وعملاً متقبلاً"
]

class DhikrManager:
    def __init__(self):
        self.file = Path.home() / ".attar" / "dhikr.json"
        self.load()

    def load(self):
        if self.file.exists():
            try:
                data = json.loads(self.file.read_text(encoding='utf-8'))
                self.items = data.get("items", DEFAULT.copy())
            except:
                self.items = DEFAULT.copy()
                self.save()
        else:
            self.items = DEFAULT.copy()
            self.save()

    def save(self):
        self.file.write_text(json.dumps({"items": self.items}, ensure_ascii=False, indent=2), encoding='utf-8')

    def get_all(self):
        return self.items

    def get_active(self):
        config_file = Path.home() / ".attar" / "config.json"
        try:
            cfg = json.loads(config_file.read_text(encoding='utf-8'))
            active = cfg.get("active_dhikr", self.items.copy())
            return [a for a in active if a in self.items]
        except:
            return self.items.copy()

    def set_active(self, active_list):
        config_file = Path.home() / ".attar" / "config.json"
        try:
            cfg = json.loads(config_file.read_text(encoding='utf-8'))
        except:
            cfg = {}
        cfg["active_dhikr"] = active_list
        config_file.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')

    def get_random(self):
        import random
        active = self.get_active()
        if not active:
            active = self.items.copy()
        return random.choice(active)
