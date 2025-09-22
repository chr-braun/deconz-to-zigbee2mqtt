#!/usr/bin/env python3
"""
Installationsroutine für deCONZ zu Zigbee2MQTT Migration Tool
Automatische Einrichtung mit virtueller Umgebung und GUI-Start
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

class Installer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.python_cmd = None
        self.pip_cmd = None
        
    def print_header(self):
        """Zeige Installations-Header."""
        print("=" * 60)
        print("🚀 deCONZ zu Zigbee2MQTT Migration Tool - Installer")
        print("=" * 60)
        print("Dieses Skript richtet das Migration Tool automatisch ein.")
        print("=" * 60)
        
    def check_python(self):
        """Prüfe Python-Version."""
        print("\n🐍 Prüfe Python-Version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"❌ Python {version.major}.{version.minor} gefunden.")
            print("   Mindestens Python 3.8 erforderlich!")
            return False
            
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} gefunden")
        return True
        
    def check_tkinter(self):
        """Prüfe tkinter-Installation."""
        print("\n🖥️ Prüfe tkinter...")
        
        try:
            import tkinter
            print("✅ tkinter verfügbar")
            return True
        except ImportError:
            print("⚠️ tkinter nicht verfügbar")
            print("   GUI-Features werden nicht funktionieren")
            print("   Terminal-Tools sind weiterhin verfügbar")
            print("   Fortfahren ohne tkinter...")
            return True  # Fortfahren ohne tkinter
            
    def install_tkinter(self):
        """Installiere tkinter."""
        system = platform.system().lower()
        
        try:
            if system == "darwin":  # macOS
                print("   macOS erkannt - installiere tkinter über Homebrew...")
                subprocess.run(["brew", "install", "python-tk"], check=True)
            elif system == "linux":
                print("   Linux erkannt - installiere python3-tk...")
                subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"], check=True)
            elif system == "windows":
                print("   Windows erkannt - tkinter sollte bereits installiert sein")
                print("   Falls nicht, installiere Python mit tkinter-Support")
            else:
                print(f"   Unbekanntes System: {system}")
                print("   Bitte installiere tkinter manuell")
                return False
                
            # Teste erneut
            import tkinter
            print("✅ tkinter erfolgreich installiert")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Fehler bei tkinter-Installation: {e}")
            print("   Bitte installiere tkinter manuell")
            return False
        except ImportError:
            print("❌ tkinter nach Installation immer noch nicht verfügbar")
            return False
            
    def create_virtual_environment(self):
        """Erstelle virtuelle Umgebung."""
        print("\n📦 Erstelle virtuelle Umgebung...")
        
        if self.venv_path.exists():
            print("   Virtuelle Umgebung existiert bereits - lösche...")
            shutil.rmtree(self.venv_path)
            
        try:
            # Verwende python3 statt sys.executable für bessere Kompatibilität
            python_cmd = "python3" if shutil.which("python3") else sys.executable
            subprocess.run([python_cmd, "-m", "venv", str(self.venv_path)], check=True)
            print("✅ Virtuelle Umgebung erstellt")
            
            # Setze Python- und Pip-Pfade
            if platform.system().lower() == "windows":
                self.python_cmd = str(self.venv_path / "Scripts" / "python.exe")
                self.pip_cmd = str(self.venv_path / "Scripts" / "pip.exe")
            else:
                self.python_cmd = str(self.venv_path / "bin" / "python")
                self.pip_cmd = str(self.venv_path / "bin" / "pip")
                
            # Prüfe ob die Pfade existieren
            if not Path(self.python_cmd).exists():
                print(f"⚠️ Python-Pfad nicht gefunden: {self.python_cmd}")
                print("   Verwende System-Python...")
                self.python_cmd = python_cmd
                self.pip_cmd = "pip3" if shutil.which("pip3") else "pip"
                
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Fehler beim Erstellen der virtuellen Umgebung: {e}")
            print("   Verwende System-Python...")
            self.python_cmd = "python3" if shutil.which("python3") else sys.executable
            self.pip_cmd = "pip3" if shutil.which("pip3") else "pip"
            return True
            
    def install_requirements(self):
        """Installiere Python-Abhängigkeiten."""
        print("\n📚 Installiere Abhängigkeiten...")
        
        try:
            # Upgrade pip
            subprocess.run([self.pip_cmd, "install", "--upgrade", "pip"], check=True)
            
            # Installiere requirements
            subprocess.run([self.pip_cmd, "install", "-r", "requirements.txt"], check=True)
            
            print("✅ Abhängigkeiten installiert")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Fehler beim Installieren der Abhängigkeiten: {e}")
            return False
            
    def create_directory_structure(self):
        """Erstelle Verzeichnisstruktur."""
        print("\n📁 Erstelle Verzeichnisstruktur...")
        
        # Hauptverzeichnisse
        dirs = [
            "bin",           # Ausführbare Dateien
            "config",        # Konfigurationsdateien
            "docs",          # Dokumentation
            "examples",      # Beispiel-Konfigurationen
            "logs",          # Log-Dateien
            "temp"           # Temporäre Dateien
        ]
        
        for dir_name in dirs:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(exist_ok=True)
            print(f"   📁 {dir_name}/")
            
        print("✅ Verzeichnisstruktur erstellt")
        return True
        
    def organize_files(self):
        """Organisiere Dateien in Verzeichnisse."""
        print("\n🗂️ Organisiere Dateien...")
        
        # Datei-Kategorien
        file_categories = {
            "bin": [
                "advanced_gui.py",
                "gui_migrate.py", 
                "final_interactive.py",
                "interactive_with_key.py",
                "quick_migrate.py",
                "simple_api_key.py",
                "test_api.py"
            ],
            "config": [
                "requirements.txt",
                "configuration.yaml"
            ],
            "docs": [
                "README.md",
                "deconz_research.md",
                "migration_success.md",
                "gui_features.md"
            ],
            "examples": [
                "migrate_now.py",
                "demo_interactive.py"
            ]
        }
        
        # Verschiebe Dateien
        for category, files in file_categories.items():
            target_dir = self.project_root / category
            for file_name in files:
                source_path = self.project_root / file_name
                if source_path.exists():
                    target_path = target_dir / file_name
                    shutil.move(str(source_path), str(target_path))
                    print(f"   📄 {file_name} → {category}/")
                    
        print("✅ Dateien organisiert")
        return True
        
    def create_launcher_scripts(self):
        """Erstelle Start-Skripte."""
        print("\n🚀 Erstelle Start-Skripte...")
        
        # Haupt-GUI Launcher
        gui_launcher = self.project_root / "start_gui.py"
        with open(gui_launcher, 'w', encoding='utf-8') as f:
            f.write('''#!/usr/bin/env python3
"""
GUI Launcher für deCONZ zu Zigbee2MQTT Migration Tool
"""

import sys
import os
from pathlib import Path

# Füge bin-Verzeichnis zum Python-Pfad hinzu
project_root = Path(__file__).parent
bin_path = project_root / "bin"
sys.path.insert(0, str(bin_path))

# Starte GUI
if __name__ == "__main__":
    try:
        from advanced_gui import main
        main()
    except ImportError:
        print("❌ GUI konnte nicht gestartet werden")
        print("Führe 'python3 install.py' aus, um das Tool zu installieren")
        sys.exit(1)
''')
        
        # Terminal Launcher
        terminal_launcher = self.project_root / "start_terminal.py"
        with open(terminal_launcher, 'w', encoding='utf-8') as f:
            f.write('''#!/usr/bin/env python3
"""
Terminal Launcher für deCONZ zu Zigbee2MQTT Migration Tool
"""

import sys
import os
from pathlib import Path

# Füge bin-Verzeichnis zum Python-Pfad hinzu
project_root = Path(__file__).parent
bin_path = project_root / "bin"
sys.path.insert(0, str(bin_path))

# Starte Terminal-Tool
if __name__ == "__main__":
    try:
        from final_interactive import main
        main()
    except ImportError:
        print("❌ Terminal-Tool konnte nicht gestartet werden")
        print("Führe 'python3 install.py' aus, um das Tool zu installieren")
        sys.exit(1)
''')
        
        # Machen Sie die Skripte ausführbar
        for script in [gui_launcher, terminal_launcher]:
            os.chmod(script, 0o755)
            
        print("✅ Start-Skripte erstellt")
        return True
        
    def create_requirements_file(self):
        """Erstelle erweiterte requirements.txt."""
        print("\n📋 Erstelle requirements.txt...")
        
        requirements = """# deCONZ to Zigbee2MQTT Migration Tool Dependencies
