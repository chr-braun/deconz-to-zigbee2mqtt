#!/usr/bin/env python3
"""
Einfache macOS App für deCONZ zu Zigbee2MQTT Migration Tool
Erstellt eine .app-Bundle ohne PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

class SimpleMacAppCreator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.app_name = "deCONZ-Migration-Tool"
        self.app_bundle = self.project_root / f"{self.app_name}.app"
        
    def print_header(self):
        """Zeige App-Erstellungs-Header."""
        print("=" * 60)
        print("🍎 Einfache macOS App Creator")
        print("=" * 60)
        print("Erstellt eine .app-Bundle ohne PyInstaller")
        print("=" * 60)
        
    def create_app_structure(self):
        """Erstelle App-Bundle-Struktur."""
        print("\n📁 Erstelle App-Bundle-Struktur...")
        
        # Lösche alte App
        if self.app_bundle.exists():
            shutil.rmtree(self.app_bundle)
            print("   Alte App gelöscht")
        
        # Erstelle App-Bundle-Verzeichnisse
        contents_dir = self.app_bundle / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        for dir_path in [contents_dir, macos_dir, resources_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   📁 {dir_path.relative_to(self.project_root)}/")
            
        print("✅ App-Bundle-Struktur erstellt")
        return True
        
    def create_info_plist(self):
        """Erstelle Info.plist."""
        print("\n📋 Erstelle Info.plist...")
        
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
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeName</key>
            <string>YAML Configuration</string>
            <key>CFBundleTypeRole</key>
            <string>Editor</string>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>yaml</string>
                <string>yml</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
'''
        
        plist_path = self.app_bundle / "Contents" / "Info.plist"
        with open(plist_path, 'w', encoding='utf-8') as f:
            f.write(info_plist)
            
        print("✅ Info.plist erstellt")
        return True
        
    def create_launcher_script(self):
        """Erstelle Launcher-Skript."""
        print("\n🚀 Erstelle Launcher-Skript...")
        
        launcher_script = '''#!/bin/bash
# deCONZ Migration Tool Launcher

# Ermittle App-Verzeichnis
APP_DIR="$(dirname "$0")"
APP_ROOT="$(dirname "$APP_DIR")"
RESOURCES_DIR="$APP_DIR/../Resources"

# Wechsle zum App-Verzeichnis
cd "$RESOURCES_DIR"

# Prüfe Python
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python 3 ist nicht installiert. Bitte installiere Python 3 von python.org" buttons {"OK"} default button "OK"'
    exit 1
fi

# Prüfe tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    osascript -e 'display dialog "tkinter ist nicht verfügbar. Bitte installiere Python mit tkinter-Support." buttons {"OK"} default button "OK"'
    exit 1
fi

# Starte GUI
echo "Starte deCONZ Migration Tool..."
python3 start_gui.py

# Falls GUI fehlschlägt, starte Terminal-Version
if [ $? -ne 0 ]; then
    echo "GUI fehlgeschlagen, starte Terminal-Version..."
    python3 start_terminal.py
fi
'''
        
        launcher_path = self.app_bundle / "Contents" / "MacOS" / "launcher"
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_script)
            
        # Mache Launcher ausführbar
        os.chmod(launcher_path, 0o755)
        
        print("✅ Launcher-Skript erstellt")
        return True
        
    def copy_resources(self):
        """Kopiere Ressourcen in die App."""
        print("\n📦 Kopiere Ressourcen...")
        
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
                print(f"   📄 {file_name}")
        
        # Kopiere Verzeichnisse
        dirs_to_copy = ["bin", "config", "docs", "examples", "logs", "temp"]
        
        for dir_name in dirs_to_copy:
            source_dir = self.project_root / dir_name
            if source_dir.exists():
                dest_dir = resources_dir / dir_name
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
                print(f"   📁 {dir_name}/")
        
        print("✅ Ressourcen kopiert")
        return True
        
    def create_app_icon(self):
        """Erstelle App-Icon."""
        print("\n🎨 Erstelle App-Icon...")
        
        try:
            # Erstelle einfaches Icon mit Python
            icon_script = '''
import tkinter as tk
from tkinter import Canvas
import os

# Erstelle Icon-Fenster
root = tk.Tk()
root.withdraw()

# Erstelle Canvas
canvas = Canvas(root, width=512, height=512, bg='white')
canvas.pack()

# Zeichne Icon
canvas.create_rectangle(50, 50, 462, 462, fill='#2E86AB', outline='#1B4F72', width=8)
canvas.create_text(256, 200, text="deCONZ", fill='white', font=('Arial', 48, 'bold'))
canvas.create_text(256, 280, text="→", fill='white', font=('Arial', 64, 'bold'))
canvas.create_text(256, 360, text="Z2M", fill='white', font=('Arial', 48, 'bold'))

# Speichere als PostScript
canvas.postscript(file='app_icon.ps')
root.destroy()

print("Icon erstellt")
'''
            
            # Führe Icon-Skript aus
            result = subprocess.run([sys.executable, "-c", icon_script], 
                                  cwd=str(self.app_bundle / "Contents" / "Resources"),
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ App-Icon erstellt")
            else:
                print("⚠️ Icon-Erstellung fehlgeschlagen, verwende Standard")
                
        except Exception as e:
            print(f"⚠️ Icon-Erstellung fehlgeschlagen: {e}")
            
        return True
        
    def create_dmg(self):
        """Erstelle DMG-Installer."""
        print("\n💿 Erstelle DMG-Installer...")
        
        try:
            dmg_name = f"{self.app_name}-1.0.0.dmg"
            dmg_path = self.project_root / dmg_name
            
            # Erstelle DMG
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
            
    def run(self):
        """Führe App-Erstellung aus."""
        self.print_header()
        
        # App-Erstellungs-Schritte
        steps = [
            ("App-Bundle-Struktur erstellen", self.create_app_structure),
            ("Info.plist erstellen", self.create_info_plist),
            ("Launcher-Skript erstellen", self.create_launcher_script),
            ("Ressourcen kopieren", self.copy_resources),
            ("App-Icon erstellen", self.create_app_icon),
            ("DMG-Installer erstellen", self.create_dmg)
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
        print("   cp -R '{self.app_bundle}' /Applications/")
        
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
    creator = SimpleMacAppCreator()
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
