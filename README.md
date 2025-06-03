# Summer NLP for Robotics Internship: Language-to-Robot Interface Development

## Overview
This repository documents my summer internship journey under the guidance of Professor [Professor's Name] from NIT Trichy. The internship focuses on developing Natural Language Processing (NLP) capabilities for robotics, progressing through distinct phases from dataset analysis to practical robot command execution.

## Internship Phases & Progress

### 🎯 Task 1: Dataset Exploration & Analysis (Completed)
* **Objective:** To conduct a deep, content-level exploration of existing robotics and robot instruction datasets. This involved understanding data modalities, annotation structures, and identifying opportunities for NLP integration in robotics.
* **Deliverable:** A comprehensive presentation outlining findings and insights from the dataset analysis.
* **Location:** See `01_Task_Dataset_Analysis/` for the presentation and a summary of findings.

### 💻 Task 2: Basic Simulation Development (In Progress / Recently Completed)
* **Objective:** To implement basic simulations demonstrating the potential for language-to-robot mapping using few-shot examples from selected datasets (KITTI for navigation context and `milistu/robot-instructions` for direct command execution).
* **Deliverables:** Python codes for each simulation, along with detailed documentation of their logic and implementation.
* **Location:** All code and specific notes related to these simulations can be found in `02_Task_Simulations/`.

### 🤖 Task 3: Humanoid Robot Command Replication (Upcoming / In Progress)
* **Objective:** To replicate and adapt the robotic commands derived in previous tasks to control a humanoid robot. This phase will involve bridging the gap between simulated commands and actual robot actions.
* **Deliverables:** Code for humanoid robot control, demonstration of command execution, and documentation of challenges and solutions.
* **Location:** Progress on this task will be documented in `03_Task_Humanoid_Replication/`.

## Repository Structure
* `internship_log.md`: A chronological log of daily/weekly progress, thoughts, challenges, and insights throughout the internship.
* `01_Task_Dataset_Analysis/`: Contains the presentation (`.pptx`) and a summary (`.md`) from Task 1.
* `02_Task_Simulations/`: Holds all code, images, and documentation for the KITTI and Robot Instructions simulations from Task 2.
    * `kitti_simulation/`: For KITTI-related code and notes.
    * `robot_instructions_simulation/`: For robot instruction parsing and simulation code and notes.
* `03_Task_Humanoid_Replication/`: (Will be populated) For code and documentation related to Task 3.
* `requirements.txt`: Python package dependencies for all project tasks.

## How to Run the Simulations (from Task 2)
### Prerequisites
* Python 3.x
* Install required packages: `pip install -r requirements.txt`

### KITTI Navigation Simulation
1.  Navigate to the `02_Task_Simulations/kitti_simulation/` directory.
2.  Ensure the `images/` folder contains test images (e.g., `image1.jpg`, `image2.jpg`).
3.  Run the simulation:
    ```bash
    python kitti_simulation.py
    ```
    This will simulate object detection and navigation instructions based on the images.

### Robot Instruction Simulation
1.  Navigate to the `02_Task_Simulations/robot_instructions_simulation/` directory.
2.  Run the simulation:
    ```bash
    python robot.py
    ```
    This will simulate a robot arm executing a sequence of commands from the `milistu/robot-instructions` dataset examples.

## Datasets Explored (Relevant to Task 1 & 2)
* **`mint-lab/awesome-robotics-datasets`**: A curated list of various robotics datasets for autonomous driving, flying, underwater, etc. (Link: [https://github.com/mint-lab/awesome-robotics-datasets](https://github.com/mint-lab/awesome-robotics-datasets))
* **`milistu/robot-instructions`**: A dataset focused on mapping natural language instructions to robot function calls. (Link: [https://huggingface.co/datasets/milistu/robot-instructions](https://huggingface.co/datasets/milistu/robot-instructions))

## Contact
* [Your Name]
* [Your Email]
* [Your LinkedIn Profile (Optional)]
