import requests
import json

# Overpass API URL
overpass_url = "http://overpass-api.de/api/interpreter"

# Your Overpass query
overpass_query = """
[out:json][timeout:100];
// gather results
(
  // query part for: “parking=surface”
  node["parking"="surface"](39.7042,-86.3994,39.9569,-86.0172);
  way["parking"="surface"](39.7042,-86.3994,39.9569,-86.0172);
  relation["parking"="surface"](39.7042,-86.3994,39.9569,-86.0172);
);
// print results
out body;
>;
out skel qt;
"""

# Send the request
overpass_response = requests.get(overpass_url, params={'data': overpass_query})

# Check for HTTP errors
overpass_response.raise_for_status()

# Parse the JSON response
data = overpass_response.json()

# Print the results or process them as you need
print(json.dumps(data, indent=4))

# Save the data to a file
with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)


# Method to process the Overpass API Query
def process_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Create a dictionary to map node IDs to their lat/lon
    node_dict = {}
    for element in data['elements']:
        if element['type'] == 'node':
            node_dict[element['id']] = (element['lat'], element['lon'])

    output_data = {}
    for element in data['elements']:
        if element['type'] == 'way':
            way_id = str(element['id'])
            node_ids = element['nodes']

            # Initialize min and max values
            min_lat = min_lon = float('inf')
            max_lat = max_lon = float('-inf')
            total_lat = total_lon = 0
            coordinate_list = []

            for node_id in node_ids:
                if node_id in node_dict:
                    lat, lon = node_dict[node_id]
                    min_lat = min(min_lat, lat)
                    max_lat = max(max_lat, lat)
                    min_lon = min(min_lon, lon)
                    max_lon = max(max_lon, lon)
                    total_lat += lat
                    total_lon += lon
                    coordinate_list.append(f"{lat},{lon}")

            center_lat = total_lat / len(node_ids)
            center_lon = total_lon / len(node_ids)
            coordinates = "_".join(coordinate_list)

            output_data[way_id] = {
                "min_lat": min_lat,
                "min_lon": min_lon,
                "max_lat": max_lat,
                "max_lon": max_lon,
                "center_point_lat": center_lat,
                "center_point_lon": center_lon,
                "coordinates": coordinates
            }

    return output_data

# Replace 'path_to_your_data.json' with the actual file path
processed_data = process_json('data.json')

# To print the processed data
print(json.dumps(processed_data, indent=4))

# To save the processed data to a new file
with open('coordinates.json', 'w') as file:
    json.dump(processed_data, file, indent=4)
