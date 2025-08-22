
# deCONZ → Zigbee2MQTT Migration Tool (work in progress)

> Migration Tool für deCONZ-Geräte nach Zigbee2MQTT

## Features
- Automatische Suche der deCONZ-Datenbank (zll.db)
- Abfrage von Kanal, PAN-ID, Extended PAN ID, API-Key
- Dry-Run-Modus
- Export für Zigbee2MQTT

## Installation
```bash
git clone https://github.com/chr-braun/deconz-to-z2m.git
cd deconz-to-z2m
python3 -m venv deconz-migrator-env
source deconz-migrator-env/bin/activate
pip install -r requirements.txt
```

## Datenbank suchen
```bash
sudo find / -name "zll.db" 2>/dev/null
sudo find / -name "*deconz*" -type d 2>/dev/null
sudo find / -name "*dresden*" -type d 2>/dev/null
```

## API-Key anfordern
```bash
curl -X POST http://<DECONZ-IP>:<PORT>/api -d '{"devicetype": "my_app"}'
```

## Skript ausführen
```bash
python3 deconz_to_z2m.py
```

- Abfragen: Kanal, PAN-ID, Extended PAN ID, API-Key, Dry-Run
- Ergebnis: configuration.yaml
