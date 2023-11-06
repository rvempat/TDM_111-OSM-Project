import requests

# Define the API endpoint for uploading data
osm_api_url = 'https://api.openstreetmap.org/api/0.6/changeset/create'

# Set up request headers (e.g., Authorization header for authenticated requests)
headers = {
    'Content-Type': 'text/xml',
    'Authorization': 'Bearer ACCESS_TOKEN'  # Only for authenticated requests
}

# Read the OSM XML data from a file
with open('osm_data.xml', 'r') as xml_file:
    osm_data = xml_file.read()

# Send a POST request to upload the data
response = requests.post(osm_api_url, headers=headers, data=osm_data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Process the response (e.g., extract the new OSM elements created)
    new_osm_data = response.text
    print(new_osm_data)
else:
    print(f'Error: {response.status_code} - {response.text}')
