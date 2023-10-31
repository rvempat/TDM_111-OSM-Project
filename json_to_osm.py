import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Load JSON data from your file
with open('input.json', 'r') as json_file:
    data = json.load(json_file)

# Create the root OSM element
osm = ET.Element('osm', version="0.6", generator="Python script")

# Loop through your JSON data and convert it to OSM XML elements
for feature in data:
    if 'id' in feature:
        node = ET.SubElement(osm, 'node', id=str(feature['id']), lat=str(feature['lat']), lon=str(feature['lon']))
        for key, value in feature.items():
            if key not in ['id', 'lat', 'lon']:
                ET.SubElement(node, 'tag', k=key, v=value)
    elif 'from' in feature and 'to' in feature:
        way = ET.SubElement(osm, 'way')
        for key, value in feature.items():
            if key not in ['from', 'to']:
                ET.SubElement(way, 'tag', k=key, v=value)
        for node_id in feature['nodes']:
            ET.SubElement(way, 'nd', ref=str(node_id))

# Create a prettified XML string
xml_str = minidom.parseString(ET.tostring(osm)).toprettyxml(indent="  ")

# Write the XML string to a file
with open('output.osm', 'w') as osm_file:
    osm_file.write(xml_str)

print("Conversion completed. Output saved as 'output.osm'.")
