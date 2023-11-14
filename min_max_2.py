import json

# Function to update min_max_coords.json with node coordinates
def update_coords_json():
    # Load data from min_max_coords.json
    with open("min_max_coords.json", "r") as min_max_file:
        min_max_data = json.load(min_max_file)

    # Load data from data.json
    with open("data.json", "r") as data_file:
        data = json.load(data_file)

        for element in data["elements"]:
            if element["type"] == "way":
                way_id = str(element["id"])

                # Fetch the way's coordinates
                coordinates = []
                for node_id in element["nodes"]:
                    node_coords = next(
                        (
                            {"id": node["id"], "lat": node["lat"], "lon": node["lon"]}
                            for node in data["elements"]
                            if node["id"] == node_id
                        ),
                        None,
                    )
                    if node_coords:
                        coordinates.append((node_coords["lat"], node_coords["lon"]))

                # Format the coordinates as requested
                formatted_coords = "_".join([f"{lat},{lon}" for lat, lon in coordinates])

                # Update min_max_coords.json with the coordinates of this way
                if way_id in min_max_data:
                    min_max_data[way_id]["coordinates"] = formatted_coords

    # Write the updated data back to min_max_coords.json
    with open("min_max_coords.json", "w") as min_max_file:
        json.dump(min_max_data, min_max_file, indent=2)

# Call the function to update min_max_coords.json
update_coords_json()
