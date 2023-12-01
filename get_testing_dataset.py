import requests
import math
import os

# Ensure the folder exists
save_dir = 'E:/OSMTestingImages'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Define your bounding box and ground resolution
min_lat = 39.7416667
min_long = -86.1833333
max_lat = 39.7853
max_long = -86.1340
ground_resolution = 0.2986  # meters/pixel

# Convert ground resolution to delta in degrees for latitude and longitude
delta_lat = ground_resolution / 111111  # degrees per meter (approximate)
delta_long = delta_lat / math.cos(math.radians(min_lat))

# Calculate the number of squares within the bounding box
num_lat = int((max_lat - min_lat) / delta_lat)
num_long = int((max_long - min_long) / delta_long)

# API parameters
base_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/"
params = {
    "mapSize": "500,500",
    "mapLayer": "Basemap,Buildings",
    "key": "Your_BingMapsKey"  # Replace with your actual Bing Maps API key
}

# Function to retrieve and save the image
def get_image(bottom_left_lat, bottom_left_long, top_right_lat, top_right_long):
    # Define the bounding box for the current square
    map_area = f"{bottom_left_lat},{bottom_left_long},{top_right_lat},{top_right_long}"
    # Construct the API URL
    api_url = f"{base_url}{map_area}&mapSize={params['mapSize']}&mapLayer={params['mapLayer']}&key={params['key']}"
    response = requests.get(api_url)
    if response.status_code == 200:
        # Construct the file path
        image_filename = os.path.join(save_dir, f"image_{bottom_left_lat}_{bottom_left_long}_{top_right_lat}_{top_right_long}.jpeg")
        # Save the image
        with open(image_filename, 'wb') as image_file:
            image_file.write(response.content)
        print(f"Downloaded {image_filename}")
    else:
        print(f"Failed to download image at {bottom_left_lat}, {bottom_left_long}: {response.status_code}")

# Iterate over each square within the bounding box
for lat_step in range(num_lat + 1):
    for long_step in range(num_long + 1):
        # Calculate the latitude and longitude for the bottom left corner of the square
        bottom_left_lat = min_lat + (lat_step * delta_lat)
        bottom_left_long = min_long + (long_step * delta_long)
        
        # Calculate the latitude and longitude for the top right corner of the square
        top_right_lat = bottom_left_lat + delta_lat
        top_right_long = bottom_left_long + delta_long
        
        # Ensure that we do not exceed the max bounds
        top_right_lat = min(top_right_lat, max_lat)
        top_right_long = min(top_right_long, max_long)
        
        # Retrieve and save the image for the current square
        get_image(bottom_left_lat, bottom_left_long, top_right_lat, top_right_long)
