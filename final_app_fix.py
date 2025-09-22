#!/usr/bin/env python3
"""
Finale App-Reparatur für deCONZ Migration Tool
Behebt alle Probleme und erstellt eine funktionsfähige App
"""

import os
import sys
import shutil
from pathlib import Path

def final_app_fix():
    """Finale App-Reparatur."""
    print("🔧 Finale App-Reparatur...")
    
    # App-Pfad
    app_path = Path("deCONZ-Migration-Tool.app")
    resources_path = app_path / "Contents" / "Resources"
    
    # Erstelle finalen GUI-Starter
    final_gui_starter = '''#!/usr/bin/env python3
"""
Finaler GUI-Starter für deCONZ Migration Tool
Verwendet System-Python mit installierten Paketen
"""

import sys
import os
from pathlib import Path

# Debug-Informationen
print("🔍 Finale Debug-Informationen:")
print(f"Python-Version: {sys.version}")
print(f"Aktuelles Verzeichnis: {os.getcwd()}")

# Ermittle korrekte Pfade
script_dir = Path(__file__).parent
bin_dir = script_dir / "bin"

print(f"Script-Verzeichnis: {script_dir}")
print(f"Bin-Verzeichnis: {bin_dir}")
print(f"Bin-Verzeichnis existiert: {bin_dir.exists()}")

# Füge bin-Verzeichnis zum Python-Pfad hinzu
if bin_dir.exists():
    sys.path.insert(0, str(bin_dir))
    print(f"✅ Bin-Verzeichnis zum Python-Pfad hinzugefügt: {bin_dir}")
else:
    print("❌ Bin-Verzeichnis nicht gefunden!")

# Prüfe verfügbare Module
print("\\n📦 Verfügbare Module im bin-Verzeichnis:")
if bin_dir.exists():
    for file in bin_dir.glob("*.py"):
        print(f"  - {file.name}")

# Prüfe Python-Abhängigkeiten
print("\\n🔍 Prüfe Python-Abhängigkeiten:")
try:
    import yaml
    print("✅ PyYAML verfügbar")
except ImportError:
    print("❌ PyYAML nicht verfügbar")

try:
    import requests
    print("✅ requests verfügbar")
except ImportError:
    print("❌ requests nicht verfügbar")

try:
    import tkinter
    print("✅ tkinter verfügbar")
except ImportError:
    print("❌ tkinter nicht verfügbar")

def main():
    """Hauptfunktion der App."""
    try:
        print("\\n🚀 Starte GUI...")
        
        # Importiere GUI-Module
        from advanced_gui import AdvancedDeconzMigratorGUI
        import tkinter as tk
        
        print("✅ GUI-Module erfolgreich importiert")
        
        # Erstelle GUI
        root = tk.Tk()
        app = AdvancedDeconzMigratorGUI(root)
        
        print("✅ GUI erstellt")
        
        # Beim Schließen Einstellungen speichern
        def on_closing():
            try:
                app.save_settings()
                print("✅ Einstellungen gespeichert")
            except Exception as e:
                print(f"⚠️ Fehler beim Speichern der Einstellungen: {e}")
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("✅ GUI gestartet - Fenster sollte jetzt sichtbar sein")
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        print("\\n🔍 Verfügbare Module:")
        for module in sys.modules:
            if 'gui' in module.lower() or 'deconz' in module.lower():
                print(f"  - {module}")
        
        # Fallback: Terminal-Version
        print("\\n🔄 Fallback: Starte Terminal-Version...")
        try:
            from final_interactive import main as terminal_main
            terminal_main()
        except ImportError as e2:
            print(f"❌ Terminal-Version auch nicht verfügbar: {e2}")
            sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback: Terminal-Version
        print("\\n🔄 Fallback: Starte Terminal-Version...")
        try:
            from final_interactive import main as terminal_main
            terminal_main()
        except ImportError as e2:
            print(f"❌ Terminal-Version auch nicht verfügbar: {e2}")
            sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    # Schreibe finalen GUI-Starter
    gui_starter_path = resources_path / "final_gui_starter.py"
    with open(gui_starter_path, 'w', encoding='utf-8') as f:
        f.write(final_gui_starter)
    
    # Mache GUI-Starter ausführbar
    os.chmod(gui_starter_path, 0o755)
    
    print("✅ Finaler GUI-Starter erstellt")
    
    # Erstelle finalen Launcher
    final_launcher = '''#!/bin/bash
# Finaler Launcher für deCONZ Migration Tool

cd "$(dirname "$0")/../Resources"

echo "🚀 deCONZ Migration Tool - Finale Version"
echo "========================================"

# Prüfe Python
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python 3 ist nicht installiert.\\n\\nBitte installiere Python 3 von python.org" buttons {"OK"} default button "OK"'
    exit 1
fi

# Prüfe tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    osascript -e 'display dialog "tkinter ist nicht verfügbar.\\n\\nBitte installiere Python mit tkinter-Support." buttons {"OK"} default button "OK"'
    exit 1
fi

# Starte GUI
echo "Starte GUI..."
python3 final_gui_starter.py 2>&1 | tee final_gui.log

echo "Logdatei erstellt: final_gui.log"
'''
    
    final_launcher_path = app_path / "Contents" / "MacOS" / "final_launcher"
    with open(final_launcher_path, 'w', encoding='utf-8') as f:
        f.write(final_launcher)
    
    os.chmod(final_launcher_path, 0o755)
    
    print("✅ Finaler Launcher erstellt")
    
    # Erstelle einfachen Start-Skript
    simple_start = '''#!/bin/bash
# Einfacher Start für deCONZ Migration Tool

cd "$(dirname "$0")/../Resources"

# Verwende System-Python mit virtueller Umgebung
if [ -f "../../venv/bin/python" ]; then
    echo "Verwende virtuelle Umgebung..."
    ../../venv/bin/python final_gui_starter.py
else
    echo "Verwende System-Python..."
    python3 final_gui_starter.py
fi
'''
    
    simple_start_path = app_path / "Contents" / "MacOS" / "simple_start"
    with open(simple_start_path, 'w', encoding='utf-8') as f:
        f.write(simple_start)
    
    os.chmod(simple_start_path, 0o755)
    
    print("✅ Einfacher Start-Skript erstellt")
    
    # Kopiere virtuelle Umgebung in die App
    venv_source = Path("venv")
    venv_dest = resources_path / "venv"
    
    if venv_source.exists():
        print("📦 Kopiere virtuelle Umgebung...")
        if venv_dest.exists():
            shutil.rmtree(venv_dest)
        shutil.copytree(venv_source, venv_dest)
        print("✅ Virtuelle Umgebung kopiert")
    else:
        print("⚠️ Virtuelle Umgebung nicht gefunden")
    
    print("\\n🎉 Finale App-Reparatur abgeschlossen!")
    print("\\n📋 Verfügbare Start-Methoden:")
    print("1. Finaler Launcher: ./deCONZ-Migration-Tool.app/Contents/MacOS/final_launcher")
    print("2. Einfacher Start: ./deCONZ-Migration-Tool.app/Contents/MacOS/simple_start")
    print("3. App öffnen: open deCONZ-Migration-Tool.app")
    
    return True

if __name__ == "__main__":
    final_app_fix()
