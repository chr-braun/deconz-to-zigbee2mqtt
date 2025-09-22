#!/usr/bin/env python3
"""
Interaktives deCONZ zu Zigbee2MQTT Migration Tool
Führt den Benutzer Schritt für Schritt durch den Migrationsprozess
"""

import requests
import yaml
import random
import time
import sys
from pathlib import Path

def print_header():
    """Zeige den Header des Tools."""
    print("=" * 60)
    print("🚀 deCONZ zu Zigbee2MQTT Migration Tool")
    print("=" * 60)
    print("Dieses Tool hilft dir dabei, deine deCONZ-Geräte")
    print("zu Zigbee2MQTT zu migrieren.")
    print("=" * 60)

def get_user_input(prompt, default="", validator=None, error_msg="Ungültige Eingabe"):
    """Hole Benutzereingabe mit Validierung."""
    while True:
        try:
            if default:
                user_input = input(f"{prompt} [{default}]: ").strip()
                value = user_input if user_input else default
            else:
                value = input(f"{prompt}: ").strip()
            
            if not value:
                if default:
                    return default
                print("❌ Eingabe darf nicht leer sein!")
                continue
            
            if validator and not validator(value):
                print(f"❌ {error_msg}")
                continue
            
            return value
        except KeyboardInterrupt:
            print("\n\n👋 Migration abgebrochen!")
            sys.exit(0)

def validate_ip(ip):
    """Validiere IP-Adresse."""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

def validate_port(port):
    """Validiere Port-Nummer."""
    try:
        return 1 <= int(port) <= 65535
    except ValueError:
        return False

def test_connection(host, port):
    """Teste Verbindung zu deCONZ."""
    print(f"\n🔍 Teste Verbindung zu {host}:{port}...")
    try:
        response = requests.get(f"http://{host}:{port}/api", timeout=5)
        if response.status_code in [200, 403]:
            print("✅ Verbindung erfolgreich!")
            return True
        else:
            print(f"❌ Verbindung fehlgeschlagen: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Verbindung fehlgeschlagen: {e}")
        return False

def generate_api_key(host, port):
    """Generiere API-Key mit interaktiver Anleitung."""
    print("\n" + "=" * 60)
    print("🔑 API-Key Generierung")
    print("=" * 60)
    print("Um einen API-Key zu generieren, musst du den")
    print("LINK-BUTTON auf deinem deCONZ-Gateway drücken.")
    print("\n📋 Anleitung:")
    print("1. Gehe zu deinem deCONZ-Gateway")
    print("2. Drücke den LINK-BUTTON (meist 5-10 Sekunden halten)")
    print("3. Warte bis die LED blinkt oder sich ändert")
    print("4. Drücke dann ENTER hier im Terminal")
    print("\n⏱️  Du hast 60 Sekunden Zeit!")
    print("=" * 60)
    
    input("\nDrücke ENTER wenn du den Link-Button gedrückt hast...")
    
    # Generiere App-Namen
    app_name = f"deconz-migrator-{random.randint(1000, 9999)}"
    url = f"http://{host}:{port}/api"
    payload = {"devicetype": app_name}
    headers = {"Content-Type": "application/json"}
    
    print(f"\n🔄 Generiere API-Key...")
    print(f"📱 App-Name: {app_name}")
    
    try:
        # Erster Versuch
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 403]:
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                result = data[0]
                
                if "success" in result and "username" in result["success"]:
                    api_key = result["success"]["username"]
                    print(f"✅ API-Key erfolgreich generiert!")
                    print(f"🔑 API-Key: {api_key}")
                    return api_key
                    
                elif "error" in result:
                    error_msg = result["error"].get("description", "Unbekannter Fehler")
                    print(f"❌ Fehler: {error_msg}")
                    
                    if "link button not pressed" in error_msg.lower():
                        print("\n🔄 Link-Button nicht erkannt. Versuche es erneut...")
                        print("Drücke den Link-Button nochmal und warte 5 Sekunden...")
                        time.sleep(5)
                        
                        # Zweiter Versuch
                        response2 = requests.post(url, json=payload, headers=headers, timeout=10)
                        if response2.status_code in [200, 403]:
                            data2 = response2.json()
                            if isinstance(data2, list) and len(data2) > 0:
                                result2 = data2[0]
                                if "success" in result2 and "username" in result2["success"]:
                                    api_key = result2["success"]["username"]
                                    print(f"✅ API-Key erfolgreich generiert (2. Versuch)!")
                                    print(f"🔑 API-Key: {api_key}")
                                    return api_key
                                else:
                                    print(f"❌ Auch der zweite Versuch fehlgeschlagen: {result2}")
                    else:
                        print(f"❌ Unerwarteter Fehler: {error_msg}")
        else:
            print(f"❌ HTTP-Fehler: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Fehler bei API-Key-Generierung: {e}")
    
    print("\n💡 Tipps:")
    print("- Stelle sicher, dass deCONZ läuft")
    print("- Drücke den Link-Button länger (5-10 Sekunden)")
    print("- Versuche es erneut")
    return None

