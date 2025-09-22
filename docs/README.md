# 🚀 deCONZ zu Zigbee2MQTT Migration Tool

> **Vollständig installiert!** Migration Tool für deCONZ-Geräte nach Zigbee2MQTT

## 🚀 Schnellstart

### Installation
```bash
# Automatische Installation
python3 install.py

# Oder manuell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Verwendung
```bash
# GUI starten (empfohlen)
python3 start_gui.py

# Terminal starten
python3 start_terminal.py
```

## 📁 Verzeichnisstruktur

```
deconz-to-zigbee2mqtt/
├── bin/                    # Ausführbare Tools
│   ├── advanced_gui.py    # Haupt-GUI
│   ├── gui_migrate.py     # Basis-GUI
│   ├── final_interactive.py
│   └── ...
├── config/                 # Konfigurationsdateien
│   ├── requirements.txt
│   └── configuration.yaml
├── docs/                   # Dokumentation
│   ├── README.md
│   ├── gui_features.md
│   └── ...
├── examples/               # Beispiel-Skripte
├── logs/                   # Log-Dateien
├── temp/                   # Temporäre Dateien
├── venv/                   # Virtuelle Umgebung
├── start_gui.py           # GUI-Starter
├── start_terminal.py      # Terminal-Starter
└── install.py             # Installationsskript
```

## 🛠️ Tools

### GUI-Tools
- `python3 start_gui.py` - Erweiterte GUI
- `python3 bin/gui_migrate.py` - Basis-GUI

### Terminal-Tools
- `python3 start_terminal.py` - Interaktives Terminal-Tool
- `python3 bin/final_interactive.py` - Direktes Terminal-Tool

## ✅ Erfolgreich getestet

- **deCONZ-Server**: 192.168.178.76:4530
- **Geräte migriert**: 86 (69 Sensoren + 17 Lichter)
- **Konfiguration**: Vollständige `configuration.yaml` generiert
- **GUI**: Moderne grafische Benutzeroberfläche

## 🎯 Features

- **🖥️ GUI**: Moderne grafische Benutzeroberfläche
- **💻 Terminal**: Interaktive Terminal-Version
- **🔑 API-Key**: Automatische Generierung mit Link-Button
- **📊 Geräte**: 86 Geräte (69 Sensoren + 17 Lichter)
- **⚙️ Konfiguration**: Vollständige Zigbee2MQTT-Konfiguration
- **📋 Logging**: Detailliertes Log mit Zeitstempel

## 🚀 Nächste Schritte

1. **Zigbee2MQTT installieren**
2. **Konfiguration kopieren**: `config/configuration.yaml` → Zigbee2MQTT
3. **Zigbee2MQTT starten** mit neuer Konfiguration
4. **Geräte prüfen** in der Zigbee2MQTT-Oberfläche

---

**Migration erfolgreich abgeschlossen!** 🎉