# Core dependencies
pyyaml>=6.0,<7.0
requests>=2.25.0,<3.0.0

# GUI dependencies (optional)
# tkinter is usually included with Python

# Development dependencies (optional)
# pytest>=6.0.0
# black>=21.0.0
# flake8>=3.8.0
"""
        
        with open(self.project_root / "requirements.txt", 'w') as f:
            f.write(requirements)
            
        print("✅ requirements.txt erstellt")
        return True
        
    def create_readme(self):
        """Erstelle aktualisierte README."""
        print("\n📖 Erstelle README...")
        
        readme_content = """# 🚀 deCONZ zu Zigbee2MQTT Migration Tool

> **Vollständig installiert!** Migration Tool für deCONZ-Geräte nach Zigbee2MQTT

## 🚀 Schnellstart

### Installation
```bash
# Automatische Installation
python3 install.py

# Oder manuell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Verwendung
```bash
# GUI starten (empfohlen)
python3 start_gui.py

# Terminal starten
python3 start_terminal.py
```

## 📁 Verzeichnisstruktur

```
deconz-to-zigbee2mqtt/
├── bin/                    # Ausführbare Tools
│   ├── advanced_gui.py    # Haupt-GUI
│   ├── gui_migrate.py     # Basis-GUI
│   ├── final_interactive.py
│   └── ...
├── config/                 # Konfigurationsdateien
│   ├── requirements.txt
│   └── configuration.yaml
├── docs/                   # Dokumentation
│   ├── README.md
│   ├── gui_features.md
│   └── ...
├── examples/               # Beispiel-Skripte
├── logs/                   # Log-Dateien
├── temp/                   # Temporäre Dateien
├── venv/                   # Virtuelle Umgebung
├── start_gui.py           # GUI-Starter
├── start_terminal.py      # Terminal-Starter
└── install.py             # Installationsskript
```

## 🛠️ Tools

### GUI-Tools
- `python3 start_gui.py` - Erweiterte GUI
- `python3 bin/gui_migrate.py` - Basis-GUI

### Terminal-Tools
- `python3 start_terminal.py` - Interaktives Terminal-Tool
- `python3 bin/final_interactive.py` - Direktes Terminal-Tool

## ✅ Erfolgreich getestet

- **deCONZ-Server**: 192.168.178.76:4530
- **Geräte migriert**: 86 (69 Sensoren + 17 Lichter)
- **Konfiguration**: Vollständige `configuration.yaml` generiert
- **GUI**: Moderne grafische Benutzeroberfläche

## 🎯 Features

- **🖥️ GUI**: Moderne grafische Benutzeroberfläche
- **💻 Terminal**: Interaktive Terminal-Version
- **🔑 API-Key**: Automatische Generierung mit Link-Button
- **📊 Geräte**: 86 Geräte (69 Sensoren + 17 Lichter)
- **⚙️ Konfiguration**: Vollständige Zigbee2MQTT-Konfiguration
- **📋 Logging**: Detailliertes Log mit Zeitstempel

## 🚀 Nächste Schritte

1. **Zigbee2MQTT installieren**
2. **Konfiguration kopieren**: `config/configuration.yaml` → Zigbee2MQTT
3. **Zigbee2MQTT starten** mit neuer Konfiguration
4. **Geräte prüfen** in der Zigbee2MQTT-Oberfläche

---

**Migration erfolgreich abgeschlossen!** 🎉
"""
        
        with open(self.project_root / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        print("✅ README erstellt")
        return True
        
    def test_installation(self):
        """Teste Installation."""
        print("\n🧪 Teste Installation...")
        
        try:
            # Teste mit virtuellem Python
            test_script = f"""
import sys
sys.path.insert(0, '{self.project_root / "bin"}')
try:
    from final_interactive import main as terminal_main
    print("✅ Terminal-Import erfolgreich")
except ImportError as e:
    print(f"❌ Terminal-Import fehlgeschlagen: {{e}}")
    sys.exit(1)

try:
    from advanced_gui import AdvancedDeconzMigratorGUI
    print("✅ GUI-Import erfolgreich")
except ImportError:
    print("⚠️ GUI-Import fehlgeschlagen (tkinter-Problem)")
    print("   Terminal-Tools sind verfügbar")

print("✅ Installation erfolgreich getestet")
"""
            
            # Führe Test mit virtuellem Python aus
            result = subprocess.run([self.python_cmd, "-c", test_script], 
                                  capture_output=True, text=True, cwd=str(self.project_root))
            
            if result.returncode == 0:
                print(result.stdout)
                return True
            else:
                print(f"❌ Test fehlgeschlagen: {result.stderr}")
                return False
            
        except Exception as e:
            print(f"❌ Test-Fehler: {e}")
            return False
            
    def cleanup_old_files(self):
        """Räume alte Dateien auf."""
        print("\n🧹 Räume auf...")
        
        # Dateien die nicht mehr benötigt werden
        old_files = [
            "deconz_to_z2m.py",
            "migrate_now.py",
            "get_api_key.py"
        ]
        
        for file_name in old_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                file_path.unlink()
                print(f"   🗑️ {file_name} gelöscht")
                
        print("✅ Aufräumung abgeschlossen")
        return True
        
    def run(self):
        """Führe Installation aus."""
        self.print_header()
        
        # Installation-Schritte
        steps = [
            ("Python-Version prüfen", self.check_python),
            ("tkinter prüfen", self.check_tkinter),
            ("Virtuelle Umgebung erstellen", self.create_virtual_environment),
            ("Abhängigkeiten installieren", self.install_requirements),
            ("Verzeichnisstruktur erstellen", self.create_directory_structure),
            ("Dateien organisieren", self.organize_files),
            ("Start-Skripte erstellen", self.create_launcher_scripts),
            ("requirements.txt erstellen", self.create_requirements_file),
            ("README erstellen", self.create_readme),
            ("Installation testen", self.test_installation),
            ("Aufräumen", self.cleanup_old_files)
        ]
        
        # Führe Schritte aus
        for step_name, step_func in steps:
            print(f"\n{'='*20} {step_name} {'='*20}")
            if not step_func():
                print(f"\n❌ Installation fehlgeschlagen bei: {step_name}")
                return False
                
        # Erfolg
        print("\n" + "="*60)
        print("🎉 INSTALLATION ERFOLGREICH ABGESCHLOSSEN!")
        print("="*60)
        print("\n📋 Nächste Schritte:")
        print("1. GUI starten: python3 start_gui.py")
        print("2. Terminal starten: python3 start_terminal.py")
        print("3. Dokumentation lesen: docs/README.md")
        print("\n🚀 Viel Erfolg mit deinem Migration Tool!")
        
        return True

def main():
    """Hauptfunktion."""
    installer = Installer()
    success = installer.run()
    
    if success:
        print("\n🎯 Möchtest du die GUI jetzt starten? (j/n): ", end="")
        try:
            response = input().lower().strip()
            if response in ['j', 'ja', 'y', 'yes']:
                print("\n🚀 Starte GUI...")
                subprocess.run([sys.executable, "start_gui.py"])
        except KeyboardInterrupt:
            print("\n👋 Installation beendet")
    else:
        print("\n❌ Installation fehlgeschlagen!")
        sys.exit(1)

if __name__ == "__main__":
    main()
