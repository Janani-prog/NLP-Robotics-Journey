# Task 6: Environment & Disaster Scenario Simulation

## Overview

This directory focuses on simulating complex disaster environments and robot-assisted response scenarios. It includes both Python-based and web-based tools for modeling, visualizing, and interacting with disaster events, environmental entities, and NLP-driven command processing.

## Key Components

- **sample.py**: Core Python script for modeling disaster scenarios, extracting entities from NLP commands, and visualizing environments in 3D. Includes classes for disaster types, entities, scenario building, and visualization.
- **disaster-simulator/**: Contains a web-based simulation (JavaScript/React) for interactive disaster scenario visualization. Main code is in `src/` and assets in `public/`.
- **vis/**: (Likely) contains additional visualization scripts or tools (see `src/`).
- **claude_simulation_link.txt**: Contains links to external, advanced simulation demos (see below).
- **venv/**: Python virtual environment (can be ignored for usage).

## Claude Simulation Artifacts

This project includes advanced, interactive simulations created with Anthropic's Claude Artifact platform. These artifacts demonstrate AI-powered scenario modeling, visualization, or educational tools relevant to disaster robotics and environment simulation.

- [Simulation Artifact 1](https://claude.ai/public/artifacts/31083858-f3d5-4378-b14e-6fdc1bc6029a?fullscreen=false): An interactive AI-powered simulation or visualization. Open in your browser to explore the scenario.
- [Simulation Artifact 2](https://claude.ai/public/artifacts/2dc87ca0-7cfc-4db9-b29b-ce2a97e9cd2c): Another interactive artifact, demonstrating a different scenario or tool. Open in your browser for details.

> **Note:** For the most accurate description, open each link and review the scenario or tool presented. These artifacts are best viewed in a modern browser and may require a Claude account for full interactivity.

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
- For an advanced, interactive demo, open the links above or see `claude_simulation_link.txt`.

## Directory Structure

- `sample.py` — Python code for scenario/entity modeling and visualization.
- `disaster-simulator/` — Web-based disaster simulation (JS/React, see `src/`).
- `vis/` — Additional visualization scripts/tools.
- `claude_simulation_link.txt` — External simulation links.
- `venv/` — Python virtual environment (not needed for usage).

---
*This week's work demonstrates the integration of NLP, environment modeling, and interactive visualization for disaster robotics research.* 