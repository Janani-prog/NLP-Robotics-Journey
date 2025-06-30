import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import random

class DisasterType(Enum):
    EARTHQUAKE = "earthquake"
    FLOOD = "flood"
    FIRE = "fire"
    CHEMICAL = "chemical"
    CYCLONE = "cyclone"
    TSUNAMI = "tsunami"
    LANDSLIDE = "landslide"
    RADIATION = "radiation"

class EntityType(Enum):
    LOCATION = "location"
    EQUIPMENT = "equipment"
    HAZARD = "hazard"
    PERSONNEL = "personnel"
    VICTIM = "victim"
    STRUCTURE = "structure"

@dataclass
class EnvironmentEntity:
    name: str
    entity_type: EntityType
    position: Tuple[float, float, float]
    properties: Dict
    status: str = "active"

@dataclass
class DisasterScenario:
    scenario_id: str
    disaster_type: DisasterType
    location: str
    entities: List[EnvironmentEntity]
    parameters: Dict
    safety_level: int  # 1-5 scale

class NLPCommandProcessor:
    def __init__(self):
        self.location_patterns = {
            r'gandhi nagar|gandhi nagr': (13.0827, 80.2707, 0),
            r'velachery': (12.9752, 80.2212, 0),
            r'marina beach': (13.0478, 80.2773, 0),
            r'ennore': (13.2167, 80.3167, 0),
            r'central railway station': (13.0836, 80.2753, 0),
            r'nagapattinam': (10.7672, 79.8420, 0),
            r'cuddalore': (11.7480, 79.7714, 0),
            r'mettur': (11.7900, 77.8021, 0),
            r'adyar': (13.0067, 80.2206, 0),
            r'mudumalai': (11.5500, 76.5333, 500),
            r'kalpakkam': (12.5500, 80.1833, 0),
            r'nilgiris': (11.4916, 76.7337, 1000),
            r'andaman': (11.7401, 92.6586, 0),
            r'nh48': (13.1000, 80.2000, 0)  # Approximate highway position
        }
        
        self.equipment_mapping = {
            'thermal sensors': EntityType.EQUIPMENT,
            'survival kits': EntityType.EQUIPMENT,
            'amphibious drones': EntityType.EQUIPMENT,
            'led beacons': EntityType.EQUIPMENT,
            'mobile generators': EntityType.EQUIPMENT,
            'water purification units': EntityType.EQUIPMENT,
            'lidar': EntityType.EQUIPMENT,
            'mesh network': EntityType.EQUIPMENT
        }
        
        self.hazard_mapping = {
            'chemical leak': EntityType.HAZARD,
            'fire': EntityType.HAZARD,
            'debris': EntityType.HAZARD,
            'radiation': EntityType.HAZARD,
            'ammonia': EntityType.HAZARD,
            'burning oil depot': EntityType.HAZARD
        }

    def extract_coordinates(self, text: str) -> Optional[Tuple[float, float, float]]:
        """Extract GPS coordinates from text"""
        coord_pattern = r'(\d+\.\d+)°[NS],?\s*(\d+\.\d+)°[EW]'
        match = re.search(coord_pattern, text)
        if match:
            lat, lon = float(match.group(1)), float(match.group(2))
            return (lat, lon, 0)
        
        # Check for known locations
        text_lower = text.lower()
        for pattern, coords in self.location_patterns.items():
            if re.search(pattern, text_lower):
                return coords
        
        return None

    def extract_entities(self, command: Dict) -> List[EnvironmentEntity]:
        """Extract entities from disaster command"""
        entities = []
        english_text = command['english'].lower()
        parameters = command.get('parameters', {})
        
        # Extract location
        coords = self.extract_coordinates(english_text)
        if coords:
            location_entity = EnvironmentEntity(
                name=parameters.get('landmark', parameters.get('location', 'Unknown Location')),
                entity_type=EntityType.LOCATION,
                position=coords,
                properties={'type': 'primary_location'},
                status='active'
            )
            entities.append(location_entity)
        
        # Extract equipment
        for equipment, entity_type in self.equipment_mapping.items():
            if equipment in english_text:
                equipment_pos = coords if coords else (0, 0, 0)
                equipment_entity = EnvironmentEntity(
                    name=equipment,
                    entity_type=entity_type,
                    position=equipment_pos,
                    properties={'quantity': parameters.get('quantity', 1)},
                    status='deployed'
                )
                entities.append(equipment_entity)
        
        # Extract hazards
        for hazard, entity_type in self.hazard_mapping.items():
            if hazard in english_text:
                hazard_pos = coords if coords else (0, 0, 0)
                hazard_entity = EnvironmentEntity(
                    name=hazard,
                    entity_type=entity_type,
                    position=hazard_pos,
                    properties={'severity': 'high' if command.get('safety_critical') else 'medium'},
                    status='active'
                )
                entities.append(hazard_entity)
        
        return entities

    def determine_disaster_type(self, command: Dict) -> DisasterType:
        """Determine disaster type from command content"""
        english_text = command['english'].lower()
        
        if any(word in english_text for word in ['fire', 'burning', 'firebreak']):
            return DisasterType.FIRE
        elif any(word in english_text for word in ['flood', 'water rescue', 'amphibious']):
            return DisasterType.FLOOD
        elif any(word in english_text for word in ['chemical', 'ammonia', 'radiation']):
            return DisasterType.CHEMICAL
        elif any(word in english_text for word in ['cyclone', 'storm']):
            return DisasterType.CYCLONE
        elif any(word in english_text for word in ['tsunami', 'coastal']):
            return DisasterType.TSUNAMI
        elif any(word in english_text for word in ['landslide', 'hillslope']):
            return DisasterType.LANDSLIDE
        elif any(word in english_text for word in ['collapsed', 'debris', 'structural']):
            return DisasterType.EARTHQUAKE
        else:
            return DisasterType.EARTHQUAKE  # Default

