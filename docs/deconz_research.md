# deCONZ Schnittstellen und Python-Bibliotheken - Recherche

## Projektübersicht
**deCONZ zu Zigbee2MQTT Migration Tool** - Ein Tool zur Migration von Geräten und Konfigurationen von deCONZ zu Zigbee2MQTT.

## Aktueller Stand des Projekts
- **Hauptklasse**: `DeconzToZ2MMigrator`
- **Datenquelle**: SQLite-Datenbank (`zll.db`) mit direkten Datenbankabfragen
- **Funktionen**: 
  - Automatische Datenbanksuche
  - Netzwerkparameter-Extraktion (Kanal, PAN-ID, Extended PAN ID, Network Key)
  - Geräte-Migration aus Datenbank
  - Dry-Run-Modus
  - YAML-Export für Zigbee2MQTT

## deCONZ Schnittstellen

### 1. REST-API (Empfohlen für Erweiterung)
**Hauptendpunkte:**
- `/api` - API-Authentifizierung und -Verwaltung
- `/config` - Netzwerkkonfiguration (Kanal, PAN-ID, etc.)
- `/sensors` - Alle Sensoren und deren Werte
- `/lights` - Alle Lichter und deren Zustand
- `/groups` - Gruppen von Geräten
- `/scenes` - Szenen und Automatisierungen
- `/rules` - Automatisierungsregeln

**Vorteile:**
- Strukturierte JSON-Daten
- Live-Daten (nicht nur gespeicherte)
- Einfacher zu verwenden als Datenbankabfragen
- Netzwerkparameter direkt abrufbar

### 2. WebSocket-API
- Echtzeit-Updates über Änderungen im Zigbee-Netzwerk
- Ideal für Live-Monitoring und sofortige Benachrichtigungen

### 3. Datenbankzugriff (Aktuell verwendet)
- SQLite-Datenbank (`zll.db`)
- Direkte Zugriffsmöglichkeiten
- Detaillierte Netzwerkparameter und Geräteinformationen

### 4. Prometheus Exporter
- Spezieller Exporter für Monitoring-Metriken
- Konvertiert Sensordaten in Prometheus-Format

## Python-Bibliotheken für deCONZ

### 1. pydeconz (Empfohlen)
- **Zweck**: Wrapper für die deCONZ REST-API
- **Verwendung**: Hauptsächlich in Home Assistant
- **Features**: 
  - Kommunikation mit deCONZ REST-API
  - Unterstützung der meisten deCONZ-Geräte
  - Einfache Integration in Python-Projekte
- **Installation**: `pip install pydeconz`

### 2. zigpy-deconz
- **Zweck**: Zigbee-Integration über deCONZ-Hardware
- **Verwendung**: Teil des zigpy-Frameworks
- **Features**:
  - Kommunikation mit ConBee/RaspBee-Modulen
  - Low-Level Zigbee-Protokoll-Zugriff
  - Integration in Smart-Home-Systeme
- **GitHub**: [zigpy/zigpy-deconz](https://github.com/zigpy/zigpy-deconz)

### 3. deconz (Home Assistant)
- **Zweck**: Spezielle Implementierung für Home Assistant
- **Features**:
  - REST-API-Integration
  - Geräteunterstützung
  - Home Assistant-spezifische Funktionen

## Empfohlene Erweiterungen

### Option 1: REST-API Integration
- **pydeconz** für REST-API-Zugriff nutzen
- Kombination aus Datenbank + REST-API
- Live-Daten zusätzlich zu historischen Daten erfassen

### Option 2: Hybrid-Ansatz
- Datenbank für historische Gerätedaten
- REST-API für aktuelle Netzwerkkonfiguration
- Bessere Datenqualität und Vollständigkeit

## Nächste Schritte
1. pydeconz in requirements.txt hinzufügen
2. REST-API-Integration in DeconzToZ2MMigrator implementieren
3. Konfigurationsabfrage über REST-API statt manueller Eingabe
4. Live-Gerätedaten über REST-API abrufen
5. Fallback auf Datenbank bei API-Fehlern

## Quellen
- [deCONZ REST API Dokumentation](https://dresden-elektronik.github.io/deconz-rest-doc/)
- [pydeconz auf PyPI](https://pypi.org/project/pydeconz/)
- [zigpy-deconz auf GitHub](https://github.com/zigpy/zigpy-deconz)
