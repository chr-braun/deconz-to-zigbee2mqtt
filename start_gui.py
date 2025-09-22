#!/usr/bin/env python3
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
