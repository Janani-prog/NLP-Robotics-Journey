# Week 3: Robot Arm Simulation with PyBullet

---

## Overview
This document summarizes the work completed for Week 3, which focused on developing and simulating a robot arm using the PyBullet physics engine. The primary objective was to create a functional simulation environment where a robot arm could execute predefined movement instructions, demonstrating both joint-level control and end-effector (TCP) manipulation through inverse kinematics.

## Key Components and Functionality
The simulation is built around the `arm_simulation.py` script, supported by `setup.py` for environment configuration and `run_simulation.py` for easy execution.

* **`arm_simulation.py` (Core Simulation Script)**
    * **PyBullet Integration**: Initializes the PyBullet GUI, sets up the physics environment (gravity, time steps), and manages the simulation loop.
    * **Environment & Robot Loading**:
        * Automatically loads a ground plane.
        * Attempts to load popular robot URDFs (e.g., Kuka IIWA, R2D2).
        * Includes a robust **fallback mechanism** to create a simple 3-DOF custom robot arm if no standard URDFs are found, ensuring the simulation runs on any system.
    * **Joint Control**: Identifies and catalogs controllable joints, allowing for precise angular control of individual or multiple joints (`move_joints`).
    * **End-Effector (TCP) Control**: Implements **inverse kinematics** (`move_tcp`) to command the robot's end-effector to reach specified 3D positions, abstracting complex joint calculations.
    * **Instruction Execution**: Processes a series of predefined `SAMPLE_INSTRUCTIONS` that demonstrate diverse movements, from simple joint rotations to intricate TCP paths (e.g., "Move end effector forward," "Wave motion").
    * **Smooth Interpolation**: All movements are smoothly interpolated over time, providing realistic and visually appealing motion.
    * **Real-time Feedback**: Provides continuous updates on current joint positions in the console.

* **`setup.py` (Environment Setup and Validation)**
    * **Dependency Management**: Checks Python version compatibility (Python 3.6+).
    * **Automated Installation**: Installs necessary Python packages like `pybullet` and `numpy` based on `requirements.txt`.
    * **PyBullet Health Check**: Verifies PyBullet's core functionality by attempting to connect to the physics client and load test URDFs.
    * **Script Generation**: Creates `run_simulation.py` for convenience.

* **`run_simulation.py` (Execution Helper)**
    * A simple wrapper to launch the `arm_simulation.py` script, simplifying the execution process.

* **`requirements.txt` (Dependencies List)**
    * Lists all required Python libraries, ensuring consistent setup across different environments.

## Simulation Features & Interactions
* **Dynamic 3D Visualization**: Observe the robot arm in motion within a PyBullet GUI window.
* **Camera Controls**:
    * **Mouse**: Rotate camera view.
    * **Mouse Wheel**: Zoom in/out.
* **Exit**: Press **ESC** or close the simulation window to exit.

## Getting Started

### 1. Install Requirements
Navigate to the project directory in your terminal and run the setup script. This will install all necessary dependencies and prepare your environment.

```bash
python setup.py