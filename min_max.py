import json

# Load the JSON data from your file
with open("data.json", "r") as json_file:
    data = json.load(json_file)

# Initialize a dictionary to store the minimum and maximum latitude and longitude for each "way"
way_min_max_coords = {}

# Iterate through the elements in the JSON data
for element in data["elements"]:
    if element["type"] == "way":
        way_id = element["id"]
        min_lat = float("inf")
        max_lat = float("-inf")
        min_lon = float("inf")
        max_lon = float("-inf")

        # Iterate through the nodes of the "way" to find the min/max coordinates
        for node_id in element["nodes"]:
            node = next((e for e in data["elements"] if e["type"] == "node" and e["id"] == node_id), None)
            if node:
                lat = node["lat"]
                lon = node["lon"]
                min_lat = min(min_lat, lat)
                max_lat = max(max_lat, lat)
                min_lon = min(min_lon, lon)
                max_lon = max(max_lon, lon)

        way_min_max_coords[way_id] = {
            "min_lat": min_lat,
            "min_lon": min_lon,
            "max_lat": max_lat,
            "max_lon": max_lon,
            "center_point_lat": (min_lat + max_lat) / 2,
            "center_point_lon": (min_lon + max_lon) / 2,
        }

# Save the minimum and maximum latitude and longitude data to a separate JSON file
with open("min_max_coords.json", "w") as output_file:
    json.dump(way_min_max_coords, output_file, indent=4)

print("Minimum and maximum coordinates saved to min_max_coords.json")
