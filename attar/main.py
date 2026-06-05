import sys, os, argparse, signal, subprocess
from pathlib import Path
from .config import Config
from .dhikr import DhikrManager

def get_pid_file():
    return Path.home() / ".attar" / "daemon.pid"

def is_running():
    pid_file = get_pid_file()
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, 0)
            return True
        except:
            pass
    return False

def start_daemon():
    if is_running():
        print("الديمون يعمل بالفعل.")
        return
    Config().set("enabled", True)
    daemon_path = Path(__file__).parent / "daemon.py"
    proc = subprocess.Popen([sys.executable, str(daemon_path)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    get_pid_file().write_text(str(proc.pid))
    print("تم تشغيل الديمون.")

def stop_daemon():
    pid_file = get_pid_file()
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, signal.SIGTERM)
        except:
            pass
        pid_file.unlink(missing_ok=True)
    Config().set("enabled", False)
    print("تم إيقاف الديمون.")

def show_status():
    if is_running():
        pid = get_pid_file().read_text().strip()
        print(f"الديمون يعمل (PID: {pid})")
    else:
        print("الديمون متوقف.")

def show_version():
    print("Attar 3.0.0")

def open_gui():
    from PyQt6.QtWidgets import QApplication
    from .gui import AttarGUI
    app = QApplication(sys.argv)
    win = AttarGUI()
    win.show()
    sys.exit(app.exec())

def main():
    parser = argparse.ArgumentParser(prog="attar", description="Attar - تذكير إسلامي")
    parser.add_argument("--start", action="store_true", help="تشغيل الديمون")
    parser.add_argument("--stop", action="store_true", help="إيقاف الديمون")
    parser.add_argument("--status", action="store_true", help="حالة الديمون")
    parser.add_argument("--gui", action="store_true", help="فتح لوحة التحكم")
    parser.add_argument("--version", action="store_true", help="إصدار البرنامج")
    parser.add_argument("--uninstall", action="store_true", help="إلغاء التثبيت")
    args = parser.parse_args()

    if args.start:
        start_daemon()
    elif args.stop:
        stop_daemon()
    elif args.status:
        show_status()
    elif args.gui:
        open_gui()
    elif args.version:
        show_version()
    elif args.uninstall:
        uninstall_path = Path.home() / ".attar" / "uninstall.sh"
        if uninstall_path.exists():
            subprocess.run(["bash", str(uninstall_path)])
        else:
            print("سكربت إلغاء التثبيت غير موجود.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
