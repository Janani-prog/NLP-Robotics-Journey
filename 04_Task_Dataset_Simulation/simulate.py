import json

def load_disaster_data(file_path):
    """
    Loads the disaster scenarios from a JSON file.

    Args:
        file_path (str): The path to the nlp_disaster.json file.

    Returns:
        list: A list of dictionaries, where each dictionary is a command.
              Returns an empty list if the file is not found or is invalid.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.")
        return []

def simulate_command_processing(command_text, commands_data):
    """
    Simulates finding and processing a specific disaster response command.

    Args:
        command_text (str): The English-language command to simulate.
        commands_data (list): The list of loaded disaster command data.
    """
    # In a real NLP system, this would be a sophisticated matching model.
    # Here, we do a simple search for the exact English text.
    command = next((cmd for cmd in commands_data if cmd["english"] == command_text), None)

    if not command:
        print(f"--- \nCommand not found: '{command_text}'\n---")
        return

    print("="*50)
    print(f"▶️  Simulating Command: '{command['english']}'")
    print(f"🗣️  Tamil Translation: '{command['tamil']}'")
    print("-"*50)

    print(f"🔍 Intent Identified: {command['intent']}")

    print("\n📋 Extracted Parameters:")
    for key, value in command['parameters'].items():
        print(f"   - {key.replace('_', ' ').title()}: {value}")

    print("\n🚨 Safety & Confirmation:")
    # Use emojis for quick visual assessment
    safety_status = "🔴 CRITICAL" if command['safety_critical'] else "🟢 NON-CRITICAL"
    confirm_status = "❗ REQUIRED" if command['confirmation_required'] else "✅ NOT REQUIRED"

    print(f"   - Safety Status: {safety_status}")
    print(f"   - User Confirmation: {confirm_status}")
    print("="*50 + "\n")


if __name__ == "__main__":
    # Load the disaster data from the JSON file
    file_name = 'nlp_disaster.json'
    disaster_commands = load_disaster_data(file_name)

    if disaster_commands:
        # --- SIMULATION ---
        # You can change the text below to simulate any command from your file.

        # Example 1: A safety-critical command that requires confirmation.
        command_to_simulate_1 = "Use thermal sensors to locate survivors in the collapsed apartment near Gandhi Nagar."
        simulate_command_processing(command_to_simulate_1, disaster_commands)

        # Example 2: A non-critical command.
        command_to_simulate_2 = "Airdrop 50 survival kits to coordinates 13.0827°N, 80.2707°E with high priority."
        simulate_command_processing(command_to_simulate_2, disaster_commands)

        # Example 3: A command involving technology to clear a route.
        command_to_simulate_3 = "Clear derailed coaches from Chennai Central to Tambaram rail line within 6 hours."
        simulate_command_processing(command_to_simulate_3, disaster_commands)

        # Example 4: A command for deploying robotic equipment.
        command_to_simulate_4 = "Deploy fire-resistant robots to extinguish lithium battery fire at electronics factory in Sriperumbudur."
        simulate_command_processing(command_to_simulate_4, disaster_commands)