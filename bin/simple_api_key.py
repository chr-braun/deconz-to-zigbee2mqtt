#!/usr/bin/env python3
"""
Einfaches Skript zum Generieren eines deCONZ API-Keys
"""

import requests
import json
import sys

def get_api_key(host: str, port: int = 4530):
    """
    Generiere einen API-Key für deCONZ.
    
    Args:
        host: deCONZ-Host-IP
        port: deCONZ-Port
    """
    url = f"http://{host}:{port}/api"
    payload = {"devicetype": "deconz-migrator"}
    headers = {"Content-Type": "application/json"}
    
    print(f"🔗 Verbinde zu deCONZ auf {host}:{port}")
    print("⚠️  WICHTIG: Drücke den Link-Button auf deinem deCONZ-Gateway!")
    print("⏱️  Du hast 60 Sekunden Zeit...")
    
    try:
        # Erster Versuch
        print("\n🔄 Versuche API-Key zu generieren...")
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
                        print("\n🔄 Warte 10 Sekunden und versuche es erneut...")
                        import time
                        time.sleep(10)
                        
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
                print("❌ Ungültige Antwort vom Server")
        else:
            print(f"❌ HTTP-Fehler: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print("\n💡 Tipps:")
    print("1. Stelle sicher, dass deCONZ läuft")
    print("2. Drücke den Link-Button auf dem Gateway")
    print("3. Versuche es erneut")
    print("4. Oder verwende die Phoscon-Weboberfläche")
    
    return None

def main():
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = "192.168.178.76"
    
    port = 4530
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    
    print("🚀 deCONZ API-Key Generator")
    print("=" * 40)
    
    api_key = get_api_key(host, port)
    
    if api_key:
        print(f"\n📋 Kopiere diesen API-Key in dein Migration Tool:")
        print(f"   {api_key}")
    else:
        print("\n❌ API-Key-Generierung fehlgeschlagen")
        sys.exit(1)

if __name__ == "__main__":
    main()
