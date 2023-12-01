import requests
import math

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
    "key": "Ain7kUv28hvUkTkX5QfhVU-J_rqqtZMk7lGZNjh_e0ivB3wxcJsR3tAHJVAr8ZdC"  # Bing Maps API key
}

# Function to retrieve and save the image
def get_image(lat, long):
    # Define the bounding box for the current square
    map_area = f"{lat},{long},{lat-delta_lat},{long+delta_long}"
    # Construct the API URL
    api_url = f"{base_url}{map_area}&mapSize={params['mapSize']}&mapLayer={params['mapLayer']}&key={params['key']}"
    response = requests.get(api_url)
    if response.status_code == 200:
        # Save the image
        image_filename = f"image_{lat}_{long}.png"
        with open(image_filename, 'wb') as image_file:
            image_file.write(response.content)
        print(f"Downloaded {image_filename}")
    else:
        print(f"Failed to download image at {lat}, {long}: {response.status_code}")

# Iterate over each square within the bounding box
for i in range(num_lat + 1):
    for j in range(num_long + 1):
        # Calculate the latitude and longitude for the top-left corner of the square
        current_lat = max_lat - i * delta_lat
        current_long = min_long + j * delta_long
        # Retrieve and save the image for the current square
        get_image(current_lat, current_long)
