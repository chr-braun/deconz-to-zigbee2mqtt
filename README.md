# 🚀 deCONZ zu Zigbee2MQTT Migration Tool

> **🚧 Work in Progress** - Professionelles Migration Tool für deCONZ-Geräte nach Zigbee2MQTT

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![macOS](https://img.shields.io/badge/macOS-10.13+-green.svg)](https://apple.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Work%20in%20Progress-orange.svg)](README.md)

## 📋 Inhaltsverzeichnis

- [Installation](#-installation)
- [Schnellstart](#-schnellstart)
- [Verzeichnisstruktur](#-verzeichnisstruktur)
- [Tools](#-tools)
- [Features](#-features)
- [Status](#-status)
- [Mitwirkende](#-mitwirkende)
- [Lizenz](#-lizenz)

## 🚀 Installation

### Voraussetzungen
- Python 3.8 oder höher
- macOS 10.13 oder höher (für .app-Bundle)
- deCONZ-Gateway mit aktivierter REST-API
- Zigbee2MQTT (für die Migration)

### Automatische Installation
```bash
# Repository klonen
git clone https://github.com/username/deconz-to-zigbee2mqtt.git
cd deconz-to-zigbee2mqtt

# Automatische Installation
python3 install.py
```

### Manuelle Installation
```bash
# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

## 🎯 Schnellstart

### 🖥️ GUI starten (Empfohlen)
```bash
python3 start_gui.py
```

### 💻 Terminal starten
```bash
python3 start_terminal.py
```

### 🍎 macOS App erstellen
```bash
python3 create_app_with_logs.py
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
├── deCONZ-Migration-Tool.app  # macOS App
├── install.py             # Installationsskript
└── simple_mac_app.py      # macOS App Creator
```

## 🛠️ Tools

### GUI-Tools
- `python3 start_gui.py` - Erweiterte GUI
- `python3 bin/gui_migrate.py` - Basis-GUI

### Terminal-Tools
- `python3 start_terminal.py` - Interaktives Terminal-Tool
- `python3 bin/final_interactive.py` - Direktes Terminal-Tool

### macOS App
- `deCONZ-Migration-Tool.app` - Native macOS-Anwendung
- `python3 simple_mac_app.py` - App-Erstellung

## 🎯 Features

### 🖥️ Benutzeroberflächen
- **GUI-Version**: Moderne grafische Benutzeroberfläche mit Tab-Navigation
- **Terminal-Version**: Interaktive Kommandozeilen-Tools
- **macOS App**: Native .app-Bundle für einfache Nutzung

### 🔧 Migration-Features
- **API-Key-Generierung**: Automatische Generierung mit Link-Button-Unterstützung
- **Geräte-Migration**: Automatische Migration aller deCONZ-Geräte
- **Konfigurationsgenerierung**: Vollständige `configuration.yaml` für Zigbee2MQTT
- **Netzwerk-Parameter**: Automatische Übertragung von Kanal, PAN-ID, etc.

### 📊 Getestete Konfiguration
- **deCONZ-Server**: 192.168.178.76:4530
- **Geräte migriert**: 86 (69 Sensoren + 17 Lichter)
- **Konfiguration**: Vollständige `configuration.yaml` generiert
- **GUI**: Moderne grafische Benutzeroberfläche funktional

## 🚧 Status

### ✅ Implementiert
- [x] Terminal-basierte Migration
- [x] GUI-Interface (tkinter)
- [x] macOS .app-Bundle
- [x] API-Key-Generierung
- [x] Geräte-Migration
- [x] Konfigurationsgenerierung
- [x] Virtuelle Umgebung
- [x] Installationsskripte

### 🚧 Work in Progress
- [ ] Fehlerbehandlung verbessern
- [ ] Logging-System erweitern
- [ ] Dokumentation vervollständigen
- [ ] Tests hinzufügen
- [ ] CI/CD-Pipeline

### 📋 Geplant
- [ ] Windows-Unterstützung
- [ ] Linux-Unterstützung
- [ ] Docker-Container
- [ ] Web-Interface
- [ ] Automatische Updates

## 🤝 Mitwirkende

- **Entwickler**: Christian Braun
- **Projekt**: deCONZ zu Zigbee2MQTT Migration Tool
- **Status**: Work in Progress

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

---

**Work in Progress - Beiträge sind willkommen!** 🚧
