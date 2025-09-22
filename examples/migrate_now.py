#!/usr/bin/env python3
"""
Schnelle Migration mit vorkonfigurierten Werten
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from deconz_to_z2m import DeconzToZ2MMigrator

def main():
    print("🚀 deCONZ zu Zigbee2MQTT Migration")
    print("=" * 50)
    print("Verwende vorkonfigurierte Werte:")
    print("  Host: 192.168.178.76")
    print("  Port: 4530")
    print("  API-Key: 99D54B94DA")
    print("=" * 50)
    
    # Erstelle Migrator
    migrator = DeconzToZ2MMigrator()
    
    # Simuliere Benutzereingaben
    import io
    from unittest.mock import patch
    
    # Eingaben simulieren: REST-API, Host, Port, API-Key, MQTT, Topic, Dry-run
    inputs = [
        "2",  # REST-API
        "",   # Host (Standard)
        "",   # Port (Standard)
        "99D54B94DA",  # API-Key
        "mqtt://localhost",  # MQTT Server
        "zigbee2mqtt",  # MQTT Topic
        "N"   # Dry-run (nein)
    ]
    
    with patch('builtins.input', side_effect=inputs):
        try:
            migrator.run_migration()
            print("\n✅ Migration erfolgreich abgeschlossen!")
        except Exception as e:
            print(f"\n❌ Fehler: {e}")

if __name__ == "__main__":
    main()
