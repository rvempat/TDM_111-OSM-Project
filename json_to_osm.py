import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Load JSON data from your file
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

# Create the root OSM element
osm = ET.Element('osm', version=str(data['version']), generator=data['generator'])

# Loop through the 'elements' list and convert them to OSM XML elements
for element in data['elements']:
    if element['type'] == 'node':
        node = ET.SubElement(osm, 'node', id=str(element['id']), lat=str(element['lat']), lon=str(element['lon']))
    # You can handle other element types (e.g., 'way', 'relation') here if needed

# Create a prettified XML string
xml_str = minidom.parseString(ET.tostring(osm)).toprettyxml(indent="  ")

# Write the XML string to a file
with open('output.osm', 'w') as osm_file:
    osm_file.write(xml_str)

print("Conversion completed. Output saved as 'output.osm'.")