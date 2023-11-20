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
response = requests.get(overpass_url, 
                        params={'data': overpass_query})

# Check for HTTP errors
response.raise_for_status()

# Parse the JSON response
data = response.json()

# Print the results or process them as you need
print(json.dumps(data, indent=4))

# Save the data to a file
with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)
