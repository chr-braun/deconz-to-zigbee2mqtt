#!/usr/bin/env python3
"""
App-Fix für deCONZ Migration Tool
Behebt das Problem mit der nicht-interaktiven Ausführung
"""

import os
import sys
import shutil
from pathlib import Path

def fix_app():
    """Behebe App-Probleme."""
    print("🔧 Behebe App-Probleme...")
    
    # App-Pfad
    app_path = Path("deCONZ-Migration-Tool.app")
    resources_path = app_path / "Contents" / "Resources"
    
    # Erstelle verbesserten Launcher
    launcher_script = '''#!/bin/bash
# deCONZ Migration Tool Launcher - Verbessert

# Ermittle App-Verzeichnis
APP_DIR="$(dirname "$0")"
APP_ROOT="$(dirname "$APP_DIR")"
RESOURCES_DIR="$APP_DIR/../Resources"

# Wechsle zum App-Verzeichnis
cd "$RESOURCES_DIR"

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

# Starte GUI direkt
echo "Starte deCONZ Migration Tool GUI..."
python3 -c "
import sys
sys.path.insert(0, 'bin')
try:
    from advanced_gui import AdvancedDeconzMigratorGUI
    import tkinter as tk
    
    root = tk.Tk()
    app = AdvancedDeconzMigratorGUI(root)
    
    def on_closing():
        try:
            app.save_settings()
        except:
            pass
        root.destroy()
    
    root.protocol('WM_DELETE_WINDOW', on_closing)
    root.mainloop()
    
except ImportError as e:
    print(f'GUI-Fehler: {e}')
    osascript -e 'display dialog \"GUI konnte nicht gestartet werden.\\n\\nFehler: ' + str(e) + '\" buttons {\"OK\"} default button \"OK\"'
    exit 1
except Exception as e:
    print(f'Unerwarteter Fehler: {e}')
    osascript -e 'display dialog \"Unerwarteter Fehler: ' + str(e) + '\" buttons {\"OK\"} default button \"OK\"'
    exit 1
"
'''
    
    # Schreibe verbesserten Launcher
    launcher_path = app_path / "Contents" / "MacOS" / "launcher"
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_script)
    
    # Mache Launcher ausführbar
    os.chmod(launcher_path, 0o755)
    
    print("✅ Launcher verbessert")
    
    # Erstelle GUI-Starter-Skript
    gui_starter = '''#!/usr/bin/env python3
"""
GUI-Starter für deCONZ Migration Tool
"""

import sys
import os
from pathlib import Path

# Füge bin-Verzeichnis zum Python-Pfad hinzu
if getattr(sys, 'frozen', False):
    # PyInstaller-Bundle
    app_dir = Path(sys._MEIPASS)
    bin_dir = app_dir / "bin"
else:
    # Normale Ausführung
    app_dir = Path(__file__).parent
    bin_dir = app_dir / "bin"

sys.path.insert(0, str(bin_dir))

def main():
    """Hauptfunktion der App."""
    try:
        # Starte GUI
        from advanced_gui import AdvancedDeconzMigratorGUI
        import tkinter as tk
        
        root = tk.Tk()
        app = AdvancedDeconzMigratorGUI(root)
        
        # Beim Schließen Einstellungen speichern
        def on_closing():
            try:
                app.save_settings()
            except:
                pass
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except ImportError as e:
        print(f"GUI nicht verfügbar: {e}")
        # Zeige Fehlermeldung
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Fehler", f"GUI konnte nicht gestartet werden:\\n{e}")
            root.destroy()
        except:
            print(f"Fehler: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
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
    
    # Schreibe GUI-Starter
    gui_starter_path = resources_path / "gui_starter.py"
    with open(gui_starter_path, 'w', encoding='utf-8') as f:
        f.write(gui_starter)
    
    # Mache GUI-Starter ausführbar
    os.chmod(gui_starter_path, 0o755)
    
    print("✅ GUI-Starter erstellt")
    
    # Erstelle einfachen Test-Launcher
    test_launcher = '''#!/bin/bash
# Test-Launcher für deCONZ Migration Tool

cd "$(dirname "$0")/../Resources"

echo "Teste deCONZ Migration Tool..."
python3 gui_starter.py
'''
    
    test_launcher_path = app_path / "Contents" / "MacOS" / "test_launcher"
    with open(test_launcher_path, 'w', encoding='utf-8') as f:
        f.write(test_launcher)
    
    os.chmod(test_launcher_path, 0o755)
    
    print("✅ Test-Launcher erstellt")
    
    print("\n🎉 App-Reparatur abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print("1. Teste die App: open deCONZ-Migration-Tool.app")
    print("2. Falls Probleme: ./deCONZ-Migration-Tool.app/Contents/MacOS/test_launcher")
    
    return True

if __name__ == "__main__":
    fix_app()
