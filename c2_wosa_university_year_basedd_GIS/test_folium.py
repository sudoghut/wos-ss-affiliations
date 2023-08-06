import folium

# Replace this with your actual coord_dic containing university coordinates
# For example: coord_dic = {'University1': (latitude1, longitude1), 'University2': (latitude2, longitude2), ...}
coord_dic = {
    'University1': (40.7128, -74.0060),
    'University2': (34.0522, -118.2437),
    'University3': (51.5074, -0.1278),
    # Add more universities as needed
}

# Create a map centered on a specific location (e.g., New York City)
map_center = (40.7128, -74.0060)
zoom_level = 4
map_object = folium.Map(location=map_center, zoom_start=zoom_level)

# Add markers for each university
for university, coords in coord_dic.items():
    latitude, longitude = coords
    folium.Marker(location=[latitude, longitude], popup=university).add_to(map_object)

# Save the map to an HTML file
map_object.save("university_map.html")
