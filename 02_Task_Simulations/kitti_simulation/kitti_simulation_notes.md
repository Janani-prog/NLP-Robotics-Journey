# KITTI Navigation Simulation: Implementation Details

## Objective
To simulate a robot's navigation decisions based on visual input, inspired by the KITTI dataset's autonomous driving context. This simulation demonstrates a "few-shot" approach to generating navigation instructions from detected objects.

## `kitti_simulation.py` Overview
The `kitti_simulation.py` script contains:
* `DetectedObject` and `NavigationInstruction` dataclasses for structured data.
* `SimpleObjectDetector`: A simplified class that simulates object detection (instead of running a full CNN). It uses predefined rules to "detect" objects like cars, pedestrians, traffic lights based on image dimensions or simulated presence.
* `RobotNavigator`: This class takes detected objects and applies a simple rule-based logic to generate navigation instructions (e.g., "slow_down" if a car is close, "turn_left" if an obstacle is on the right).
* `run_few_shot_simulation`: Orchestrates the simulation by processing a list of images and generating instructions.

## Few-Shot Logic Implemented
The `RobotNavigator.decide_action` method contains the core logic:
* **Traffic Light Handling:** If a red traffic light is detected, the robot stops.
* **Pedestrian Detection:** If a pedestrian is detected nearby, the robot slows down.
* **Car/Truck Detection:** If cars or trucks are detected, the robot assesses their position (left/right/center) to decide if it needs to slow down, turn, or proceed.
* **Default:** If no critical objects are detected, the robot proceeds.

## How it Works (Simplified)
1.  **Image Input:** The simulation takes a list of image file paths (e.g., `image1.jpg` from the `images/` folder).
2.  **Simulated Detection:** For each image, the `SimpleObjectDetector` "detects" objects and assigns them simulated bounding boxes and confidence scores. These detections are hardcoded or randomized for demonstration purposes.
3.  **Navigation Decision:** The `RobotNavigator` takes these simulated detections and applies its rule set to decide the next action (stop, slow_down, turn, proceed).
4.  **Output:** The simulation prints the detected objects and the determined navigation instruction for each image. It also displays the image with simulated bounding boxes.

## Code Snippets and Key Sections
### `SimpleObjectDetector.detect_objects`
```python
# ... (see kitti_simulation.py for full code)
        # Example: Simulate a car in image1.jpg, a pedestrian in image2.jpg
        if "image1.jpg" in os.path.basename(image_path) or "image1.jpeg" in os.path.basename(image_path):
            detected_objects.append(DetectedObject('car', 0.95, (100, 200, 300, 150), (250, 275)))
        elif "image2.jpg" in os.path.basename(image_path):
            detected_objects.append(DetectedObject('pedestrian', 0.85, (500, 300, 80, 180), (540, 390)))
# ...

# ... (see kitti_simulation.py for full code)
        if any(obj.class_name == 'traffic_light' and obj.center[1] < height / 2 and obj.bbox[2] > 50 for obj in detected_objects):
            return NavigationInstruction("stop", "Detected red traffic light", 0.99)
        
        for obj in detected_objects:
            if obj.class_name == 'pedestrian' and obj.bbox[2] > 100: # large bbox implies close
                return NavigationInstruction("slow_down", "Pedestrian detected close ahead", 0.9)
# ...