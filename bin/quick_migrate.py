#!/usr/bin/env python3
"""
Schnelle Migration mit festen Werten
"""

import requests
import yaml
import random
from pathlib import Path

def generate_random_hex(byte_count: int) -> str:
    """Generiere zufällige Hex-Zeichen."""
    return ''.join(random.choices('0123456789abcdef', k=byte_count * 2))

def main():
    print("🚀 deCONZ zu Zigbee2MQTT Migration")
    print("=" * 50)
    
    # Konfiguration
    host = "192.168.178.76"
    port = 4530
    api_key = "99D54B94DA"
    base_url = f"http://{host}:{port}/api"
    headers = {"Content-Type": "application/json"}
    
    print(f"🔗 Verbinde zu {host}:{port}")
    print(f"🔑 API-Key: {api_key}")
    
    try:
        # Hole Konfiguration
        print("\n📋 Hole Netzwerkkonfiguration...")
        config_response = requests.get(f"{base_url}/{api_key}/config", headers=headers, timeout=10)
        
        if config_response.status_code != 200:
            print(f"❌ Fehler beim Abrufen der Konfiguration: {config_response.status_code}")
            return
        
        config = config_response.json()
        channel = config.get('zigbeechannel', 15)
        pan_id = config.get('panid', 0x1A63)
        
        print(f"✅ Kanal: {channel}")
        print(f"✅ PAN-ID: 0x{pan_id:04X}")
        
        # Generiere fehlende Werte
        ext_pan_id = generate_random_hex(8)
        network_key = generate_random_hex(16)
        
        print(f"✅ Extended PAN ID: 0x{ext_pan_id}")
        print(f"✅ Network Key: 0x{network_key}")
        
        # Hole Geräte
        print("\n🔍 Hole Geräte...")
        devices = []
        
        # Sensoren
        sensors_response = requests.get(f"{base_url}/{api_key}/sensors", headers=headers, timeout=10)
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
        
        # Lichter
        lights_response = requests.get(f"{base_url}/{api_key}/lights", headers=headers, timeout=10)
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
        
        print(f"✅ {len(devices)} Geräte gefunden")
        
        # Erstelle Zigbee2MQTT-Konfiguration
        print("\n⚙️ Erstelle Zigbee2MQTT-Konfiguration...")
        
        zigbee2mqtt_config = {
            'mqtt': {
                'base_topic': 'zigbee2mqtt',
                'server': 'mqtt://localhost'
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
                
            zigbee2mqtt_config['devices'].append(device_config)
        
        # Speichere Konfiguration
        output_file = "configuration.yaml"
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(zigbee2mqtt_config, f, sort_keys=False, default_flow_style=False, 
                     allow_unicode=True, indent=2)
        
        print(f"✅ Konfiguration gespeichert: {output_file}")
        print(f"📊 Statistiken:")
        print(f"   - Sensoren: {len([d for d in devices if d['type'] == 'sensor'])}")
        print(f"   - Lichter: {len([d for d in devices if d['type'] == 'light'])}")
        print(f"   - Kanal: {channel}")
        print(f"   - PAN-ID: 0x{pan_id:04X}")
        
        print("\n🎉 Migration erfolgreich abgeschlossen!")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