def get_network_config(host, port, api_key):
    """Hole Netzwerkkonfiguration von deCONZ."""
    print(f"\n📋 Hole Netzwerkkonfiguration...")
    
    try:
        url = f"http://{host}:{port}/api/{api_key}/config"
        headers = {"Content-Type": "application/json"}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            config = response.json()
            
            network_config = {
                'channel': config.get('zigbeechannel'),
                'pan_id': config.get('panid'),
                'ext_pan_id': config.get('extpanid'),
                'network_key': config.get('networkkey'),
                'name': config.get('name', 'deCONZ'),
                'version': config.get('version', 'Unknown')
            }
            
            print("✅ Netzwerkkonfiguration abgerufen:")
            print(f"   📡 Kanal: {network_config['channel']}")
            print(f"   🆔 PAN-ID: 0x{network_config['pan_id']:04X}")
            print(f"   🏠 Gateway: {network_config['name']}")
            
            return network_config
        else:
            print(f"❌ Fehler beim Abrufen der Konfiguration: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None

def get_devices(host, port, api_key):
    """Hole alle Geräte von deCONZ."""
    print(f"\n🔍 Hole Geräte...")
    
    devices = []
    
    try:
        headers = {"Content-Type": "application/json"}
        base_url = f"http://{host}:{port}/api/{api_key}"
        
        # Hole Sensoren
        print("   📊 Lade Sensoren...")
        sensors_response = requests.get(f"{base_url}/sensors", headers=headers, timeout=10)
        if sensors_response.status_code == 200:
            sensors = sensors_response.json()
            for sensor_id, sensor in sensors.items():
                device_info = {
                    'id': sensor_id,
                    'name': sensor.get('name', f'sensor_{sensor_id}'),
                    'type': 'sensor',
                    'model': sensor.get('modelid', ''),
                    'manufacturer': sensor.get('manufacturername', ''),
                    'unique_id': sensor.get('uniqueid', ''),
                    'state': sensor.get('state', {})
                }
                devices.append(device_info)
            print(f"   ✅ {len(sensors)} Sensoren gefunden")
        
        # Hole Lichter
        print("   💡 Lade Lichter...")
        lights_response = requests.get(f"{base_url}/lights", headers=headers, timeout=10)
        if lights_response.status_code == 200:
            lights = lights_response.json()
            for light_id, light in lights.items():
                device_info = {
                    'id': light_id,
                    'name': light.get('name', f'light_{light_id}'),
                    'type': 'light',
                    'model': light.get('modelid', ''),
                    'manufacturer': light.get('manufacturername', ''),
                    'unique_id': light.get('uniqueid', ''),
                    'state': light.get('state', {})
                }
                devices.append(device_info)
            print(f"   ✅ {len(lights)} Lichter gefunden")
        
        print(f"\n✅ Insgesamt {len(devices)} Geräte gefunden!")
        return devices
        
    except Exception as e:
        print(f"❌ Fehler beim Abrufen der Geräte: {e}")
        return []

def generate_random_hex(byte_count):
    """Generiere zufällige Hex-Zeichen."""
    return ''.join(random.choices('0123456789abcdef', k=byte_count * 2))

def create_zigbee2mqtt_config(devices, network_config, mqtt_server, mqtt_topic):
    """Erstelle Zigbee2MQTT-Konfiguration."""
    print(f"\n⚙️ Erstelle Zigbee2MQTT-Konfiguration...")
    
    # Verwende Netzwerkkonfiguration oder generiere Werte
    channel = network_config.get('channel', 15) if network_config else 15
    pan_id = network_config.get('pan_id', 0x1A63) if network_config else 0x1A63
    
    # Generiere fehlende Werte
    if not network_config or not network_config.get('ext_pan_id'):
        ext_pan_id = generate_random_hex(8)
        print(f"   🔧 Extended PAN ID generiert: 0x{ext_pan_id}")
    else:
        ext_pan_id = f"{network_config['ext_pan_id']:016X}"
    
    if not network_config or not network_config.get('network_key'):
        network_key = generate_random_hex(16)
        print(f"   🔧 Network Key generiert: 0x{network_key}")
    else:
        network_key = f"{network_config['network_key']:032X}"
    
    # Erstelle Konfiguration
    config = {
        'mqtt': {
            'base_topic': mqtt_topic,
            'server': mqtt_server
        },
        'serial': {
            'port': '/dev/ttyACM0'
        },
        'advanced': {
            'pan_id': f"0x{pan_id:04X}",
            'extended_pan_id': f"0x{ext_pan_id}",
            'network_key': f"[{', '.join(f'0x{network_key[i:i+2]}' for i in range(0, len(network_key), 2))}]",
            'channel': int(channel)
        },
        'devices': []
    }
    
    # Füge Geräte hinzu
    for device in devices:
        device_config = {
            'id': device['id'],
            'name': device['name'],
            'type': device['type']
        }
        
        if device['model']:
            device_config['model'] = device['model']
        if device['manufacturer']:
            device_config['manufacturer'] = device['manufacturer']
            
        config['devices'].append(device_config)
    
    return config

def save_config(config, filename="configuration.yaml"):
    """Speichere Konfiguration in Datei."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, sort_keys=False, default_flow_style=False, 
                     allow_unicode=True, indent=2)
        print(f"✅ Konfiguration gespeichert: {filename}")
        return True
    except Exception as e:
        print(f"❌ Fehler beim Speichern: {e}")
        return False

def show_summary(devices, network_config):
    """Zeige Migrationszusammenfassung."""
    print("\n" + "=" * 60)
    print("📊 MIGRATIONSZUSAMMENFASSUNG")
    print("=" * 60)
    
    sensors = [d for d in devices if d['type'] == 'sensor']
    lights = [d for d in devices if d['type'] == 'light']
    
    print(f"🔢 Geräte gesamt: {len(devices)}")
    print(f"   📊 Sensoren: {len(sensors)}")
    print(f"   💡 Lichter: {len(lights)}")
    
    if network_config:
        print(f"\n📡 Netzwerkkonfiguration:")
        print(f"   Kanal: {network_config.get('channel', 'Unbekannt')}")
        print(f"   PAN-ID: 0x{network_config.get('pan_id', 0):04X}")
        print(f"   Gateway: {network_config.get('name', 'Unbekannt')}")
    
    print(f"\n📁 Ausgabedatei: configuration.yaml")
    print("=" * 60)

def main():
    """Hauptfunktion des interaktiven Migration Tools."""
    print_header()
    
    # Schritt 1: deCONZ-Server-Informationen
    print("\n📡 SCHRITT 1: deCONZ-Server")
    print("-" * 30)
    
    host = get_user_input(
        "deCONZ Server IP-Adresse", 
        "192.168.178.76",
        validate_ip,
        "Ungültige IP-Adresse (z.B. 192.168.1.100)"
    )
    
    port = get_user_input(
        "deCONZ Port", 
        "4530",
        validate_port,
        "Ungültiger Port (1-65535)"
    )
    
    # Teste Verbindung
    if not test_connection(host, int(port)):
        print("\n❌ Kann nicht mit deCONZ-Server verbinden!")
        print("💡 Prüfe IP-Adresse und Port, stelle sicher dass deCONZ läuft.")
        return
    
    # Schritt 2: API-Key generieren
    print("\n🔑 SCHRITT 2: API-Key")
    print("-" * 30)
    
    api_key = generate_api_key(host, int(port))
    if not api_key:
        print("\n❌ API-Key-Generierung fehlgeschlagen!")
        return
    
    # Schritt 3: Netzwerkkonfiguration abrufen
    print("\n📋 SCHRITT 3: Netzwerkkonfiguration")
    print("-" * 30)
    
    network_config = get_network_config(host, int(port), api_key)
    
    # Schritt 4: Geräte abrufen
    print("\n🔍 SCHRITT 4: Geräte")
    print("-" * 30)
    
    devices = get_devices(host, int(port), api_key)
    if not devices:
        print("\n❌ Keine Geräte gefunden!")
        return
    
    # Schritt 5: MQTT-Konfiguration
    print("\n📡 SCHRITT 5: MQTT-Konfiguration")
    print("-" * 30)
    
    mqtt_server = get_user_input(
        "MQTT Server URL", 
        "mqtt://localhost",
        None,
        ""
    )
    
    mqtt_topic = get_user_input(
        "MQTT Base Topic", 
        "zigbee2mqtt",
        None,
        ""
    )
    
    # Schritt 6: Konfiguration erstellen
    print("\n⚙️ SCHRITT 6: Konfiguration erstellen")
    print("-" * 30)
    
    config = create_zigbee2mqtt_config(devices, network_config, mqtt_server, mqtt_topic)
    
    # Schritt 7: Speichern
    print("\n💾 SCHRITT 7: Speichern")
    print("-" * 30)
    
    if save_config(config):
        show_summary(devices, network_config)
        print("\n🎉 Migration erfolgreich abgeschlossen!")
        print("\n📋 Nächste Schritte:")
        print("1. Kopiere configuration.yaml nach Zigbee2MQTT")
        print("2. Starte Zigbee2MQTT mit der neuen Konfiguration")
        print("3. Prüfe die Geräte in der Zigbee2MQTT-Oberfläche")
    else:
        print("\n❌ Migration fehlgeschlagen!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Migration abgebrochen!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")
        sys.exit(1)
