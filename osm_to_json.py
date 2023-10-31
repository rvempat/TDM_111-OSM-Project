import requests
import json

overpass_url = "http://overpass-api.de/api/interpreter"

# Query for all surface parking lots in Indianapolis
overpass_query = (
    '[out:json];'
    '(way["parking"="surface"](39.7676,-86.1666,39.80339,-86.10255);'
    '  (._;>;);'
    ');'
    'out body;'
)

headers = {
    'Accept': 'application/json'  
}

try:
    response = requests.get(overpass_url, params={'data': overpass_query}, headers=headers)
    response.raise_for_status()

    data = response.json()
    output_json = json.dumps(data, indent=4)

    print(output_json)

    with open('data.json', 'w') as f:
        json.dump(output_json, f)

except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
