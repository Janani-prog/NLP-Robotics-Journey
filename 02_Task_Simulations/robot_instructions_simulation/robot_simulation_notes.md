# Robot Instruction Simulation: Implementation Details

## Objective
To simulate a 6-DOF (Degrees of Freedom) robot arm executing commands derived from natural language instructions, primarily using examples from the `milistu/robot-instructions` dataset. This demonstrates the "function call" aspect of NLP for robotics.

## `robot.py` Overview
The `robot.py` script implements a `RobotSimulator` class that:
* Initializes the robot's joint angles and TCP (Tool Center Point) position.
* Provides methods to control the robot:
    * `move_joint(joint_idx, angle_change)`: Changes a specific joint's angle.
    * `set_tcp_position(x, y, z)`: Attempts to move the robot's end effector to a target 3D position (simplified inverse kinematics).
    * `get_joint_values()`: Returns current joint angles.
    * `get_tcp_position()`: Returns current TCP position.
* `execute_command(command_json)`: Parses a dictionary (simulating a JSON object) that represents a robot function call and executes the corresponding internal method.
* `visualize_robot()`: Uses `matplotlib` to provide a simple 3D visualization of the robot arm.
* `run_demo()`: Orchestrates a few-shot demonstration by iterating through predefined example instructions and executing them.

## Few-Shot Examples Used
The `run_demo()` method uses a hardcoded list of examples that mirror the structure found in the `milistu/robot-instructions` dataset. Each example contains:
* `instruction`: The natural language phrase.
* `output`: The robot function call in a dictionary format.

**Example Snippet:**
```python
# ... (see robot.py for full code)
        few_shot_examples = [
            {"instruction": "Move joint 0 by 30 degrees.", "output": {"function_name": "move_joint", "args": [0, math.radians(30)]}},
            {"instruction": "Set the TCP position to (600, 100, 300) mm.", "output": {"function_name": "set_tcp_position", "args": [600, 100, 300]}},
            {"instruction": "Rotate joint 3 by -45 degrees.", "output": {"function_name": "move_joint", "args": [3, math.radians(-45)]}},
            {"instruction": "Bring the end effector to (550, -50, 450) mm.", "output": {"function_name": "set_tcp_position", "args": [550, -50, 450]}},
            {"instruction": "Move joint 5 by 15 degrees.", "output": {"function_name": "move_joint", "args": [5, math.radians(15)]}}
        ]
# ...