class EnvironmentBuilder:
    def __init__(self):
        self.processor = NLPCommandProcessor()
        self.scenarios = {}
    
    def build_scenario(self, command: Dict) -> DisasterScenario:
        """Build disaster scenario from command"""
        entities = self.processor.extract_entities(command)
        disaster_type = self.processor.determine_disaster_type(command)
        safety_level = 5 if command.get('safety_critical') else 3
        
        scenario = DisasterScenario(
            scenario_id=command['id'],
            disaster_type=disaster_type,
            location=command.get('parameters', {}).get('location', 'Unknown'),
            entities=entities,
            parameters=command.get('parameters', {}),
            safety_level=safety_level
        )
        
        self.scenarios[command['id']] = scenario
        return scenario
    
    def add_environmental_context(self, scenario: DisasterScenario):
        """Add contextual entities based on disaster type"""
        base_coords = scenario.entities[0].position if scenario.entities else (0, 0, 0)
        
        # Add rescue personnel
        for i in range(random.randint(3, 8)):
            personnel_pos = (
                base_coords[0] + random.uniform(-0.01, 0.01),
                base_coords[1] + random.uniform(-0.01, 0.01),
                random.uniform(0, 10)
            )
            personnel = EnvironmentEntity(
                name=f"Rescue Team {i+1}",
                entity_type=EntityType.PERSONNEL,
                position=personnel_pos,
                properties={'role': 'first_responder', 'status': 'deployed'},
                status='active'
            )
            scenario.entities.append(personnel)
        
        # Add victims based on disaster type
        victim_count = random.randint(5, 15) if scenario.safety_level >= 4 else random.randint(1, 5)
        for i in range(victim_count):
            victim_pos = (
                base_coords[0] + random.uniform(-0.02, 0.02),
                base_coords[1] + random.uniform(-0.02, 0.02),
                random.uniform(-5, 5)
            )
            victim = EnvironmentEntity(
                name=f"Person {i+1}",
                entity_type=EntityType.VICTIM,
                position=victim_pos,
                properties={'status': random.choice(['rescued', 'trapped', 'injured'])},
                status='needs_help'
            )
            scenario.entities.append(victim)

