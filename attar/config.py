import json
from pathlib import Path

class Config:
    def __init__(self):
        self.dir = Path.home() / ".attar"
        self.file = self.dir / "config.json"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.defaults = {
            "enabled": True,
            "autostart": False,
            "style": "default",
            "duration": 8,
            "position": "top-right",
            "interval": 15,
            "font_size": 14,
            "theme": "light",
            "active_dhikr": []
        }
        self.load()

    def load(self):
        if self.file.exists():
            try:
                self.data = json.loads(self.file.read_text(encoding='utf-8'))
            except:
                self.data = {}
        else:
            self.data = {}
        for k, v in self.defaults.items():
            if k not in self.data:
                self.data[k] = v
        self.save()

    def save(self):
        self.file.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding='utf-8')

    def get(self, key, default=None):
        if default is not None:
            return self.data.get(key, default)
        return self.data.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.data[key] = value
        self.save()
