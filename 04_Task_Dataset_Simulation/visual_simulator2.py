import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from datasets import load_dataset # New import for Hugging Face datasets
import numpy as np # New import, useful for handling NaN if needed, though not directly used for type conversion here.

def create_visual_simulation(disaster_json_path, output_html_path):
    """
    Creates an interactive HTML map visualizing disaster response commands
    from nlp_disaster.json and integrates robot instructions from Hugging Face.

    Args:
        disaster_json_path (str): The path to the nlp_disaster.json file.
        output_html_path (str): The path to save the output HTML map.
    """
    # --- Load nlp_disaster.json data ---
    try:
        with open(disaster_json_path, 'r', encoding='utf-8') as f:
            data_disaster = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{disaster_json_path}' was not found. Make sure it's in the same folder as the script.")
        return
    
    df_disaster = pd.DataFrame(data_disaster)

    # --- Geolocation for nlp_disaster.json ---
    # Manual mapping of known locations to coordinates for visualization.
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
        "coimbatore": [11.0168, 76.9558], "erode": [11.3410, 77.7172],
        "salem": [11.6643, 78.1460], "tuticorin": [8.7642, 78.1348],
        "kanyakumari": [8.0883, 77.5385], "pondicherry": [11.9416, 79.8083],
        "chittoor": [13.2162, 79.0970], "bangalore": [12.9716, 77.5946],
        "nellore": [14.4426, 79.9864], "kurnool": [15.8281, 78.0374],
        "tirupati": [13.6288, 79.4192], "visakhapatnam": [17.6868, 83.2185],
        "hyderabad": [17.3850, 78.4867], "kochi": [9.9312, 76.2673],
        "trivandrum": [8.5241, 76.9361], "puducherry": [11.9416, 79.8083],
        "chengalpattu": [12.6974, 79.9701], "krishnagiri": [12.5204, 78.2144],
        "tirunelveli": [8.7139, 77.7567]
    }

    df_disaster['coords'] = None
    for index, row in df_disaster.iterrows():
        coords = None
        # Try to extract coordinates directly from parameters if available and valid
        if 'coordinates' in row['parameters'] and isinstance(row['parameters']['coordinates'], str):
            try:
                # Remove non-numeric characters before splitting
                coord_str = row['parameters']['coordinates'].replace('°N', '').replace('°E', '').strip()
                if ',' in coord_str:
                    lat, lon = map(float, coord_str.split(','))
                    coords = [lat, lon]
            except ValueError:
                pass
        
        # If coordinates not found, try to map location names
        if coords is None:
            # Check 'english' command and 'parameters' values for known location names
            search_string = str(row['english']).lower() + " " + " ".join(map(str, row['parameters'].values())).lower()
            for loc_key, loc_coords in known_locations.items():
                if loc_key in search_string:
                    coords = loc_coords
                    break
        
        # Fallback to Chennai if no specific location is found
        if coords is None:
            coords = known_locations["chennai"] 

        df_disaster.at[index, 'coords'] = coords

    # --- Load and process milistu/robot-instructions dataset from Hugging Face ---
    print("Loading 'milistu/robot-instructions' dataset from Hugging Face...")
    try:
        robot_instructions_dataset = load_dataset("milistu/robot-instructions", split="train")
        df_robot = pd.DataFrame(robot_instructions_dataset)
        print(f"Loaded {len(df_robot)} robot instructions.")
    except Exception as e:
        print(f"Error loading Hugging Face dataset: {e}")
        print("Please ensure you have an active internet connection and the 'datasets' library is installed (`pip install datasets`).")
        return

    # Transform robot instructions to match nlp_disaster.json format
    # Assign a default location for robot instructions (e.g., a "robot lab" in Chennai)
    # This places all robot-specific instructions at a single, generic point on the map.
    robot_lab_coords = [13.0827, 80.2707] # Chennai coordinates as a generic "robot lab" location

    # Map 'input' to 'english' and set default/placeholder values for other fields
    df_robot_transformed = pd.DataFrame({
        'id': 'robot_' + df_robot.index.astype(str),
        'intent': 'robot_instruction', # Default intent for these commands
        'english': df_robot['input'], # The command text from Hugging Face dataset
        'tamil': '', # No Tamil equivalent in this dataset
        'parameters': df_robot['output'].apply(lambda x: {"function_calls": x} if isinstance(x, str) else {}), # Store 'output' as parameters
        'safety_critical': False, # Default to False, as this info is not in the dataset
        'confirmation_required': False, # Default to False, as this info is not in the dataset
        'coords': [robot_lab_coords] * len(df_robot) # Assign the default location for all robot instructions
    })
    
    # Combine the two dataframes
    # Ensure all required columns are present in both dataframes before concatenating
    common_cols = ['id', 'intent', 'english', 'tamil', 'parameters', 'safety_critical', 'confirmation_required', 'coords']
    
    df_disaster_final = df_disaster[common_cols]
    df_robot_final = df_robot_transformed[common_cols]

    combined_df = pd.concat([df_disaster_final, df_robot_final], ignore_index=True)

    # --- Map Visualization ---
    initial_map_center = known_locations["chennai"] # Center map on Chennai
    disaster_map = folium.Map(location=initial_map_center, zoom_start=8, tiles="CartoDB positron")
    marker_cluster = MarkerCluster().add_to(disaster_map)

    # Define icons based on intent, including a new one for 'robot_instruction'
    icon_map = {
        "search_survivors": {"icon": "compass", "prefix": "fa"}, # Original intent
        "deploy_supplies": {"icon": "truck", "prefix": "fa"}, # Original intent
        "structural_assessment": {"icon": "exclamation-triangle", "prefix": "fa"}, # Original intent
        "evacuation_route": {"icon": "ambulance", "prefix": "fa"}, # Original intent
        "medical_assistance": {"icon": "medkit", "prefix": "fa"}, # Original intent
        "food_distribution": {"icon": "cutlery", "prefix": "fa"}, # Original intent
        "bridge_repair": {"icon": "road", "prefix": "fa"}, # Original intent
        "power_restoration": {"icon": "bolt", "prefix": "fa"}, # Original intent
        "robot_instruction": {"icon": "robot", "prefix": "fa"}, # New icon for robot instructions
        "default": {"icon": "info-circle", "prefix": "fa"} # Default if no specific icon matches
    }

    for index, row in combined_df.iterrows():
        if row['coords'] is None:
            continue

        color = 'blue'
        icon_key = 'default'
        # Set marker color to red if safety_critical is true
        if row['safety_critical']:
            color = 'red'
        
        # Use intent to select icon
        if row['intent'] in icon_map:
            icon_key = row['intent']
        else:
            # Fallback to general categories or default icon for other intents
            if 'search' in row['intent']: icon_key = 'search_survivors'
            elif 'deploy' in row['intent']: icon_key = 'deploy_supplies'
            elif 'medical' in row['intent']: icon_key = 'medical_assistance'
            elif 'power' in row['intent']: icon_key = 'power_restoration'
            elif 'bridge' in row['intent']: icon_key = 'bridge_repair'
            elif 'food' in row['intent']: icon_key = 'food_distribution'
            elif 'robot' in row['intent']: icon_key = 'robot_instruction'


        # Create detailed popup HTML
        popup_html = f"<h4><b>Intent:</b> {row['intent']}</h4><hr>"
        popup_html += f"<b>Command:</b> {row['english']}<br><br>"
        
        if row['parameters']:
            popup_html += "<b><u>Parameters:</u></b><ul>"
            for p_key, p_val in row['parameters'].items():
                # Format parameters nicely, especially for complex structures like 'function_calls' from robot dataset
                if isinstance(p_val, list) or isinstance(p_val, dict):
                    popup_html += f"<li><b>{p_key.replace('_', ' ').title()}:</b> <pre style='white-space: pre-wrap; word-wrap: break-word;'>{json.dumps(p_val, indent=2)}</pre></li>"
                else:
                    popup_html += f"<li><b>{p_key.replace('_', ' ').title()}:</b> {p_val}</li>"
            popup_html += "</ul>"
        else:
            popup_html += "<b><u>Parameters:</u></b> None<br>"
        
        safety_status = "CRITICAL" if row['safety_critical'] else "Non-Critical"
        confirm_status = "REQUIRED" if row['confirmation_required'] else "Not Required"
        
        popup_html += f"<br><b>Safety:</b> <span style='color:{color};'>{safety_status}</span>"
        popup_html += f"<br><b>Confirmation:</b> {confirm_status}"

        # Increased width/height for better display of robot instruction parameters
        iframe = folium.IFrame(popup_html, width=400, height=300) 
        popup = folium.Popup(iframe, max_width=400)

        folium.Marker(
            location=row['coords'],
            popup=popup,
            tooltip=row['intent'],
            icon=folium.Icon(color=color, icon=icon_map[icon_key]['icon'], prefix=icon_map[icon_key]['prefix'])
        ).add_to(marker_cluster)

    disaster_map.save(output_html_path)
    print(f"✅ Combined robotic NLP simulation created successfully!")
    print(f"🌍 Open the file '{output_html_path}' in your web browser to view the interactive map.")

if __name__ == "__main__":
    # Call the function to create the combined simulation map
    # Make sure 'nlp_disaster.json' is in the same directory as this script.
    # Ensure you have installed: pip install datasets pandas folium
    create_visual_simulation(
        disaster_json_path='nlp_disaster.json',
        output_html_path='combined_robot_disaster_map.html'
    )