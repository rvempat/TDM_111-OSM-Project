import requests

# Define the API endpoints
osm_api_create_changeset_url = 'https://api.openstreetmap.org/api/0.6/changeset/create'
osm_api_upload_changes_url = 'https://api.openstreetmap.org/api/0.6/changeset/{}/upload'
osm_api_close_changeset_url = 'https://api.openstreetmap.org/api/0.6/changeset/{}/close'

# Set up request headers (e.g., Authorization header for authenticated requests)
headers = {
    'Content-Type': 'text/xml',
    'Authorization': 'Bearer ACCESS_TOKEN'  # Only for authenticated requests
}

# Define the XML data for creating a changeset
changeset_xml = '<osm><changeset><tag k="created_by" v="YourAppName"/></changeset></osm>'

# Send a POST request to create a changeset
create_changeset_response = requests.put(osm_api_create_changeset_url, headers=headers, data=changeset_xml)

# Check if the changeset creation was successful (status code 200)
if create_changeset_response.status_code == 200:
    changeset_id = create_changeset_response.text
    print(f'Changeset created with ID: {changeset_id}')

    # Define the XML data for adding a new node
    node_xml = '<osm><node changeset="{}" lat="LATITUDE" lon="LONGITUDE"><tag k="name" v="NewNode"/></node></osm>'.format(changeset_id)

    # Send a POST request to upload the changes
    upload_changes_response = requests.post(osm_api_upload_changes_url.format(changeset_id), headers=headers, data=node_xml)

    # Check if the changes upload was successful (status code 200)
    if upload_changes_response.status_code == 200:
        print('Changes uploaded successfully')

        # Send a PUT request to close the changeset
        close_changeset_response = requests.put(osm_api_close_changeset_url.format(changeset_id), headers=headers)

        # Check if the changeset closure was successful (status code 200)
        if close_changeset_response.status_code == 200:
            print('Changeset closed successfully')
        else:
            print(f'Error closing changeset: {close_changeset_response.status_code} - {close_changeset_response.text}')
    else:
        print(f'Error uploading changes: {upload_changes_response.status_code} - {upload_changes_response.text}')
else:
    print(f'Error creating changeset: {create_changeset_response.status_code} - {create_changeset_response.text}')


##     Replace YourAppName with the name of your application.
##     Replace ACCESS_TOKEN with your actual OSM API access token.
##     Replace LATITUDE and LONGITUDE with the coordinates of the location where you want to add a new node.
