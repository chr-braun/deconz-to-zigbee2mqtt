#!/usr/bin/env python3
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
