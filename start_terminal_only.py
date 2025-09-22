#!/usr/bin/env python3
"""
Terminal-only Launcher für deCONZ zu Zigbee2MQTT Migration Tool
Funktioniert auch ohne tkinter
"""

import sys
import os
from pathlib import Path

# Füge bin-Verzeichnis zum Python-Pfad hinzu
project_root = Path(__file__).parent
bin_path = project_root / "bin"
sys.path.insert(0, str(bin_path))

def main():
    """Hauptfunktion."""
    print("🚀 deCONZ zu Zigbee2MQTT Migration Tool - Terminal")
    print("=" * 50)
    
    try:
        from final_interactive import main as terminal_main
        terminal_main()
    except ImportError as e:
        print(f"❌ Terminal-Tool konnte nicht gestartet werden: {e}")
        print("Führe 'python3 install.py' aus, um das Tool zu installieren")
        sys.exit(1)

if __name__ == "__main__":
    main()
