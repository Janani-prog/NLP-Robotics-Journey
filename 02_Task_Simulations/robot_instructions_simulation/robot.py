import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import math
import time
from typing import Dict, List, Any
import random

class RobotSimulator:
    """A comprehensive 6-DOF robot arm simulator with visualization"""
    
    def __init__(self, num_joints=6):
        self.num_joints = num_joints
        # Initialize joint angles (in radians)
        self.joint_angles = np.zeros(num_joints)
        
        # Initialize TCP position (in mm)
        self.tcp_position = np.array([500.0, 0.0, 400.0])  # Default position
        
        # Link lengths for visualization (mm)
        self.link_lengths = [100, 200, 150, 100, 80, 50]
        
        # Command history
        self.command_history = []
        
        print("🤖 Robot Simulator Initialized")
        print(f"   - Number of joints: {self.num_joints}")
        print(f"   - Initial TCP position: {self.tcp_position}")
        print(f"   - Initial joint angles: {np.degrees(self.joint_angles)} degrees")
        print("-" * 50)
    
    def get_joint_values(self) -> Dict[str, Any]: #returns current position of the robot joints - where the robot is currently positioned
        """Get current joint values"""
        result = {
            "joint_angles_rad": self.joint_angles.tolist(),
            "joint_angles_deg": np.degrees(self.joint_angles).tolist(),
            "timestamp": time.time()
        }
        print("📊 Current Joint Values:")
        for i, (rad, deg) in enumerate(zip(result["joint_angles_rad"], result["joint_angles_deg"])):
            print(f"   Joint {i+1}: {rad:.4f} rad ({deg:.2f}°)")
        return result
    
    def get_tcp_position(self) -> Dict[str, Any]:
        """Get current TCP position"""
        result = {
            "x": float(self.tcp_position[0]),
            "y": float(self.tcp_position[1]),
            "z": float(self.tcp_position[2]),
            "timestamp": time.time()
        }
        print(f"📍 Current TCP Position: X={result['x']:.2f}mm, Y={result['y']:.2f}mm, Z={result['z']:.2f}mm")
        return result
    
    def move_joint(self, joint: List[int], angle: List[float]) -> Dict[str, Any]: #rotates specific joints by given angles
        """Move specific joints by given angles (in radians)"""
        print(f"🔄 Moving joints {[j+1 for j in joint]} by {[math.degrees(a) for a in angle]}°")
        
        for j, a in zip(joint, angle):
            if 0 <= j < self.num_joints:
                old_angle = self.joint_angles[j]
                self.joint_angles[j] += a  # Relative movement
                print(f"   Joint {j+1}: {math.degrees(old_angle):.2f}° → {math.degrees(self.joint_angles[j]):.2f}°")
            else:
                print(f"   ⚠️  Warning: Joint {j+1} out of range (1-{self.num_joints})")
        
        # Update TCP position based on forward kinematics (simplified)
        self._update_tcp_from_joints()
        
        return {"status": "success", "moved_joints": joint, "angles_applied": angle}
    
    def move_tcp(self, x: float = None, y: float = None, z: float = None) -> Dict[str, Any]:
        """Move TCP to absolute position or relative movement"""
        old_pos = self.tcp_position.copy()
        
        # If coordinates are provided, move to absolute position or relative
        if x is not None:
            if abs(x) < 50:  # Likely relative movement (small values)
                self.tcp_position[0] += x
                print(f"🎯 Moving TCP relatively: X += {x}mm")
            else:  # Absolute position
                self.tcp_position[0] = x
                print(f"🎯 Moving TCP to absolute position: X = {x}mm")
                
        if y is not None:
            if abs(y) < 50:
                self.tcp_position[1] += y
                print(f"🎯 Moving TCP relatively: Y += {y}mm")
            else:
                self.tcp_position[1] = y
                print(f"🎯 Moving TCP to absolute position: Y = {y}mm")
                
        if z is not None:
            if abs(z) < 50:
                self.tcp_position[2] += z
                print(f"🎯 Moving TCP relatively: Z += {z}mm")
            else:
                self.tcp_position[2] = z
                print(f"🎯 Moving TCP to absolute position: Z = {z}mm")
        
        print(f"   TCP moved from [{old_pos[0]:.1f}, {old_pos[1]:.1f}, {old_pos[2]:.1f}] to [{self.tcp_position[0]:.1f}, {self.tcp_position[1]:.1f}, {self.tcp_position[2]:.1f}]")
        
        # Update joint angles based on inverse kinematics (simplified)
        self._update_joints_from_tcp()
        
        return {"status": "success", "new_position": self.tcp_position.tolist()}
    
    def _update_tcp_from_joints(self):
        """Update TCP position based on joint angles (simplified forward kinematics)"""
        # Simplified calculation - in reality this would involve complex trigonometry
        x = sum(self.link_lengths[i] * math.cos(sum(self.joint_angles[:i+1])) for i in range(3))
        y = sum(self.link_lengths[i] * math.sin(sum(self.joint_angles[:i+1])) for i in range(3))
        z = self.tcp_position[2] + self.joint_angles[2] * 50  # Simplified Z calculation
        
        self.tcp_position = np.array([x, y, max(z, 0)])  # Ensure Z >= 0
    
    def _update_joints_from_tcp(self):
        """Update joint angles based on TCP position (simplified inverse kinematics)"""
        # This is a very simplified inverse kinematics - real robots use complex algorithms
        target_distance = np.linalg.norm(self.tcp_position[:2])
        
        if target_distance > 0:
            # Simple 2D inverse kinematics for first few joints
            self.joint_angles[0] = math.atan2(self.tcp_position[1], self.tcp_position[0])
            
            # Simplified joint calculations
            for i in range(1, min(3, self.num_joints)):
                self.joint_angles[i] = target_distance / (1000 * (i + 1))
    
    def execute_command(self, command: str) -> Any:
        """Execute a robot command from the dataset format"""
        print(f"\n💬 Command: '{command}'")
        self.command_history.append(command)
        
        try:
            # Parse the JSON command
            if isinstance(command, str):
                if command.startswith('['):
                    functions = json.loads(command)
                else:
                    # Handle single function format
                    functions = [json.loads(command)]
            else:
                functions = command
            
            results = []
            for func_call in functions:
                func_name = func_call["function"]
                kwargs = func_call["kwargs"]
                
                print(f"🔧 Executing: {func_name}({kwargs})")
                
                if func_name == "get_joint_values":
                    result = self.get_joint_values()
                elif func_name == "get_tcp_position":
                    result = self.get_tcp_position()
                elif func_name == "move_joint":
                    result = self.move_joint(kwargs["joint"], kwargs["angle"])
                elif func_name == "move_tcp":
                    result = self.move_tcp(**kwargs)
                else:
                    result = {"error": f"Unknown function: {func_name}"}
                    print(f"❌ Error: Unknown function {func_name}")
                
                results.append(result)
                time.sleep(0.1)  # Small delay for realism
            
            return results if len(results) > 1 else results[0]
            
        except Exception as e:
            error_msg = f"❌ Error executing command: {str(e)}"
            print(error_msg)
            return {"error": error_msg}
    
    def visualize_robot(self, figsize=(12, 8)):
        """Create a 3D visualization of the robot"""
        fig = plt.figure(figsize=figsize)
        
        # 3D robot arm plot
        ax1 = fig.add_subplot(121, projection='3d')
        
        # Calculate joint positions for visualization
        positions = np.zeros((self.num_joints + 1, 3))
        
        for i in range(self.num_joints):
            angle_sum = sum(self.joint_angles[:i+1])
            positions[i+1, 0] = positions[i, 0] + self.link_lengths[i] * math.cos(angle_sum)
            positions[i+1, 1] = positions[i, 1] + self.link_lengths[i] * math.sin(angle_sum)
            positions[i+1, 2] = positions[i, 2] + (i * 20)  # Add height variation
        
        # Plot robot arm
        ax1.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', linewidth=3, label='Robot Arm')
        ax1.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c='red', s=100, label='Joints')
        
        # Plot TCP position
        ax1.scatter(self.tcp_position[0], self.tcp_position[1], self.tcp_position[2], 
                   c='green', s=200, marker='*', label='TCP')
        
        ax1.set_xlabel('X (mm)')
        ax1.set_ylabel('Y (mm)')
        ax1.set_zlabel('Z (mm)')
        ax1.set_title('3D Robot Arm Visualization')
        ax1.legend()
        
        # Joint angles plot
        ax2 = fig.add_subplot(122)
        joint_names = [f'Joint {i+1}' for i in range(self.num_joints)]
        joint_angles_deg = np.degrees(self.joint_angles)
        
        bars = ax2.bar(joint_names, joint_angles_deg, color='skyblue', alpha=0.7)
        ax2.set_ylabel('Angle (degrees)')
        ax2.set_title('Current Joint Angles')
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, angle in zip(bars, joint_angles_deg):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{angle:.1f}°', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    def run_demo(self):
        """Run a demonstration with few-shot examples from the dataset"""
        print("🚀 Starting Robot Simulation Demo")
        print("=" * 60)
        
        # Few-shot examples from the dataset
        demo_examples = [
            {
                "input": "Provide me with the current joint angles of the robot.",
                "output": '[{"function": "get_joint_values", "kwargs": {}}]'
            },
            {
                "input": "Rotate joint 5 for 60 degrees",
                "output": '[{"function": "move_joint", "kwargs": {"joint": [4], "angle": [1.0471975511965976]}}]'
            },
            {
                "input": "Move robot TCP to position (0.5, 0.3, 0.7) meters",
                "output": '[{"function": "move_tcp", "kwargs": {"x": 500.0, "y": 300.0, "z": 700.0}}]'
            },
            {
                "input": "Rotate robot base by 90 degrees and move TCP along x axis for 50 millimeters",
                "output": '[{"function": "move_joint", "kwargs": {"joint": [0], "angle": [1.5707963267948966]}}, {"function": "move_tcp", "kwargs": {"x": 50.0}}]'
            },
            {
                "input": "Get current robot TCP position",
                "output": '[{"function": "get_tcp_position", "kwargs": {}}]'
            }
        ]
        
        print("📚 Few-Shot Examples from Dataset:")
        print("-" * 40)
        
        for i, example in enumerate(demo_examples, 1):
            print(f"\n🔢 Example {i}:")
            print(f"Input: {example['input']}")
            print(f"Expected Output: {example['output']}")
            
            # Execute the command
            result = self.execute_command(example['output'])
            print(f"✅ Execution Result: {result}")
            
            # Small delay between commands
            time.sleep(1)
            print("-" * 40)
        
        print("\n🎯 Demo completed! Visualizing final robot state...")
        self.visualize_robot()
        
        return self.command_history

# Initialize and run the simulation
def main():
    """Main function to run the robot simulation"""
    print("🤖 Robot Instruction Dataset Simulation")
    print("=" * 60)
    
    # Create robot simulator
    robot = RobotSimulator(num_joints=6)
    
    # Run the demo with few-shot examples
    history = robot.run_demo()
    
    print(f"\n📋 Command History ({len(history)} commands executed):")
    for i, cmd in enumerate(history, 1):
        print(f"  {i}. {cmd}")
    
    print("\n🎉 Simulation Complete!")
    print("The robot has successfully executed all commands from the dataset examples.")
    
    return robot

if __name__ == "__main__":
    # Run the simulation
    robot_sim = main()
    
    # Additional interactive commands
    print("\n🔧 You can now interact with the robot:")
    print("robot_sim.get_joint_values()")
    print("robot_sim.get_tcp_position()")
    print("robot_sim.move_joint([0], [0.5])  # Move joint 1 by 0.5 radians")
    print("robot_sim.move_tcp(x=600, y=400, z=800)  # Move TCP to position")
    print("robot_sim.visualize_robot()  # Show current robot state")