#!/usr/bin/env python3
"""
macOS App Creator mit detailliertem Logging
Erstellt eine .app-Bundle und generiert umfassende Logdateien
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

class MacAppCreatorWithLogs:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.app_name = "deCONZ-Migration-Tool"
        self.app_bundle = self.project_root / f"{self.app_name}.app"
        self.log_file = self.project_root / "app_creation.log"
        
    def log(self, message):
        """Füge Nachricht zum Log hinzu."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message)
        
        print(message)
        
    def print_header(self):
        """Zeige App-Erstellungs-Header."""
        print("=" * 60)
        print("🍎 macOS App Creator mit Logging")
        print("=" * 60)
        print("Erstellt eine .app-Bundle mit detailliertem Logging")
        print("=" * 60)
        
    def create_app_structure(self):
        """Erstelle App-Bundle-Struktur."""
        self.log("📁 Erstelle App-Bundle-Struktur...")
        
        # Lösche alte App
        if self.app_bundle.exists():
            shutil.rmtree(self.app_bundle)
            self.log("   Alte App gelöscht")
        
        # Erstelle App-Bundle-Verzeichnisse
        contents_dir = self.app_bundle / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        for dir_path in [contents_dir, macos_dir, resources_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            self.log(f"   📁 {dir_path.relative_to(self.project_root)}/")
            
        self.log("✅ App-Bundle-Struktur erstellt")
        return True
        
    def create_info_plist(self):
        """Erstelle Info.plist."""
        self.log("📋 Erstelle Info.plist...")
        
        info_plist = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>{self.app_name}</string>
    <key>CFBundleDisplayName</key>
    <string>deCONZ Migration Tool</string>
    <key>CFBundleIdentifier</key>
    <string>com.deconz.migration.tool</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>10.13.0</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
    <key>NSAppleScriptEnabled</key>
    <false/>
</dict>
</plist>
'''
        
        plist_path = self.app_bundle / "Contents" / "Info.plist"
        with open(plist_path, 'w', encoding='utf-8') as f:
            f.write(info_plist)
            
        self.log("✅ Info.plist erstellt")
        return True
        
    def create_launcher_script(self):
        """Erstelle Launcher-Skript mit Logging."""
        self.log("🚀 Erstelle Launcher-Skript...")
        
        launcher_script = '''#!/bin/bash
# deCONZ Migration Tool Launcher mit Logging

# Log-Verzeichnis
LOG_DIR="$(dirname "$0")/../Resources/logs"
mkdir -p "$LOG_DIR"

# Log-Datei
LOG_FILE="$LOG_DIR/app_launcher.log"

# Funktion zum Loggen
log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🚀 deCONZ Migration Tool Launcher gestartet"
log "Aktuelles Verzeichnis: $(pwd)"
log "App-Verzeichnis: $(dirname "$0")"

# Ermittle App-Verzeichnis
APP_DIR="$(dirname "$0")"
APP_ROOT="$(dirname "$APP_DIR")"
RESOURCES_DIR="$APP_DIR/../Resources"

# Wechsle zum App-Verzeichnis
cd "$RESOURCES_DIR"
log "Wechsle zu: $(pwd)"

# Prüfe Python
if ! command -v python3 &> /dev/null; then
    log "❌ Python 3 nicht gefunden"
    osascript -e 'display dialog "Python 3 ist nicht installiert.\\n\\nBitte installiere Python 3 von python.org" buttons {"OK"} default button "OK"'
    exit 1
fi

log "✅ Python 3 gefunden: $(python3 --version)"

# Prüfe tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    log "❌ tkinter nicht verfügbar"
    osascript -e 'display dialog "tkinter ist nicht verfügbar.\\n\\nBitte installiere Python mit tkinter-Support." buttons {"OK"} default button "OK"'
    exit 1
fi

log "✅ tkinter verfügbar"

# Starte GUI mit Logging
log "🚀 Starte GUI..."
python3 gui_launcher.py 2>&1 | tee -a "$LOG_DIR/gui.log"

log "📋 GUI beendet"
'''
        
        launcher_path = self.app_bundle / "Contents" / "MacOS" / "launcher"
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_script)
        
        # Mache Launcher ausführbar
        os.chmod(launcher_path, 0o755)
        
        self.log("✅ Launcher-Skript erstellt")
        return True
        
    def create_gui_launcher(self):
        """Erstelle GUI-Launcher mit Logging."""
        self.log("🖥️ Erstelle GUI-Launcher...")
        
        gui_launcher = '''#!/usr/bin/env python3
"""
GUI-Launcher für deCONZ Migration Tool mit detailliertem Logging
"""

import sys
import os
import logging
from pathlib import Path
from datetime import datetime

# Logging-Setup
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f"gui_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Hauptfunktion der App."""
    logger.info("🚀 GUI-Launcher gestartet")
    logger.info(f"Python-Version: {sys.version}")
    logger.info(f"Aktuelles Verzeichnis: {os.getcwd()}")
    
    # Ermittle korrekte Pfade
    script_dir = Path(__file__).parent
    bin_dir = script_dir / "bin"
    
    logger.info(f"Script-Verzeichnis: {script_dir}")
    logger.info(f"Bin-Verzeichnis: {bin_dir}")
    logger.info(f"Bin-Verzeichnis existiert: {bin_dir.exists()}")
    
    # Füge bin-Verzeichnis zum Python-Pfad hinzu
    if bin_dir.exists():
        sys.path.insert(0, str(bin_dir))
        logger.info(f"✅ Bin-Verzeichnis zum Python-Pfad hinzugefügt: {bin_dir}")
    else:
        logger.error("❌ Bin-Verzeichnis nicht gefunden!")
        return False
    
    # Prüfe verfügbare Module
    logger.info("📦 Verfügbare Module im bin-Verzeichnis:")
    if bin_dir.exists():
        for file in bin_dir.glob("*.py"):
            logger.info(f"  - {file.name}")
    
    # Prüfe Python-Abhängigkeiten
    logger.info("🔍 Prüfe Python-Abhängigkeiten:")
    dependencies = ['yaml', 'requests', 'tkinter']
    
    for dep in dependencies:
        try:
            __import__(dep)
            logger.info(f"✅ {dep} verfügbar")
        except ImportError:
            logger.error(f"❌ {dep} nicht verfügbar")
    
    try:
        logger.info("🚀 Starte GUI...")
        
        # Importiere GUI-Module
        from advanced_gui import AdvancedDeconzMigratorGUI
        import tkinter as tk
        
        logger.info("✅ GUI-Module erfolgreich importiert")
        
        # Erstelle GUI
        root = tk.Tk()
        app = AdvancedDeconzMigratorGUI(root)
        
        logger.info("✅ GUI erstellt")
        
        # Beim Schließen Einstellungen speichern
        def on_closing():
            try:
                app.save_settings()
                logger.info("✅ Einstellungen gespeichert")
            except Exception as e:
                logger.error(f"⚠️ Fehler beim Speichern der Einstellungen: {e}")
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        logger.info("✅ GUI gestartet - Fenster sollte jetzt sichtbar sein")
        root.mainloop()
        
    except ImportError as e:
        logger.error(f"❌ Import-Fehler: {e}")
        logger.info("🔍 Verfügbare Module:")
        for module in sys.modules:
            if 'gui' in module.lower() or 'deconz' in module.lower():
                logger.info(f"  - {module}")
        
        # Fallback: Terminal-Version
        logger.info("🔄 Fallback: Starte Terminal-Version...")
        try:
            from final_interactive import main as terminal_main
            terminal_main()
        except ImportError as e2:
            logger.error(f"❌ Terminal-Version auch nicht verfügbar: {e2}")
            return False
        
    except Exception as e:
        logger.error(f"❌ Unerwarteter Fehler: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Fallback: Terminal-Version
        logger.info("🔄 Fallback: Starte Terminal-Version...")
        try:
            from final_interactive import main as terminal_main
            terminal_main()
        except ImportError as e2:
            logger.error(f"❌ Terminal-Version auch nicht verfügbar: {e2}")
            return False

if __name__ == "__main__":
    main()
'''
        
        gui_launcher_path = self.app_bundle / "Contents" / "Resources" / "gui_launcher.py"
        with open(gui_launcher_path, 'w', encoding='utf-8') as f:
            f.write(gui_launcher)
        
        # Mache GUI-Launcher ausführbar
        os.chmod(gui_launcher_path, 0o755)
        
        self.log("✅ GUI-Launcher erstellt")
        return True
        
    def copy_resources(self):
        """Kopiere Ressourcen in die App."""
        self.log("📦 Kopiere Ressourcen...")
        
        resources_dir = self.app_bundle / "Contents" / "Resources"
        
        # Kopiere alle Projektdateien
        files_to_copy = [
            "start_gui.py",
            "start_terminal.py", 
            "start_terminal_only.py",
            "requirements.txt",
            "README.md",
            "INSTALLATION_SUCCESS.md"
        ]
        
        for file_name in files_to_copy:
            source_path = self.project_root / file_name
            if source_path.exists():
                shutil.copy2(source_path, resources_dir)
                self.log(f"   📄 {file_name}")
        
        # Kopiere Verzeichnisse
        dirs_to_copy = ["bin", "config", "docs", "examples", "temp"]
        
        for dir_name in dirs_to_copy:
            source_dir = self.project_root / dir_name
            if source_dir.exists():
                dest_dir = resources_dir / dir_name
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
                self.log(f"   📁 {dir_name}/")
        
        # Kopiere virtuelle Umgebung
        venv_source = self.project_root / "venv"
        venv_dest = resources_dir / "venv"
        
        if venv_source.exists():
            self.log("📦 Kopiere virtuelle Umgebung...")
            if venv_dest.exists():
                shutil.rmtree(venv_dest)
            shutil.copytree(venv_source, venv_dest)
            self.log("✅ Virtuelle Umgebung kopiert")
        
        self.log("✅ Ressourcen kopiert")
        return True
        
    def run(self):
        """Führe App-Erstellung aus."""
        self.print_header()
        
        # Lösche alte Logdatei
        if self.log_file.exists():
            self.log_file.unlink()
        
        # App-Erstellungs-Schritte
        steps = [
            ("App-Bundle-Struktur erstellen", self.create_app_structure),
            ("Info.plist erstellen", self.create_info_plist),
            ("Launcher-Skript erstellen", self.create_launcher_script),
            ("GUI-Launcher erstellen", self.create_gui_launcher),
            ("Ressourcen kopieren", self.copy_resources)
        ]
        
        # Führe Schritte aus
        for step_name, step_func in steps:
            self.log(f"\\n{'='*20} {step_name} {'='*20}")
            if not step_func():
                self.log(f"\\n❌ App-Erstellung fehlgeschlagen bei: {step_name}")
                return False
                
        # Erfolg
        self.log("\\n" + "="*60)
        self.log("🎉 macOS APP ERFOLGREICH ERSTELLT!")
        self.log("="*60)
        self.log(f"\\n📱 App: {self.app_bundle}")
        self.log(f"📦 Größe: {self.get_app_size()}")
        self.log("\\n🚀 Die App kann jetzt gestartet werden:")
        self.log(f"   open '{self.app_bundle}'")
        self.log("\\n📋 Logdateien:")
        self.log(f"   - {self.log_file}")
        self.log(f"   - {self.app_bundle}/Contents/Resources/logs/")
        
        return True
        
    def get_app_size(self):
        """Ermittle App-Größe."""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(self.app_bundle):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            
            # Konvertiere zu MB
            size_mb = total_size / (1024 * 1024)
            return f"{size_mb:.1f} MB"
        except:
            return "Unbekannt"

def main():
    """Hauptfunktion."""
    creator = MacAppCreatorWithLogs()
    success = creator.run()
    
    if success:
        print("\\n🎯 Möchtest du die App jetzt starten? (j/n): ", end="")
        try:
            response = input().lower().strip()
            if response in ['j', 'ja', 'y', 'yes']:
                print("\\n🚀 Starte App...")
                subprocess.run(["open", str(creator.app_bundle)])
        except KeyboardInterrupt:
            print("\\n👋 App-Erstellung beendet")
    else:
        print("\\n❌ App-Erstellung fehlgeschlagen!")
        sys.exit(1)

if __name__ == "__main__":
    main()