class EnvironmentVisualizer:
    def __init__(self):
        self.colors = {
            EntityType.LOCATION: 'red',
            EntityType.EQUIPMENT: 'blue',
            EntityType.HAZARD: 'orange',
            EntityType.PERSONNEL: 'green',
            EntityType.VICTIM: 'purple',
            EntityType.STRUCTURE: 'brown'
        }
        
        self.markers = {
            EntityType.LOCATION: 'o',
            EntityType.EQUIPMENT: 's',
            EntityType.HAZARD: '^',
            EntityType.PERSONNEL: 'D',
            EntityType.VICTIM: 'v',
            EntityType.STRUCTURE: 'h'
        }
    
    def visualize_scenario(self, scenario: DisasterScenario):
        """Create 3D visualization of disaster scenario"""
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot entities by type
        for entity_type in EntityType:
            entities_of_type = [e for e in scenario.entities if e.entity_type == entity_type]
            if entities_of_type:
                x = [e.position[0] for e in entities_of_type]
                y = [e.position[1] for e in entities_of_type]
                z = [e.position[2] for e in entities_of_type]
                
                ax.scatter(x, y, z, 
                          c=self.colors[entity_type],
                          marker=self.markers[entity_type],
                          s=100,
                          label=entity_type.value.capitalize(),
                          alpha=0.7)
        
        # Add connections for operational relationships
        self._add_operational_connections(ax, scenario)
        
        # Styling
        ax.set_xlabel('Latitude')
        ax.set_ylabel('Longitude')
        ax.set_zlabel('Elevation (m)')
        ax.set_title(f'Disaster Response Environment: {scenario.scenario_id}\n'
                    f'Type: {scenario.disaster_type.value.capitalize()} | '
                    f'Safety Level: {scenario.safety_level}/5')
        ax.legend()
        
        # Add information panel
        self._add_info_panel(fig, scenario)
        
        plt.tight_layout()
        return fig
    
    def _add_operational_connections(self, ax, scenario: DisasterScenario):
        """Add lines showing operational relationships"""
        location_entities = [e for e in scenario.entities if e.entity_type == EntityType.LOCATION]
        equipment_entities = [e for e in scenario.entities if e.entity_type == EntityType.EQUIPMENT]
        
        # Connect equipment to primary location
        if location_entities and equipment_entities:
            primary_loc = location_entities[0]
            for equipment in equipment_entities:
                ax.plot([primary_loc.position[0], equipment.position[0]],
                       [primary_loc.position[1], equipment.position[1]],
                       [primary_loc.position[2], equipment.position[2]],
                       'k--', alpha=0.3, linewidth=1)
    
    def _add_info_panel(self, fig, scenario: DisasterScenario):
        """Add information panel to the visualization"""
        info_text = f"""
Scenario ID: {scenario.scenario_id}
Disaster Type: {scenario.disaster_type.value.capitalize()}
Location: {scenario.location}
Safety Level: {scenario.safety_level}/5
Total Entities: {len(scenario.entities)}

Entity Breakdown:
"""
        
        entity_counts = {}
        for entity in scenario.entities:
            entity_type = entity.entity_type.value
            entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
        
        for entity_type, count in entity_counts.items():
            info_text += f"- {entity_type.capitalize()}: {count}\n"
        
        fig.text(0.02, 0.98, info_text, transform=fig.transFigure, 
                fontsize=8, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

class DisasterResponseDemo:
    def __init__(self):
        self.builder = EnvironmentBuilder()
        self.visualizer = EnvironmentVisualizer()
    
    def run_demo(self, disaster_commands: List[Dict]):
        """Run complete demo with multiple disaster scenarios"""
        print("🚨 Disaster Response NLP Environment Builder Demo")
        print("=" * 60)
        
        scenarios = []
        for command in disaster_commands[:5]:  # Limit to first 5 for demo
            print(f"\n📋 Processing Command: {command['id']}")
            print(f"English: {command['english']}")
            print(f"Tamil: {command['tamil']}")
            
            # Build scenario
            scenario = self.builder.build_scenario(command)
            self.builder.add_environmental_context(scenario)
            scenarios.append(scenario)
            
            print(f"✅ Built scenario with {len(scenario.entities)} entities")
            print(f"   Disaster Type: {scenario.disaster_type.value}")
            print(f"   Safety Level: {scenario.safety_level}/5")
        
        # Create visualizations
        print(f"\n🎨 Creating visualizations for {len(scenarios)} scenarios...")
        
        for i, scenario in enumerate(scenarios):
            print(f"\nVisualizing scenario {i+1}: {scenario.scenario_id}")
            fig = self.visualizer.visualize_scenario(scenario)
            plt.show()
        
        return scenarios
    
    def analyze_command_patterns(self, commands: List[Dict]):
        """Analyze patterns in disaster commands"""
        print("\n📊 Command Pattern Analysis")
        print("-" * 40)
        
        intents = [cmd['intent'] for cmd in commands]
        safety_critical = [cmd.get('safety_critical', False) for cmd in commands]
        
        print(f"Total Commands: {len(commands)}")
        print(f"Safety Critical: {sum(safety_critical)}/{len(commands)}")
        print(f"Unique Intents: {len(set(intents))}")
        
        intent_counts = {}
        for intent in intents:
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        print("\nIntent Distribution:")
        for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {intent}: {count}")

# Demo execution
if __name__ == "__main__":
    # Sample disaster commands (you would load this from your JSON)
    sample_commands = [
        {
            "id": "disaster_001",
            "intent": "search_survivors",
            "english": "Use thermal sensors to locate survivors in the collapsed apartment near Gandhi Nagar.",
            "tamil": "காந்தி நகரில் உள்ள இடிந்த கட்டிடத்தில் வெப்ப கதிரியக்க சென்சார்களைப் பயன்படுத்தி உயிரோடு இருப்பவர்களை கண்டறியவும்.",
            "parameters": {
                "sensor_type": "thermal",
                "landmark": "Gandhi Nagar",
                "structure_type": "apartment"
            },
            "safety_critical": True,
            "confirmation_required": True
        },
        {
            "id": "disaster_002",
            "intent": "deploy_supplies",
            "english": "Airdrop 50 survival kits to coordinates 13.0827°N, 80.2707°E with high priority.",
            "tamil": "13.0827°N, 80.2707°E ஆயங்களுக்கு 50 உயிர்காப்பு கிடங்களை உயர் முன்னுரிமையுடன் விமானம் மூலம் வீசவும்.",
            "parameters": {
                "quantity": 50,
                "supply_type": "survival kits",
                "coordinates": "13.0827°N, 80.2707°E",
                "priority": "high"
            },
            "safety_critical": False,
            "confirmation_required": False
        },
        {
            "id": "disaster_007",
            "intent": "water_rescue",
            "english": "Deploy amphibious drones for water rescue operations in Marina Beach area.",
            "tamil": "மரீனா கடற்கரை பகுதியில் நீர் மீட்பு செயல்பாடுகளுக்கு நீர்நில விமானங்களை அனுப்பவும்.",
            "parameters": {
                "equipment": "amphibious drones",
                "operation": "water rescue",
                "location": "Marina Beach"
            },
            "safety_critical": True,
            "confirmation_required": False
        }
    ]
    
    # Run demo
    demo = DisasterResponseDemo()
    scenarios = demo.run_demo(sample_commands)
    demo.analyze_command_patterns(sample_commands)
    
    print("\n✨ Demo completed! The system has successfully:")
    print("  1. Parsed disaster response commands in English and Tamil")
    print("  2. Extracted entities and parameters using NLP")
    print("  3. Built dynamic 3D environments for each scenario")
    print("  4. Visualized disaster response operations")
    print("  5. Analyzed command patterns and safety criticality")