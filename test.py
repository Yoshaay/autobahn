import requests

# Basis-URL der API für Verkehrsmeldungen
BASE_URL = "https://verkehr.autobahn.de/o/autobahn/{}/services/warning"

# Liste der Autobahnen in Bayern
AUTOBAHNEN_IN_BAYERN = [
    "A3", "A6", "A7", "A8", "A9", "A70", "A72", "A73", "A93", "A96", "A99"
]

def get_traffic_description_for_autobahn(autobahn, api_key=None):
    url = BASE_URL.format(autobahn)
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Senden der GET-Anfrage mit optionalen Authentifizierungsheadern
    response = requests.get(url, headers=headers)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        try:
            data = response.json()
            # Durchsuchen der verschachtelten Struktur nach "description" und "abnormalTrafficType"
            descriptions = extract_descriptions(data)
            return descriptions
        except ValueError:
            print("Fehler: Die Antwort ist kein gültiges JSON.")
            return []
    else:
        # Fehlerbehandlung
        print(f"Fehler: {response.status_code}, Nachricht: {response.text}")
        return []

def extract_descriptions(data):
    descriptions = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "description" and isinstance(value, list):
                # Nimm alle Einträge ab der 5. Zeile (Index 4)
                for desc in value[4:]:  # Slice ab Index 4 (5. Element)
                    abnormal_traffic = data.get("abnormalTrafficType")
                    descriptions.append((desc, abnormal_traffic))  # Tuple mit Beschreibung und abnormalTrafficType
            elif isinstance(value, (dict, list)):
                descriptions.extend(extract_descriptions(value))
    elif isinstance(data, list):
        for item in data:
            descriptions.extend(extract_descriptions(item))
    
    return descriptions

def get_traffic_descriptions_for_bavaria(api_key=None):
    all_descriptions = []
    for autobahn in AUTOBAHNEN_IN_BAYERN:
        descriptions = get_traffic_description_for_autobahn(autobahn, api_key)
        all_descriptions.extend(descriptions)
    return all_descriptions

if __name__ == "__main__":
    api_key = "YOUR_API_KEY"  # Ersetze dies durch deinen tatsächlichen API-Schlüssel, falls erforderlich
    descriptions = get_traffic_descriptions_for_bavaria(api_key)
    if descriptions:
        for description, abnormal_type in descriptions:
            print(description)  # Ausgabe der Beschreibung ohne "Beschreibung"
            if abnormal_type:
                print(f"Abnormaler Verkehrstyp: {abnormal_type}")
            print()  # Leerzeile für bessere Lesbarkeit
    else:
        print("Keine Daten erhalten.")
