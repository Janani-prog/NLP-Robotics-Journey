import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster

def create_visual_simulation(json_path, output_html_path):
    """
    Creates an interactive HTML map visualizing disaster response commands.

    Args:
        json_path (str): The path to the nlp_disaster.json file.
        output_html_path (str): The path to save the output HTML map.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found. Make sure it's in the same folder as the script.")
        return
    
    df = pd.DataFrame(data)

    # --- Geolocation ---
    # We will manually map known locations to coordinates for a better visualization,
    # as not all entries have explicit lat/lon.
    known_locations = {
        "chennai": [13.0827, 80.2707], "gandhi nagar": [13.0068, 80.2520],
        "cuddalore": [11.7505, 79.7681], "velachery": [12.9786, 80.2212],
        "marina beach": [13.0511, 80.2825], "ennore": [13.2167, 80.3262],
        "central railway station": [13.0829, 80.2755], "nagapattinam": [10.7673, 79.8443],
        "kalpakkam": [12.5606, 80.1654], "mettur": [11.7865, 77.8016],
        "adyar": [13.0076, 80.2570], "mudumalai": [11.5959, 76.5413],
        "nilgiris": [11.3768, 76.7023], "andaman islands": [11.7401, 92.6586],
        "t.nagar": [13.0401, 80.2337], "tambaram": [12.9249, 80.1378],
        "kilpauk": [13.0785, 80.2346], "kotturpuram": [13.0185, 80.2458],
        "besant nagar": [13.0003, 80.2673], "thanjavur": [10.7870, 79.1378],
        "hosur": [12.7409, 77.8253], "ooty": [11.4102, 76.6950],
        "vellore": [12.9165, 79.1325], "ambattur": [13.1143, 80.1548],
        "karaikal": [10.9254, 79.8378], "trichy": [10.7905, 78.7047],
        "tarapur": [19.8322, 72.6525], "mylapore": [13.0339, 80.2694],
        "mahabalipuram": [12.6268, 80.1929], "ramanathapuram": [9.3636, 78.8357],
        "neyveli": [11.5428, 79.4851], "villupuram": [11.9390, 79.4947],
        "madurai": [9.9252, 78.1198], "korukkupet": [13.1189, 80.2900],
        "pamban": [9.2876, 79.2292], "saidapet": [13.0210, 80.2299],
        "manali": [13.1645, 80.2604], "avadi": [13.1094, 80.1037],
        "arakkonam": [13.0763, 79.6739], "poonamallee": [13.0583, 80.1110],
    }

    def get_coords(params):
        if 'coordinates' in params and isinstance(params['coordinates'], str):
            try:
                lat, lon = map(float, params['coordinates'].replace('°N', '').replace('°E', '').split(','))
                return [lat, lon]
            except:
                pass
        
        location_str = str(params.get('location', '')).lower()
        for name, coords in known_locations.items():
            if name in location_str:
                return coords
        return None

    df['coords'] = df['parameters'].apply(get_coords)
    df_mappable = df.dropna(subset=['coords']).copy()

    # --- Map Creation ---
    # Center the map on Tamil Nadu
    map_center = [11.0, 78.5]
    disaster_map = folium.Map(location=map_center, zoom_start=7, tiles="CartoDB positron")

    # Define icons based on intent
    icon_map = {
        'search': {'icon': 'search', 'prefix': 'fa'},
        'fire': {'icon': 'fire', 'prefix': 'fa'},
        'hazard': {'icon': 'warning', 'prefix': 'fa'},
        'leak': {'icon': 'tint', 'prefix': 'fa'},
        'rescue': {'icon': 'life-ring', 'prefix': 'fa'},
        'medical': {'icon': 'medkit', 'prefix': 'fa'},
        'power': {'icon': 'bolt', 'prefix': 'fa'},
        'bridge': {'icon': 'trello', 'prefix': 'fa'},
        'road': {'icon': 'road', 'prefix': 'fa'},
        'debris': {'icon': 'recycle', 'prefix': 'fa'},
        'supply': {'icon': 'truck', 'prefix': 'fa'},
        'communication': {'icon': 'signal', 'prefix': 'fa'},
        'default': {'icon': 'info-circle', 'prefix': 'fa'}
    }

    # Use Marker Clusters for better performance with many points
    marker_cluster = MarkerCluster().add_to(disaster_map)

    for idx, row in df_mappable.iterrows():
        # Choose color and icon
        color = 'red' if row['safety_critical'] else 'blue'
        
        icon_key = 'default'
        for key, val in icon_map.items():
            if key in row['intent']:
                icon_key = key
                break
        
        # Create detailed popup HTML
        popup_html = f"<h4><b>Intent:</b> {row['intent']}</h4><hr>"
        popup_html += f"<b>Command:</b> {row['english']}<br><br>"
        popup_html += "<b><u>Parameters:</u></b><ul>"
        for p_key, p_val in row['parameters'].items():
            popup_html += f"<li><b>{p_key.replace('_', ' ').title()}:</b> {p_val}</li>"
        popup_html += "</ul>"
        
        safety_status = "CRITICAL" if row['safety_critical'] else "Non-Critical"
        confirm_status = "REQUIRED" if row['confirmation_required'] else "Not Required"
        
        popup_html += f"<br><b>Safety:</b> <span style='color:{color};'>{safety_status}</span>"
        popup_html += f"<br><b>Confirmation:</b> {confirm_status}"

        iframe = folium.IFrame(popup_html, width=300, height=250)
        popup = folium.Popup(iframe, max_width=300)

        folium.Marker(
            location=row['coords'],
            popup=popup,
            tooltip=row['intent'],
            icon=folium.Icon(color=color, icon=icon_map[icon_key]['icon'], prefix=icon_map[icon_key]['prefix'])
        ).add_to(marker_cluster)

    disaster_map.save(output_html_path)
    print(f"✅ Visual simulation created successfully!")
    print(f"🌍 Open the file '{output_html_path}' in your web browser to view it.")

if __name__ == "__main__":
    create_visual_simulation(
        json_path='nlp_disaster.json', 
        output_html_path='disaster_map.html'
    )