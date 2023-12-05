import requests
import json
import os

# Function to generate the URL based on coordinates
def generate_url(coords):
    base_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/"

    # Create a folder to store the images if it doesn't exist
    folder_name = "dataset/masks"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for way_id, way_data in coords.items():
        center_lat = way_data["center_point_lat"]
        center_lon = way_data["center_point_lon"]
        zoom = 19
        map_size = "500,500"
        coordinates = way_data["coordinates"]

        url = f"{base_url}{center_lat},{center_lon}/{zoom}"
        map_layer = "Basemap,Buildings"
        key = "Ain7kUv28hvUkTkX5QfhVU-J_rqqtZMk7lGZNjh_e0ivB3wxcJsR3tAHJVAr8ZdC"
        map_size_str = f"&mapSize={map_size}"
        dc = f"p,FFFF5064,FFFF5064,2;{coordinates}"

        full_url = f"{url}?mapLayer={map_layer}&key={key}{map_size_str}&dc={dc}"
        response = requests.get(full_url)

        if response.status_code == 200:
            # Save the image to the folder
            with open(f"{folder_name}/image_{way_id}.jpg", "wb") as file:
                file.write(response.content)
            print(f"Image for way {way_id} saved")
        else:
            print(f"Error querying for way {way_id}: {response.status_code}")

# Load coordinates from min_max_coords.json
with open("coordinates.json", "r") as coords_file:
    coordinates_data = json.load(coords_file)

# Generate URLs based on coordinates and save the images
generate_url(coordinates_data)
