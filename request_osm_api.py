import requests

# Define the API endpoint
osm_api_url = 'https://api.openstreetmap.org/api/0.6/map?bbox=-180,-90,180,90'

# Set up request headers (e.g., Authorization header for authenticated requests)
headers = {
    'Content-Type': 'application/xml',
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Only for authenticated requests
}

# Send a GET request to the API
response = requests.get(osm_api_url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the XML response (response.text) and process the data
    osm_data = response.text
    # You can parse the XML data as needed
    print(osm_data)
else:
    print(f'Error: {response.status_code} - {response.text}')
