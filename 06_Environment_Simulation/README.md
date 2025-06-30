# Task 6: Environment & Disaster Scenario Simulation

## Overview

This directory focuses on simulating complex disaster environments and robot-assisted response scenarios. It includes both Python-based and web-based tools for modeling, visualizing, and interacting with disaster events, environmental entities, and NLP-driven command processing.

## Key Components

- **sample.py**: Core Python script for modeling disaster scenarios, extracting entities from NLP commands, and visualizing environments in 3D. Includes classes for disaster types, entities, scenario building, and visualization.
- **disaster-simulator/**: Contains a web-based simulation (JavaScript/React) for interactive disaster scenario visualization. Main code is in `src/` and assets in `public/`.
- **vis/**: (Likely) contains additional visualization scripts or tools (see `src/`).
- **claude_simulation_link.txt**: Contains a link to an external, advanced simulation demo: [View Claude Simulation](https://claude.ai/public/artifacts/31083858-f3d5-4378-b14e-6fdc1bc6029a?fullscreen=false)
- **venv/**: Python virtual environment (can be ignored for usage).

## How to Use

### Python Environment Simulation
1. Ensure you have Python 3.x and required packages (`numpy`, `matplotlib`, etc.).
2. Run `sample.py` to explore disaster scenario modeling and visualization:
   ```bash
   python sample.py
   ```
   This will generate 3D visualizations of disaster environments and entity interactions.

### Web-Based Disaster Simulator
1. Navigate to `disaster-simulator/` and follow any setup instructions (see `package.json`).
2. Main code is in `src/`; open or build the project as per standard React/Vite workflow.

### External Simulation
- For an advanced, interactive demo, open the link in `claude_simulation_link.txt` or click here: [Claude Simulation Demo](https://claude.ai/public/artifacts/31083858-f3d5-4378-b14e-6fdc1bc6029a?fullscreen=false)

## Directory Structure

- `sample.py` — Python code for scenario/entity modeling and visualization.
- `disaster-simulator/` — Web-based disaster simulation (JS/React, see `src/`).
- `vis/` — Additional visualization scripts/tools.
- `claude_simulation_link.txt` — External simulation link.
- `venv/` — Python virtual environment (not needed for usage).

---
*This week's work demonstrates the integration of NLP, environment modeling, and interactive visualization for disaster robotics research.* 