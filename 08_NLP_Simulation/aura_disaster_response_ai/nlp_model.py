import json
import torch
from sentence_transformers import SentenceTransformer, util

class DisasterNLP:
    def __init__(self):
        """
        Initializes the new NLP model using Sentence Transformers.
        This model finds the most semantically similar command from the dataset.
        """
        print("Initializing Sentence Transformer model (all-MiniLM-L6-v2)...")
        # This will download the model on the first run.
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded. Loading and pre-processing disaster data...")
        self.data = self._load_data()
        self.corpus_embeddings = self._precompute_embeddings()
        print("Corpus embeddings computed. NLP system is ready.")

    def _load_data(self):
        """Loads the full, enhanced JSON data directly from this script."""
        # FOR SIMPLICITY AND TO AVOID FILE ERRORS, THE ENTIRE JSON IS PASTED HERE.
        # In a larger project, this would be loaded from a file.
        json_data = """
        [
    {
      "id": "disaster_001", "intent": "search_survivors", "english": "Use thermal sensors to locate survivors in the collapsed apartment near Gandhi Nagar.", "parameters": {"sensor_type": "thermal", "landmark": "Gandhi Nagar", "structure_type": "apartment"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "drone", "environment": "rubble", "color": "#e94560"}
    },
    {
      "id": "disaster_002", "intent": "deploy_supplies", "english": "Airdrop 50 survival kits to coordinates 13.0827°N, 80.2707°E with high priority.", "parameters": {"quantity": 50, "supply_type": "survival kits", "coordinates": "13.0827°N, 80.2707°E", "priority": "high"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "deploy_supply", "icon": "drone"}
    },
    {
      "id": "disaster_003", "intent": "hazard_warning", "english": "Issue chemical leak alert within 500m radius of the damaged factory.", "parameters": {"hazard_type": "chemical leak", "radius": "500m", "landmark": "factory"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "containment", "icon": "truck", "environment": "industrial", "color": "#f5a623", "hazard_icon": "hazard"}
    },
    {
      "id": "disaster_004", "intent": "clear_path", "english": "Remove debris blocking Route NH48 between kilometer markers 120 and 125.", "parameters": {"obstacle_type": "debris", "route": "NH48"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "path_clearance", "icon": "excavator", "environment": "rubble", "path_type": "road"}
    },
    {
      "id": "disaster_005", "intent": "medical_assistance", "english": "Set up temporary medical camp at the flood relief center in Cuddalore.", "parameters": {"facility_type": "medical camp", "disaster_type": "flood", "location": "Cuddalore relief center"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "deploy_static", "icon": "truck", "environment": "flood", "deploy_icon": "medical"}
    },
    {
      "id": "disaster_006", "intent": "structural_assessment", "english": "Scan building at 25/7 Velachery Main Road for structural integrity using LiDAR.", "parameters": {"technology": "LiDAR", "address": "25/7 Velachery Main Road"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "drone", "environment": "urban", "color": "#00ddff"}
    },
    {
      "id": "disaster_007", "intent": "water_rescue", "english": "Deploy amphibious drones for water rescue operations in Marina Beach area.", "parameters": {"equipment": "amphibious drones", "location": "Marina Beach"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "sweep", "icon": "amphibious", "environment": "water", "color": "#e94560"}
    },
    {
      "id": "disaster_008", "intent": "fire_containment", "english": "Create firebreak perimeter 200m around burning oil depot in Ennore.", "parameters": {"measure": "firebreak", "radius": "200m", "location": "Ennore"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "containment", "icon": "fire_robot", "environment": "fire", "color": "#e94560", "hazard_icon": "fire"}
    },
    {
      "id": "disaster_009", "intent": "evacuation_route", "english": "Mark safe evacuation routes from Central Railway Station using LED beacons.", "parameters": {"technology": "LED beacons", "starting_point": "Central Railway Station"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "evacuation_route", "icon": "truck"}
    },
    {
      "id": "disaster_010", "intent": "communication_restore", "english": "Establish emergency mesh network in cyclone-affected Nagapattinam district.", "parameters": {"technology": "mesh network", "location": "Nagapattinam district"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "truck", "effect": "power_grid"}
    },
    {
      "id": "disaster_011", "intent": "chemical_neutralization", "english": "Disperse neutralizing agents for ammonia leak at 9.9252°N, 78.1198°E.", "parameters": {"chemical": "ammonia", "coordinates": "9.9252°N, 78.1198°E"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "decon_robot", "effect": "decontamination", "color": "#26e07f"}
    },
    {
      "id": "disaster_012", "intent": "power_restoration", "english": "Prioritize electricity restoration to Government General Hospital using mobile generators.", "parameters": {"facility": "Government General Hospital"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "deploy_static", "icon": "truck", "deploy_icon": "power"}
    },
    {
      "id": "disaster_013", "intent": "missing_persons", "english": "Cross-reference facial recognition data with survivor lists at all Chennai shelters.", "parameters": {"location": "all Chennai shelters"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "point_effect", "no_unit": true, "effect": "facial_recognition"}
    },
    {
      "id": "disaster_014", "intent": "drone_surveillance", "english": "Initiate 24/7 aerial surveillance of breached dam in Mettur with thermal imaging.", "parameters": {"location": "Mettur dam"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "drone", "environment": "water", "color": "#f5a623"}
    },
    {
      "id": "disaster_015", "intent": "water_purification", "english": "Deploy portable water purification units to tsunami-affected coastal villages.", "parameters": {"location": "coastal villages"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "deploy_static", "icon": "truck", "deploy_icon": "decon_robot", "environment": "water"}
    },
    {
      "id": "disaster_016", "intent": "bridge_inspection", "english": "Conduct ultrasonic testing on damaged Adyar bridge before allowing traffic.", "parameters": {"structure": "Adyar bridge"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "drone", "environment": "rubble", "color": "#00ddff"}
    },
    {
      "id": "disaster_017", "intent": "animal_rescue", "english": "Coordinate with forest department for wildlife rescue in flooded Mudumalai reserve.", "parameters": {"location": "Mudumalai reserve"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "deploy_static", "icon": "animal", "environment": "flood", "deploy_icon": "animal", "count": 3}
    },
    {
      "id": "disaster_018", "intent": "radiation_monitoring", "english": "Monitor radiation levels every 30 minutes at Kalpakkam nuclear plant perimeter.", "parameters": {"location": "Kalpakkam nuclear plant"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "point_effect", "icon": "decon_robot", "effect": "monitoring", "color": "#f5a623"}
    },
    {
      "id": "disaster_019", "intent": "landshed_warning", "english": "Activate landslide early warning system for Nilgiris district hillslopes.", "parameters": {"location": "Nilgiris district"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "no_unit": true, "effect": "broadcast", "color": "#f5a623"}
    },
    {
      "id": "disaster_020", "intent": "data_relay", "english": "Establish satellite data relay for relief operations in cutoff Andaman islands.", "parameters": {"location": "Andaman islands"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "truck", "effect": "power_grid"}
    },
    {
      "id": "disaster_021", "intent": "gas_leak_control", "english": "Seal gas pipeline valves in T.Nagar area after detecting methane concentrations above 500ppm.", "parameters": {"location": "T.Nagar"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "path_repair", "icon": "repair", "environment": "urban", "path_type": "pipeline"}
    },
    {
      "id": "disaster_022", "intent": "evacuation_assistance", "english": "Guide visually impaired residents via audio instructions to nearest shelter at 12.9716°N, 77.5946°E.", "parameters": {"coordinates": "12.9716°N, 77.5946°E"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "evacuation_route", "icon": "truck"}
    },
    {
      "id": "disaster_023", "intent": "structural_shoring", "english": "Install temporary supports for leaning building on GST Road near Tambaram.", "parameters": {"location": "GST Road, Tambaram"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "path_repair", "icon": "excavator", "environment": "rubble", "path_type": "building"}
    },
    {
      "id": "disaster_024", "intent": "medical_telemetry", "english": "Transmit vital signs of 15 critical patients from Kilpauk Medical College to central command.", "parameters": {"facility": "Kilpauk Medical College"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "data_flow", "no_unit": true}
    },
    {
      "id": "disaster_025", "intent": "contamination_zone", "english": "Mark 1km exclusion zone around radioactive spill site at Kalpakkam with automated beacons.", "parameters": {"radius": "1km", "location": "Kalpakkam"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "containment", "icon": "decon_robot", "color": "#e94560", "hazard_icon": "radiation"}
    },
    {
      "id": "disaster_026", "intent": "waterway_clearance", "english": "Clear submerged vehicles from Adyar river near Kotturpuram bridge using amphibious excavators.", "parameters": {"waterway": "Adyar river"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "path_clearance", "icon": "amphibious", "environment": "water", "path_type": "river"}
    },
    {
      "id": "disaster_027", "intent": "epidemic_prevention", "english": "Disinfect temporary shelters in Cuddalore district after flood waters recede.", "parameters": {"location": "Cuddalore district"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "decon_robot", "effect": "decontamination", "color": "#26e07f"}
    },
    {
      "id": "disaster_028", "intent": "power_grid_repair", "english": "Replace damaged transformers in Besant Nagar substation to restore power to 5km radius.", "parameters": {"facility": "Besant Nagar substation"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "point_effect", "icon": "truck", "effect": "power_grid"}
    },
    {
      "id": "disaster_029", "intent": "food_distribution", "english": "Coordinate drone deliveries of 2000 meal packets to marooned villages in Thanjavur district.", "parameters": {"location": "Thanjavur district"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "deploy_supply", "icon": "drone"}
    },
    {
      "id": "disaster_030", "intent": "bridge_collapse", "english": "Deploy sonar equipment to search for vehicles submerged under collapsed Hosur highway overpass.", "parameters": {"location": "Hosur highway"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "amphibious", "environment": "rubble_water", "color": "#00ddff"}
    },
    {
      "id": "disaster_031", "intent": "railway_clearance", "english": "Clear derailed coaches from Chennai Central to Tambaram rail line within 6 hours.", "parameters": {"route": "Chennai Central-Tambaram"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "path_clearance", "icon": "excavator", "environment": "derailment", "path_type": "rail"}
    },
    {
      "id": "disaster_032", "intent": "mudslide_rescue", "english": "Use ground-penetrating radar to locate survivors in Ooty mudslide area.", "parameters": {"location": "Ooty"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "crawler", "environment": "rubble", "color": "#e94560"}
    },
    {
      "id": "disaster_033", "intent": "communication_jammer", "english": "Activate emergency signal jammer at 11.0168°N, 76.9558°E to prevent detonation signals.", "parameters": {"coordinates": "11.0168°N, 76.9558°E"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "no_unit": true, "effect": "jammer"}
    },
    {
      "id": "disaster_034", "intent": "mobile_hospital", "english": "Set up robotic surgical unit at temporary field hospital in Vellore flood zone.", "parameters": {"location": "Vellore"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "deploy_static", "icon": "truck", "environment": "flood", "deploy_icon": "medical"}
    },
    {
      "id": "disaster_035", "intent": "chemical_identification", "english": "Analyze unknown chemical spill at Ambattur Industrial Estate using spectrometers.", "parameters": {"location": "Ambattur Industrial Estate"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "sweep", "icon": "decon_robot", "environment": "industrial", "color": "#f5a623"}
    },
    {
      "id": "disaster_036", "intent": "aerial_mapping", "english": "Generate 3D damage assessment maps of cyclone-hit Karaikal coast using drone swarm.", "parameters": {"location": "Karaikal coast"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "drone", "environment": "water", "color": "#00ddff"}
    },
    {
      "id": "disaster_037", "intent": "underground_search", "english": "Deploy snake robots to inspect collapsed metro tunnel near LIC building.", "parameters": {"landmark": "LIC building"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "snake_robot", "environment": "rubble", "effect": "tunnel_scan"}
    },
    {
      "id": "disaster_038", "intent": "water_sampling", "english": "Collect and analyze water samples every 2 hours from Cooum river for contamination.", "parameters": {"location": "Cooum river"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "sweep", "icon": "amphibious", "environment": "water", "color": "#26e07f"}
    },
    {
      "id": "disaster_039", "intent": "crowd_control", "english": "Deploy autonomous barriers to manage crowds at Anna Nagar relief material distribution center.", "parameters": {"location": "Anna Nagar"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "deploy_static", "icon": "truck", "deploy_icon": "barrier", "count": 5}
    },
    {
      "id": "disaster_040", "intent": "firefighting", "english": "Direct unmanned firefighting vehicles to chemical warehouse blaze in Manali.", "parameters": {"location": "Manali"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "point_effect", "icon": "fire_robot", "environment": "fire", "effect": "firefighting"}
    },
    {
      "id": "disaster_041", "intent": "debris_sorting", "english": "Use AI-powered robotic arms to separate recyclable materials from earthquake debris in Trichy.", "parameters": {"location": "Trichy"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "robot_arm", "environment": "rubble", "effect": "debris_sorting"}
    },
    {
      "id": "disaster_042", "intent": "radiation_decontamination", "english": "Begin robotic decontamination of 200m radius around leaked radiation source in Tarapur.", "parameters": {"location": "Tarapur"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "decon_robot", "effect": "decontamination", "color": "#26e07f"}
    },
    {
      "id": "disaster_043", "intent": "missing_children", "english": "Match lost children database with facial recognition scans at all Chennai railway stations.", "parameters": {"locations": "all Chennai railway stations"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "point_effect", "no_unit": true, "effect": "facial_recognition"}
    },
    {
      "id": "disaster_044", "intent": "sewer_inspection", "english": "Send waterproof drones to inspect damaged sewer lines in Mylapore area.", "parameters": {"location": "Mylapore"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "drone", "environment": "urban", "color": "#f5a623"}
    },
    {
      "id": "disaster_045", "intent": "tsunami_alert", "english": "Activate all coastal warning sirens from Mahabalipuram to Nagapattinam.", "parameters": {"coverage": "Mahabalipuram to Nagapattinam"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "point_effect", "no_unit": true, "effect": "broadcast", "color": "#e94560"}
    },
    {
      "id": "disaster_046", "intent": "livestock_rescue", "english": "Coordinate animal rescue teams for stranded cattle in Ramanathapuram flood plains.", "parameters": {"location": "Ramanathapuram"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "deploy_static", "icon": "animal", "environment": "flood", "deploy_icon": "animal", "count": 3}
    },
    {
      "id": "disaster_047", "intent": "power_line_repair", "english": "Deploy insulated robotic crews to repair high-voltage lines in Neyveli township.", "parameters": {"location": "Neyveli"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "path_repair", "icon": "repair", "path_type": "powerline"}
    },
    {
      "id": "disaster_048", "intent": "emergency_broadcast", "english": "Override local radio frequencies to broadcast evacuation instructions in Villupuram district.", "parameters": {"location": "Villupuram district"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "point_effect", "no_unit": true, "effect": "broadcast", "color": "#00ddff"}
    },
    {
      "id": "disaster_049", "intent": "temporary_shelter", "english": "Assemble 50 prefabricated shelters in open ground near Madurai Meenakshi Temple.", "parameters": {"location": "Madurai"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "deploy_static", "icon": "truck", "deploy_icon": "medical", "count": 5}
    },
    {
      "id": "disaster_050", "intent": "data_backup", "english": "Secure backup of hospital patient records from flood-threatened CMC Vellore servers.", "parameters": {"facility": "CMC Vellore"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "data_flow", "no_unit": true}
    },
    {
      "id": "disaster_051", "intent": "landslide_monitoring", "english": "Install real-time soil moisture sensors along Nilgiri Mountain roads to predict landslide risks.", "parameters": {"location": "Nilgiri Mountain roads"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "truck", "effect": "monitoring", "color": "#f5a623"}
    },
    {
      "id": "disaster_052", "intent": "factory_fire", "english": "Deploy fire-resistant robots to extinguish lithium battery fire at electronics factory in Sriperumbudur.", "parameters": {"location": "Sriperumbudur"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "point_effect", "icon": "fire_robot", "environment": "fire", "effect": "firefighting"}
    },
    {
      "id": "disaster_053", "intent": "gas_pipeline_repair", "english": "Use magnetic crawler robots to repair ruptured gas pipeline near Ennore Port.", "parameters": {"location": "near Ennore Port"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "path_repair", "icon": "crawler", "path_type": "pipeline"}
    },
    {
      "id": "disaster_054", "intent": "coastal_erosion", "english": "Monitor erosion patterns along Marina Beach using autonomous underwater drones.", "parameters": {"location": "Marina Beach"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "sweep", "icon": "amphibious", "environment": "water", "color": "#00ddff"}
    },
    {
      "id": "disaster_055", "intent": "tunnel_collapse", "english": "Send snake-arm robots through rubble to locate trapped workers in Chennai Metro tunnel collapse.", "parameters": {"location": "Chennai Metro"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "snake_robot", "environment": "rubble", "effect": "tunnel_scan"}
    },
    {
      "id": "disaster_056", "intent": "oil_spill", "english": "Deploy oil-absorbent drone skimmers to contain spill off Chennai coast near Thiruvanmiyur.", "parameters": {"location": "off Thiruvanmiyur coast"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "containment", "icon": "amphibious", "environment": "water", "color": "#8B4513", "hazard_icon": "hazard"}
    },
    {
      "id": "disaster_057", "intent": "dam_inspection", "english": "Conduct ultrasonic thickness testing on Mettur Dam spillway using climbing robots.", "parameters": {"structure": "Mettur Dam"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "crawler", "environment": "structure", "color": "#00ddff"}
    },
    {
      "id": "disaster_058", "intent": "chemical_neutralization", "english": "Mix and disperse neutralizing agents for sulfuric acid leak at Ranipet tannery.", "parameters": {"location": "Ranipet tannery"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "point_effect", "icon": "decon_robot", "effect": "decontamination", "color": "#26e07f"}
    },
    {
      "id": "disaster_059", "intent": "bridge_inspection", "english": "Deploy aerial drones with LiDAR to assess damage to Pamban Bridge after cyclone impact.", "parameters": {"structure": "Pamban Bridge"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "drone", "environment": "structure_water", "color": "#00ddff"}
    },
    {
      "id": "disaster_060", "intent": "underground_fire", "english": "Lower fire-suppression robots into manholes to control methane fire in T.Nagar sewers.", "parameters": {"location": "T.Nagar sewers"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "point_effect", "icon": "fire_robot", "environment": "urban", "effect": "firefighting"}
    },
    {
      "id": "disaster_061", "intent": "tsunami_debris", "english": "Clear marine debris from Nagapattinam fishing harbor using amphibious excavators.", "parameters": {"location": "Nagapattinam fishing harbor"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "path_clearance", "icon": "amphibious", "environment": "water", "path_type": "river"}
    },
    {
      "id": "disaster_062", "intent": "radiation_mapping", "english": "Create real-time radiation heatmap of Kalpakkam nuclear complex using sensor drones.", "parameters": {"location": "Kalpakkam nuclear complex"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "drone", "color": "#e94560"}
    },
    {
      "id": "disaster_063", "intent": "tunnel_ventilation", "english": "Activate emergency ventilation in Chennai Port tunnel after smoke detection.", "parameters": {"location": "Chennai Port tunnel"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "point_effect", "icon": "truck", "effect": "decontamination", "color": "#aaaaaa"}
    },
    {
      "id": "disaster_064", "intent": "flood_barrier", "english": "Deploy automatic flood barriers along Adyar river at Saidapet vulnerable points.", "parameters": {"location": "Adyar river, Saidapet"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "deploy_static", "icon": "truck", "deploy_icon": "barrier", "count": 5}
    },
    {
      "id": "disaster_065", "intent": "industrial_accident", "english": "Evacuate 500m radius around chemical plant explosion in Manali industrial area.", "parameters": {"evacuation_radius": "500m", "location": "Manali industrial area"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "containment", "icon": "default", "environment": "fire", "color": "#e94560", "hazard_icon": "hazard"}
    },
    {
      "id": "disaster_066", "intent": "power_grid_stabilization", "english": "Activate grid stabilization protocols for Chennai metro area during cyclone-induced outages.", "parameters": {"location": "Chennai metro area"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "no_unit": true, "effect": "power_grid"}
    },
    {
      "id": "disaster_067", "intent": "military_ammunition", "english": "Establish 2km exclusion zone around burning ammunition depot in Avadi.", "parameters": {"exclusion_zone": "2km", "location": "Avadi"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "containment", "icon": "default", "environment": "fire", "color": "#e94560", "hazard_icon": "ammunition"}
    },
    {
      "id": "disaster_068", "intent": "water_treatment", "english": "Deploy mobile water treatment plants to flood-affected areas of Cuddalore.", "parameters": {"location": "Cuddalore"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "deploy_static", "icon": "truck", "environment": "flood", "deploy_icon": "decon_robot"}
    },
    {
      "id": "disaster_069", "intent": "railway_track_repair", "english": "Use automated track-laying machines to restore Chennai-Villupuram rail line.", "parameters": {"route": "Chennai-Villupuram"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "path_repair", "icon": "excavator", "path_type": "rail"}
    },
    {
      "id": "disaster_070", "intent": "telemedicine", "english": "Establish satellite-linked telemedicine units in cutoff Nilgiris villages.", "parameters": {"location": "Nilgiris villages"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "deploy_static", "icon": "truck", "deploy_icon": "medical"}
    },
    {
      "id": "disaster_071", "intent": "forest_fire", "english": "Coordinate water-bombing drones to contain wildfire in Sathyamangalam Tiger Reserve.", "parameters": {"location": "Sathyamangalam Tiger Reserve"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "drone", "environment": "forest_fire", "effect": "water_bombing"}
    },
    {
      "id": "disaster_072", "intent": "gas_leak_detection", "english": "Scan residential areas of Ambattur for LPG leaks using mobile gas detectors.", "parameters": {"location": "Ambattur"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "sweep", "icon": "truck", "environment": "urban", "color": "#f5a623"}
    },
    {
      "id": "disaster_073", "intent": "bridge_repair", "english": "Initiate emergency repair of damaged pillars on Napier Bridge using robotic concrete printers.", "parameters": {"structure": "Napier Bridge"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "path_repair", "icon": "printer3d", "path_type": "building"}
    },
    {
      "id": "disaster_074", "intent": "water_rescue", "english": "Deploy amphibious rescue robots for flooded areas of Pattukkottai town.", "parameters": {"location": "Pattukkottai"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "sweep", "icon": "amphibious", "environment": "flood", "color": "#e94560"}
    },
    {
      "id": "disaster_075", "intent": "epidemic_control", "english": "Dispatch UV-disinfection robots to containment zones in Madurai during dengue outbreak.", "parameters": {"location": "Madurai"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "decon_robot", "effect": "decontamination", "color": "#9013FE"}
    },
    {
      "id": "disaster_076", "intent": "debris_removal", "english": "Clear earthquake debris from Rameswaram temple complex using robotic excavators.", "parameters": {"location": "Rameswaram"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "path_clearance", "icon": "excavator", "environment": "rubble", "path_type": "area"}
    },
    {
      "id": "disaster_077", "intent": "nuclear_emergency", "english": "Activate radiation-hardened robots for inspection at Kudankulam plant after seismic alert.", "parameters": {"facility": "Kudankulam"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "crawler", "color": "#e94560"}
    },
    {
      "id": "disaster_078", "intent": "mine_rescue", "english": "Send explosion-proof crawler robots to search for trapped miners in Neyveli lignite mines.", "parameters": {"location": "Neyveli"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "point_effect", "icon": "crawler", "environment": "rubble", "effect": "tunnel_scan"}
    },
    {
      "id": "disaster_079", "intent": "hospital_backup", "english": "Switch to backup power and oxygen systems at GH Chennai using automated failover.", "parameters": {"facility": "GH Chennai"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "no_unit": true, "effect": "power_grid"}
    },
    {
      "id": "disaster_080", "intent": "tsunami_evacuation", "english": "Activate all coastal warning systems and direct drones to guide evacuation along ECR.", "parameters": {"route": "East Coast Road (ECR)"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "evacuation_route", "icon": "drone"}
    },
    {
      "id": "disaster_081", "intent": "air_quality", "english": "Deploy mobile air quality monitoring stations across Chennai after industrial fire.", "parameters": {"location": "Chennai"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "truck", "effect": "monitoring", "count": 3}
    },
    {
      "id": "disaster_082", "intent": "train_derailment", "english": "Stabilize derailed coaches at Arakkonam junction using hydraulic lift systems.", "parameters": {"location": "Arakkonam junction"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "path_repair", "icon": "excavator", "environment": "derailment", "path_type": "building"}
    },
    {
      "id": "disaster_083", "intent": "water_supply", "english": "Restore drinking water supply to Tambaram by repairing broken pipelines with robotic welders.", "parameters": {"location": "Tambaram"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "path_repair", "icon": "repair", "path_type": "pipeline"}
    },
    {
      "id": "disaster_084", "intent": "building_demolition", "english": "Prepare unstable high-rise in T.Nagar for controlled demolition using explosive drones.", "parameters": {"location": "T.Nagar"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "drone", "environment": "rubble", "effect": "demolition"}
    },
    {
      "id": "disaster_085", "intent": "animal_tracking", "english": "Monitor displaced wildlife in Mudumalai forest using GPS-enabled drone surveillance.", "parameters": {"location": "Mudumalai forest"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "drone", "environment": "forest", "color": "#26e07f"}
    },
    {
      "id": "disaster_086", "intent": "port_closure", "english": "Secure Chennai Port cranes and activate storm moorings for ships ahead of cyclone landfall.", "parameters": {"facility": "Chennai Port"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "deploy_static", "icon": "truck", "deploy_icon": "barrier", "count": 3}
    },
    {
      "id": "disaster_087", "intent": "telecom_restoration", "english": "Deploy mobile cell towers to restore communication in cutoff Nagapattinam villages.", "parameters": {"location": "Nagapattinam villages"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "truck", "effect": "power_grid"}
    },
    {
      "id": "disaster_088", "intent": "school_safety", "english": "Inspect structural damage to 15 government schools in Coimbatore earthquake zone.", "parameters": {"location": "Coimbatore"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "drone", "environment": "urban", "color": "#f5a623"}
    },
    {
      "id": "disaster_089", "intent": "road_repair", "english": "Use 3D asphalt printers to repair damaged sections of GST Road between Chromepet and Tambaram.", "parameters": {"route": "GST Road"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "path_repair", "icon": "printer3d", "path_type": "road"}
    },
    {
      "id": "disaster_090", "intent": "evacuation_shelter", "english": "Set up 20 temporary shelters with sanitation facilities at Madurai Race Course grounds.", "parameters": {"location": "Madurai"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "deploy_static", "icon": "truck", "deploy_icon": "medical", "count": 5}
    },
    {
      "id": "disaster_091", "intent": "gas_storage", "english": "Transfer LPG from damaged storage tanks in Korukkupet to secure facilities using robotic handlers.", "parameters": {"location": "Korukkupet"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "robot_arm", "effect": "containment", "hazard_icon": "hazard"}
    },
    {
      "id": "disaster_092", "intent": "sewage_overflow", "english": "Pump out flooded sewage systems in Mylapore using submersible robotic pumps.", "parameters": {"location": "Mylapore"}, "safety_critical": false, "confirmation_required": false,
      "visualization": {"type": "point_effect", "icon": "decon_robot", "environment": "flood", "effect": "decontamination", "color": "#8B4513"}
    },
    {
      "id": "disaster_093", "intent": "heritage_protection", "english": "Deploy moisture-absorbent drones to protect ancient murals in Thanjavur temple from flood damage.", "parameters": {"location": "Thanjavur temple"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "drone", "effect": "shield"}
    },
    {
      "id": "disaster_094", "intent": "power_line_inspection", "english": "Inspect 230kV transmission lines between Neyveli and Chennai using autonomous climbing robots.", "parameters": {"route": "Neyveli to Chennai"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "crawler", "color": "#00ddff"}
    },
    {
      "id": "disaster_095", "intent": "medical_evacuation", "english": "Prepare rooftop drone landing pads at GH Chennai for emergency medical evacuations.", "parameters": {"facility": "GH Chennai"}, "safety_critical": true, "confirmation_required": false,
      "visualization": {"type": "deploy_static", "icon": "drone", "deploy_icon": "medical"}
    },
    {
      "id": "disaster_096", "intent": "food_safety", "english": "Inspect flood-affected food warehouses in Trichy using contamination-detection robots.", "parameters": {"location": "Trichy"}, "safety_critical": false, "confirmation_required": true,
      "visualization": {"type": "sweep", "icon": "decon_robot", "environment": "flood", "color": "#f5a623"}
    },
    {
      "id": "disaster_097", "intent": "bridge_safety", "english": "Monitor vibration levels on new Poonamallee bypass bridge using IoT sensors.", "parameters": {"structure": "Poonamallee bypass bridge"}, "safety_critical": true, "confirmation_required": true,
      "visualization": {"type": "point_effect", "icon": "truck", "effect": "monitoring", "count": 3}
    }
]
        """
        return json.loads(json_data)

    def _precompute_embeddings(self):
        """Encodes all English commands into embeddings for fast similarity search."""
        corpus = [item['english'] for item in self.data]
        return self.model.encode(corpus, convert_to_tensor=True)

    def predict(self, query: str):
        """
        Finds the most similar command in the corpus to the user's query.
        """
        if not query.strip():
            return None

        # Encode the user's query
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        # Compute cosine-similarities
        cos_scores = util.cos_sim(query_embedding, self.corpus_embeddings)[0]

        # Find the index of the highest score
        best_match_idx = torch.argmax(cos_scores).item()

        # Return the entire JSON object for the best match
        best_match_command = self.data[best_match_idx]
        
        # Add the original query text to the response for clarity
        best_match_command['original_query'] = query
        
        return best_match_command