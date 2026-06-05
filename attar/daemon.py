import sys, os, time, json, signal, subprocess
from pathlib import Path
from PyQt6.QtCore import QCoreApplication, QTimer

class Daemon:
    def __init__(self):
        self.app = QCoreApplication(sys.argv)
        self.cfg = Path.home() / ".attar" / "config.json"
        self.dhikr_file = Path.home() / ".attar" / "dhikr.json"
        self.stats = Path.home() / ".attar" / "stats.json"
        self.last = Path.home() / ".attar" / ".last_dhikr"
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(10000)
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def read_cfg(self):
        try:
            return json.loads(self.cfg.read_text(encoding='utf-8'))
        except:
            return {"enabled":True,"interval":15,"duration":8,"position":"top-right","theme":"light"}

    def get_dhikr(self):
        try:
            items = json.loads(self.dhikr_file.read_text(encoding='utf-8')).get("items",[])
            active = self.read_cfg().get("active_dhikr", items)
            valid = [a for a in active if a in items]
            if valid:
                import random
                return random.choice(valid)
        except:
            pass
        return "سبحان الله"

    def tick(self):
        c = self.read_cfg()
        if not c.get("enabled",True):
            return
        interval = c.get("interval",15)
        now = time.time()
        last = 0
        if self.last.exists():
            try:
                last = float(self.last.read_text())
            except:
                pass
        if now - last >= interval*60:
            d = self.get_dhikr()
            dur = c.get("duration",8)
            pos = c.get("position","top-right")
            thm = c.get("theme","light")
            st = {}
            if self.stats.exists():
                try:
                    st = json.loads(self.stats.read_text())
                except:
                    pass
            today = time.strftime("%Y-%m-%d")
            st[today] = st.get(today,0)+1
            self.stats.write_text(json.dumps(st,ensure_ascii=False,indent=2),encoding='utf-8')
            notifier = Path(__file__).parent / "notifier.py"
            subprocess.Popen([sys.executable,str(notifier),d,str(dur),pos,thm],
                             stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            self.last.write_text(str(now))

    def shutdown(self,*a):
        self.app.quit()

    def run(self):
        self.app.exec()

if __name__ == "__main__":
    Daemon().run()
