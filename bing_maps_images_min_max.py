import requests
import os
import json  # Import the json module to work with JSON files

# Define the base API URL
base_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/"

# Define the query parameters that are common to all requests
common_params = {
    "mapSize": "500,500",
    "mapLayer": "Basemap,Buildings",
    "key": "Ain7kUv28hvUkTkX5QfhVU-J_rqqtZMk7lGZNjh_e0ivB3wxcJsR3tAHJVAr8ZdC",
}

# Load the dataset of IDs and their corresponding coordinates from min_max_coords.json
with open("coordinates.json", "r") as json_file:
    coordinates_data = json.load(json_file)

# Create a directory to store the images
output_dir = "bing_maps_images_min_max"
os.makedirs(output_dir, exist_ok=True)

# Iterate through the dataset and make API requests
for id, coords in coordinates_data.items():
    # Define unique parameters for each request
    params = {
        **common_params,
        "mapArea": f"{coords['min_lat']},{coords['min_lon']},{coords['max_lat']},{coords['max_lon']}",
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check for a successful response
    if response.status_code == 200:
        # Save the image data to a file
        image_file = os.path.join(output_dir, f"image_{id}.jpg")
        with open(image_file, "wb") as file:
            file.write(response.content)
        print(f"Image for ID {id} saved as {image_file}")
    else:
        # Print an error message if the request was not successful
        print(f"HTTP request for ID {id} failed with status code: {response.status_code}")