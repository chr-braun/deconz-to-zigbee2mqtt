#!/usr/bin/env python3
"""
App-Pfad-Fix für deCONZ Migration Tool
Behebt das Problem mit den Modul-Pfaden
"""

import os
import sys
import shutil
from pathlib import Path

def fix_app_paths():
    """Behebe App-Pfad-Probleme."""
    print("🔧 Behebe App-Pfad-Probleme...")
    
    # App-Pfad
    app_path = Path("deCONZ-Migration-Tool.app")
    resources_path = app_path / "Contents" / "Resources"
    
    # Erstelle verbesserten GUI-Starter mit korrekten Pfaden
    gui_starter = '''#!/usr/bin/env python3
"""
GUI-Starter für deCONZ Migration Tool - Mit korrekten Pfaden
"""

import sys
import os
from pathlib import Path

# Debug-Informationen
print("🔍 Debug-Informationen:")
print(f"Python-Version: {sys.version}")
print(f"Aktuelles Verzeichnis: {os.getcwd()}")
print(f"Python-Pfad: {sys.path}")

# Ermittle korrekte Pfade
if getattr(sys, 'frozen', False):
    # PyInstaller-Bundle
    app_dir = Path(sys._MEIPASS)
    bin_dir = app_dir / "bin"
    print(f"PyInstaller-Modus: {app_dir}")
else:
    # Normale Ausführung
    script_dir = Path(__file__).parent
    bin_dir = script_dir / "bin"
    print(f"Normale Ausführung: {script_dir}")

print(f"Bin-Verzeichnis: {bin_dir}")
print(f"Bin-Verzeichnis existiert: {bin_dir.exists()}")

# Füge bin-Verzeichnis zum Python-Pfad hinzu
if bin_dir.exists():
    sys.path.insert(0, str(bin_dir))
    print(f"Bin-Verzeichnis zum Python-Pfad hinzugefügt: {bin_dir}")
else:
    print("❌ Bin-Verzeichnis nicht gefunden!")

# Liste verfügbare Module
print("\\n📦 Verfügbare Module im bin-Verzeichnis:")
if bin_dir.exists():
    for file in bin_dir.glob("*.py"):
        print(f"  - {file.name}")

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
        
        # Zeige Fehlermeldung
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Import-Fehler", f"GUI konnte nicht gestartet werden:\\n{e}\\n\\nBitte prüfe die Logdatei für Details.")
            root.destroy()
        except:
            print(f"Fehler: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Fehler", f"Unerwarteter Fehler: {e}")
            root.destroy()
        except:
            print(f"Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    # Schreibe verbesserten GUI-Starter
    gui_starter_path = resources_path / "gui_starter.py"
    with open(gui_starter_path, 'w', encoding='utf-8') as f:
        f.write(gui_starter)
    
    # Mache GUI-Starter ausführbar
    os.chmod(gui_starter_path, 0o755)
    
    print("✅ GUI-Starter mit Debug-Informationen erstellt")
    
    # Erstelle verbesserten Test-Launcher
    test_launcher = '''#!/bin/bash
# Test-Launcher für deCONZ Migration Tool - Mit Logging

cd "$(dirname "$0")/../Resources"

echo "🔍 Debug-Informationen:"
echo "Aktuelles Verzeichnis: $(pwd)"
echo "Python-Version: $(python3 --version)"
echo "Verfügbare Python-Module:"
python3 -c "import sys; print('\\n'.join(sys.path))"

echo ""
echo "📁 Verzeichnis-Inhalt:"
ls -la

echo ""
echo "📁 Bin-Verzeichnis:"
ls -la bin/

echo ""
echo "🚀 Starte GUI mit Debug-Informationen..."
python3 gui_starter.py 2>&1 | tee gui_debug.log

echo ""
echo "📋 Logdatei erstellt: gui_debug.log"
'''
    
    test_launcher_path = app_path / "Contents" / "MacOS" / "test_launcher"
    with open(test_launcher_path, 'w', encoding='utf-8') as f:
        f.write(test_launcher)
    
    os.chmod(test_launcher_path, 0o755)
    
    print("✅ Test-Launcher mit Debug-Informationen erstellt")
    
    # Erstelle Log-Verzeichnis
    logs_dir = resources_path / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    print("✅ Log-Verzeichnis erstellt")
    
    print("\\n🎉 App-Pfad-Reparatur abgeschlossen!")
    print("\\n📋 Nächste Schritte:")
    print("1. Teste die App: ./deCONZ-Migration-Tool.app/Contents/MacOS/test_launcher")
    print("2. Prüfe Logdateien: cat deCONZ-Migration-Tool.app/Contents/Resources/gui_debug.log")
    
    return True

if __name__ == "__main__":
    fix_app_paths()
