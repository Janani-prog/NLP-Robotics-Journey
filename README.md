# Aura: A Bilingual AI for Disaster Response
### From Curiosity to Crisis Response: A Journey in Language, Robotics, and Visual Generation

In the critical moments following a disaster, communication is the lifeline. This project chronicles an ambitious summer internship, under the guidance of Professor S. Sangeetha (NIT Trichy), to bridge the gap between human language and robotic action in high-stakes environments. This repository is not just a collection of code; it's the story of transforming raw data and bold ideas into **Aura**, a bilingual (English & Tamil) AI system engineered for intelligent disaster response. Each folder marks a milestone, and every simulation is a step toward tangible, real-world impact.

---

## 🚀 The Journey: A Developmental Chronicle

Our path was structured as a multi-stage evolution, with each chapter building upon the last to create a comprehensive and intelligent system.

### **Chapter 1: Exploring the Unknown (01_Task_Dataset_Analysis)**
Every mission begins with reconnaissance. Our journey commenced with a deep dive into the complex landscape of robotics and disaster response datasets. This foundational analysis was crucial for understanding the terrain, identifying opportunities, and defining the strategic challenges that would guide our development.
- **Artifacts:** [Presentation, Summary, and Key Insights](01_Task_Dataset_Analysis/)

### **Chapter 2: Simulating the First Steps (02_Task_Simulations)**
With a solid analytical foundation, we forged the first link between language and robotic action. By leveraging the KITTI dataset for navigation and `milistu/robot-instructions` for command interpretation, we demonstrated that even foundational NLP models could effectively guide robotic agents in meaningful, task-oriented ways.
- **Artifacts:** [KITTI Navigation & Robot Instruction Simulations](02_Task_Simulations/)

### **Chapter 3: Giving Robots a Body (03_Task_Robot_Arm_Simulation)**
This phase gave our system a physical presence. We moved from abstract commands to tangible motion by developing code to control a simulated robot arm. This was a critical step in translating human language into the precise, tactile movements required for real-world intervention.
- **Artifacts:** [Robot Arm Simulation and Control Code](03_Task_Robot_Arm_Simulation/)

### **Chapter 4: Seeing the Bigger Picture (04_Task_Dataset_Simulation, 05_Task_Robot_Simulation & 06_Environment_Simulation)**
Effective disaster response demands context. To create a rich, virtual proving ground for our AI, we developed a multi-layered simulation environment, comprising:
- **Visual Disaster Maps:** Dynamic crisis scenarios to test strategic awareness ([04_Task_Dataset_Simulation/](04_Task_Dataset_Simulation/)).
- **Diverse Robot Simulations:** HTML-based visualizations of various robotic assets and their capabilities ([05_Task_Robot_Simulation/](05_Task_Robot_Simulation/)).
- **Interactive Environments:** Immersive, web-based simulators that allow for dynamic interaction within a disaster zone ([06_Environment_Simulation/](06_Environment_Simulation/)).

### **Chapter 5: Commanding the Swarm (07_Commands_Simulation)**
To scale our system from a single agent to a coordinated fleet, we designed a centralized command interface. This simulation allows an operator to issue high-level, natural language commands and observe as a swarm of robots executes the mission in concert, providing a powerful glimpse into future command-and-control systems.
- **Artifacts:** [Robotic Operations Command Center](07_Commands_Simulation/)

### **Chapter 6: The Language of Help—The Bilingual AI Core (08_NLP_Simulation & 09_Bilingual_Simulation)**
The pinnacle of our journey is **Aura**, a full-stack, bilingual AI for disaster response. This system integrates all previous work into a cohesive whole, allowing operators to issue commands in either **English or Tamil**. With robust intent recognition, entity extraction, and seamless Tamil-to-English command mapping, Aura interprets instructions, visualizes the operational plan, and simulates the response on an interactive map, making advanced robotic control both powerful and inclusive.
- **Artifacts:**
  - [English NLP Disaster Response Prototype](08_NLP_Simulation/)
  - [Aura: The Full Bilingual AI Disaster Response System](09_Bilingual_Simulation/)

---

## 🧭 Project Blueprint
- `01_Task_Dataset_Analysis/`: Dataset exploration, presentation, and summary.
- `02_Task_Simulations/`: KITTI navigation and robot instruction simulations.
- `03_Task_Robot_Arm_Simulation/`: Robot arm simulation and control.
- `04_Task_Dataset_Simulation/`: Visual disaster scenario maps and simulators.
- `05_Task_Robot_Simulation/`: HTML-based robot simulation scenarios.
- `06_Environment_Simulation/`: Web-based environment and disaster simulation.
- `07_Commands_Simulation/`: Robotic operations command center (HTML).
- `08_NLP_Simulation/`: English NLP disaster response prototype.
- `09_Bilingual_Simulation/`: Aura—Bilingual (English & Tamil) NLP disaster response system.
- `requirements.txt`: Python dependencies for all tasks.

---

## 🌐 Core Technologies & Datasets
- **Datasets:**
  - `mint-lab/awesome-robotics-datasets`: A curated list of robotics datasets for navigation, manipulation, and disaster scenarios.
  - `milistu/robot-instructions`: A dataset for mapping natural language to robot commands.
  - **Custom Datasets:** Bespoke command datasets developed for this project in both English and Tamil.
- **Technologies:** Python, Flask, scikit-learn, spaCy, Pandas, JavaScript, Leaflet.js, rapidfuzz, sentence-transformers, HTML/CSS.

---

## 🏁 Getting Started: Installation & Usage
- Each numbered folder is self-contained and includes a dedicated `README.md` with specific setup and usage instructions.
- For the final, complete system, please refer to the guide in `09_Bilingual_Simulation/aura_disaster_response_ai/README.md`.
- A global `requirements.txt` is provided. Most simulations require Python 3.x and the listed dependencies.

---

## 🙏 Acknowledgements
- This project was made possible by the invaluable guidance of **Professor S. Sangeetha, NIT Trichy.**
- Our work stands on the shoulders of giants in the open-source robotics and NLP communities.
- Fueled by curiosity, collaboration, and a steadfast vision for a safer, more resilient world.

---

**From data to action, from English to Tamil, from simulation to impact—this project is a testament to the power of language, code, and imagination in shaping the future of robotics.**