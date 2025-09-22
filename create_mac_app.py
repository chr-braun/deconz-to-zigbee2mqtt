#!/usr/bin/env python3
"""
macOS App Creator für deCONZ zu Zigbee2MQTT Migration Tool
Erstellt eine native .app-Anwendung mit PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class MacAppCreator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.app_name = "deCONZ-Migration-Tool"
        self.app_version = "1.0.0"
        self.app_bundle = self.project_root / f"{self.app_name}.app"
        
    def print_header(self):
        """Zeige App-Erstellungs-Header."""
        print("=" * 60)
        print("🍎 macOS App Creator - deCONZ Migration Tool")
        print("=" * 60)
        print("Erstellt eine native macOS .app-Anwendung")
        print("=" * 60)
        
    def check_pyinstaller(self):
        """Prüfe PyInstaller-Installation."""
        print("\n🔍 Prüfe PyInstaller...")
        
        try:
            import PyInstaller
            print("✅ PyInstaller verfügbar")
            return True
        except ImportError:
            print("❌ PyInstaller nicht verfügbar")
            print("   Installiere PyInstaller...")
            return self.install_pyinstaller()
            
    def install_pyinstaller(self):
        """Installiere PyInstaller."""
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✅ PyInstaller installiert")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Fehler bei PyInstaller-Installation: {e}")
            return False
            
    def create_app_script(self):
        """Erstelle Haupt-App-Skript."""
        print("\n📝 Erstelle App-Skript...")
        
        app_script = self.project_root / "app_main.py"
        
        script_content = '''#!/usr/bin/env python3
"""
deCONZ zu Zigbee2MQTT Migration Tool - macOS App
Hauptskript für die .app-Anwendung
"""

import sys
import os
import tkinter as tk
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
        # Versuche GUI zu starten
        from advanced_gui import AdvancedDeconzMigratorGUI
        
        root = tk.Tk()
        app = AdvancedDeconzMigratorGUI(root)
        
        # Beim Schließen Einstellungen speichern
        def on_closing():
            app.save_settings()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except ImportError as e:
        # Fallback: Terminal-Version
        print(f"GUI nicht verfügbar: {e}")
        print("Starte Terminal-Version...")
        
        try:
            from final_interactive import main as terminal_main
            terminal_main()
        except ImportError as e2:
            print(f"Terminal-Version nicht verfügbar: {e2}")
            print("App kann nicht gestartet werden.")
            input("Drücke Enter zum Beenden...")
            sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        with open(app_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
            
        print("✅ App-Skript erstellt")
        return True
        
    def create_app_icon(self):
        """Erstelle App-Icon."""
        print("\n🎨 Erstelle App-Icon...")
        
        # Erstelle ein einfaches Icon mit tkinter
        try:
            import tkinter as tk
            from tkinter import Canvas
            
            # Erstelle Icon-Datei
            icon_path = self.project_root / "app_icon.ico"
            
            # Für macOS verwenden wir .icns, aber PyInstaller kann auch .ico
            # Hier erstellen wir ein einfaches Icon
            root = tk.Tk()
            root.withdraw()  # Verstecke das Fenster
            
            # Erstelle Canvas für Icon
            canvas = Canvas(root, width=256, height=256, bg='white')
            canvas.pack()
            
            # Zeichne einfaches Icon
            canvas.create_rectangle(20, 20, 236, 236, fill='#2E86AB', outline='#1B4F72', width=3)
            canvas.create_text(128, 100, text="deCONZ", fill='white', font=('Arial', 24, 'bold'))
            canvas.create_text(128, 140, text="→", fill='white', font=('Arial', 32, 'bold'))
            canvas.create_text(128, 180, text="Z2M", fill='white', font=('Arial', 24, 'bold'))
            
            # Speichere als PostScript (kann zu PNG konvertiert werden)
            canvas.postscript(file=str(icon_path).replace('.ico', '.ps'))
            
            root.destroy()
            print("✅ App-Icon erstellt")
            return True
            
        except Exception as e:
            print(f"⚠️ Icon-Erstellung fehlgeschlagen: {e}")
            print("   Verwende Standard-Icon...")
            return True
            
    def create_spec_file(self):
        """Erstelle PyInstaller .spec-Datei."""
        print("\n📋 Erstelle .spec-Datei...")
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app_main.py'],
    pathex=['{self.project_root}'],
    binaries=[],
    datas=[
        ('bin', 'bin'),
        ('config', 'config'),
        ('docs', 'docs'),
        ('examples', 'examples'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'requests',
        'yaml',
        'json',
        'threading',
        'datetime',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico' if os.path.exists('app_icon.ico') else None,
)

app = BUNDLE(
    exe,
    name='{self.app_name}.app',
    icon='app_icon.ico' if os.path.exists('app_icon.ico') else None,
    bundle_identifier='com.deconz.migration.tool',
    version='{self.app_version}',
    info_plist={{
        'CFBundleName': '{self.app_name}',
        'CFBundleDisplayName': 'deCONZ Migration Tool',
        'CFBundleIdentifier': 'com.deconz.migration.tool',
        'CFBundleVersion': '{self.app_version}',
        'CFBundleShortVersionString': '{self.app_version}',
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundleExecutable': '{self.app_name}',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
    }},
)
'''
        
        spec_file = self.project_root / f"{self.app_name}.spec"
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
            
        print("✅ .spec-Datei erstellt")
        return True
        
    def build_app(self):
        """Erstelle die .app-Anwendung."""
        print("\n🔨 Erstelle .app-Anwendung...")
        
        try:
            # Lösche alte App falls vorhanden
            if self.app_bundle.exists():
                shutil.rmtree(self.app_bundle)
                print("   Alte App gelöscht")
            
            # Erstelle App mit PyInstaller
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--windowed",
                "--name", self.app_name,
                "--distpath", str(self.project_root),
                "--workpath", str(self.project_root / "build"),
                "--specpath", str(self.project_root),
                f"{self.app_name}.spec"
            ]
            
            print(f"   Führe aus: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=str(self.project_root), capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ .app-Anwendung erstellt")
                return True
            else:
                print(f"❌ Fehler beim Erstellen der App: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim Erstellen der App: {e}")
            return False
            
    def create_dmg(self):
        """Erstelle DMG-Installer (optional)."""
        print("\n💿 Erstelle DMG-Installer...")
        
        try:
            dmg_name = f"{self.app_name}-{self.app_version}.dmg"
            dmg_path = self.project_root / dmg_name
            
            # Erstelle DMG mit hdiutil
            cmd = [
                "hdiutil", "create",
                "-volname", self.app_name,
                "-srcfolder", str(self.app_bundle),
                "-ov", "-format", "UDZO",
                str(dmg_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ DMG erstellt: {dmg_name}")
                return True
            else:
                print(f"⚠️ DMG-Erstellung fehlgeschlagen: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"⚠️ DMG-Erstellung fehlgeschlagen: {e}")
            return False
            
    def cleanup(self):
        """Räume temporäre Dateien auf."""
        print("\n🧹 Räume auf...")
        
        # Lösche temporäre Dateien
        temp_files = [
            "app_main.py",
            f"{self.app_name}.spec",
            "app_icon.ico",
            "app_icon.ps",
            "build"
        ]
        
        for file_name in temp_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                if file_path.is_dir():
                    shutil.rmtree(file_path)
                else:
                    file_path.unlink()
                print(f"   🗑️ {file_name} gelöscht")
                
        print("✅ Aufräumung abgeschlossen")
        return True
        
    def run(self):
        """Führe App-Erstellung aus."""
        self.print_header()
        
        # App-Erstellungs-Schritte
        steps = [
            ("PyInstaller prüfen", self.check_pyinstaller),
            ("App-Skript erstellen", self.create_app_script),
            ("App-Icon erstellen", self.create_app_icon),
            (".spec-Datei erstellen", self.create_spec_file),
            (".app-Anwendung erstellen", self.build_app),
            ("DMG-Installer erstellen", self.create_dmg),
            ("Aufräumen", self.cleanup)
        ]
        
        # Führe Schritte aus
        for step_name, step_func in steps:
            print(f"\n{'='*20} {step_name} {'='*20}")
            if not step_func():
                if step_name == "DMG-Installer erstellen":
                    print("⚠️ DMG-Erstellung fehlgeschlagen, aber App wurde erstellt")
                    continue
                else:
                    print(f"\n❌ App-Erstellung fehlgeschlagen bei: {step_name}")
                    return False
                    
        # Erfolg
        print("\n" + "="*60)
        print("🎉 macOS APP ERFOLGREICH ERSTELLT!")
        print("="*60)
        print(f"\n📱 App: {self.app_bundle}")
        print(f"📦 Größe: {self.get_app_size()}")
        print("\n🚀 Die App kann jetzt gestartet werden:")
        print(f"   open '{self.app_bundle}'")
        print("\n💡 Tipp: Die App kann in den Applications-Ordner kopiert werden")
        
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
    creator = MacAppCreator()
    success = creator.run()
    
    if success:
        print("\n🎯 Möchtest du die App jetzt starten? (j/n): ", end="")
        try:
            response = input().lower().strip()
            if response in ['j', 'ja', 'y', 'yes']:
                print("\n🚀 Starte App...")
                subprocess.run(["open", str(creator.app_bundle)])
        except KeyboardInterrupt:
            print("\n👋 App-Erstellung beendet")
    else:
        print("\n❌ App-Erstellung fehlgeschlagen!")
        sys.exit(1)

if __name__ == "__main__":
    main()
