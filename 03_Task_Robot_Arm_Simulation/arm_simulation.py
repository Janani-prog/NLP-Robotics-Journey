#!/usr/bin/env python3
"""
Working Robot Simulation with PyBullet
This script creates a functional robot simulation that executes movement instructions.
"""

import pybullet as p
import pybullet_data
import time
import json
import math
import numpy as np
import os

# Sample robot instructions that work with any robot configuration
SAMPLE_INSTRUCTIONS = [
    {
        "instruction": "Move to home position",
        "actions": [{"function": "move_joints", "joints": [0, 1, 2], "targets": [0, -30, 60]}]
    },
    {
        "instruction": "Raise first joint",
        "actions": [{"function": "move_joints", "joints": [0], "targets": [45]}]
    },
    {
        "instruction": "Lower second joint",
        "actions": [{"function": "move_joints", "joints": [1], "targets": [-60]}]
    },
    {
        "instruction": "Bend elbow",
        "actions": [{"function": "move_joints", "joints": [2], "targets": [90]}]
    },
    {
        "instruction": "Move end effector forward",
        "actions": [{"function": "move_tcp", "position": [0.4, 0.0, 0.6]}]
    },
    {
        "instruction": "Move end effector to side",
        "actions": [{"function": "move_tcp", "position": [0.2, 0.3, 0.5]}]
    },
    {
        "instruction": "Return to center",
        "actions": [{"function": "move_tcp", "position": [0.3, 0.0, 0.5]}]
    },
    {
        "instruction": "Wave motion",
        "actions": [
            {"function": "move_joints", "joints": [0], "targets": [30]},
            {"function": "move_joints", "joints": [0], "targets": [-30]},
            {"function": "move_joints", "joints": [0], "targets": [0]}
        ]
    }
]

class RobotSimulator:
    def __init__(self):
        self.physics_client = None
        self.robot_id = None
        self.controllable_joints = []
        self.joint_info = {}
        self.robot_type = None
        
    def setup_pybullet(self):
        """Initialize PyBullet with proper error handling."""
        print("🚀 Initializing PyBullet...")
        
        try:
            # Connect to PyBullet GUI
            self.physics_client = p.connect(p.GUI)
            if self.physics_client < 0:
                raise Exception("Failed to connect to PyBullet")
            
            # Set additional search path
            p.setAdditionalSearchPath(pybullet_data.getDataPath())
            
            # Configure physics
            p.setGravity(0, 0, -9.81)
            p.setTimeStep(1./240.)
            
            print("✓ PyBullet connected successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup PyBullet: {e}")
            return False
    
    def load_environment(self):
        """Load ground plane and environment."""
        try:
            # Load ground plane
            plane_id = p.loadURDF("plane.urdf")
            print("✓ Ground plane loaded")
            
            # Set camera position for better view
            p.resetDebugVisualizerCamera(
                cameraDistance=2.5,
                cameraYaw=45,
                cameraPitch=-30,
                cameraTargetPosition=[0, 0, 0.5]
            )
            
            return True
            
        except Exception as e:
            print(f"⚠ Warning loading environment: {e}")
            # Create simple ground manually
            try:
                ground_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[5, 5, 0.1])
                p.createMultiBody(0, ground_shape, basePosition=[0, 0, -0.1])
                print("✓ Simple ground created")
                return True
            except:
                print("❌ Failed to create ground")
                return False
    
    def load_robot(self):
        """Try to load a robot with multiple fallback options."""
        robot_options = [
            ("kuka_iiwa/model.urdf", "Kuka IIWA"),
            ("r2d2.urdf", "R2D2"),
            ("cartpole.urdf", "CartPole"),
            ("humanoid/nao.urdf", "NAO Humanoid")
        ]
        
        for urdf_path, robot_name in robot_options:
            try:
                print(f"🤖 Trying to load {robot_name}...")
                
                # Load robot at origin
                self.robot_id = p.loadURDF(
                    urdf_path,
                    basePosition=[0, 0, 0],
                    useFixedBase=True
                )
                
                self.robot_type = robot_name
                print(f"✓ Successfully loaded {robot_name}")
                break
                
            except Exception as e:
                print(f"⚠ Could not load {robot_name}: {e}")
                continue
        
        if self.robot_id is None:
            # Create a simple robot manually
            print("🔧 Creating simple custom robot...")
            self.robot_id = self.create_simple_robot()
            self.robot_type = "Custom Simple Robot"
        
        if self.robot_id is None:
            print("❌ Failed to load any robot")
            return False
        
        # Analyze robot joints
        self.analyze_robot_joints()
        return True
    
    def create_simple_robot(self):
        """Create a simple 3-DOF robot arm manually."""
        try:
            # Base
            base_shape = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.1, height=0.1)
            base_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.1, length=0.1, rgbaColor=[0.2, 0.2, 0.8, 1])
            
            # Links
            link_shape = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.05, height=0.3)
            link_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.05, length=0.3, rgbaColor=[0.8, 0.2, 0.2, 1])
            
            # Create multi-body
            link_masses = [1, 1, 1]
            link_collision_shapes = [link_shape, link_shape, link_shape]
            link_visual_shapes = [link_visual, link_visual, link_visual]
            link_positions = [[0, 0, 0.2], [0, 0, 0.3], [0, 0, 0.3]]
            link_orientations = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
            link_parent_indices = [0, 1, 2]
            link_joint_types = [p.JOINT_REVOLUTE, p.JOINT_REVOLUTE, p.JOINT_REVOLUTE]
            link_joint_axes = [[0, 0, 1], [1, 0, 0], [1, 0, 0]]
            
            robot_id = p.createMultiBody(
                baseMass=2,
                baseCollisionShapeIndex=base_shape,
                baseVisualShapeIndex=base_visual,
                basePosition=[0, 0, 0.05],
                linkMasses=link_masses,
                linkCollisionShapeIndices=link_collision_shapes,
                linkVisualShapeIndices=link_visual_shapes,
                linkPositions=link_positions,
                linkOrientations=link_orientations,
                linkInertialFramePositions=[[0, 0, 0]] * 3,
                linkInertialFrameOrientations=[[0, 0, 0, 1]] * 3,
                linkParentIndices=link_parent_indices,
                linkJointTypes=link_joint_types,
                linkJointAxis=link_joint_axes
            )
            
            print("✓ Custom robot created successfully")
            return robot_id
            
        except Exception as e:
            print(f"❌ Failed to create custom robot: {e}")
            return None
    
    def analyze_robot_joints(self):
        """Analyze and catalog robot joints."""
        if self.robot_id is None:
            return
        
        num_joints = p.getNumJoints(self.robot_id)
        print(f"🔍 Analyzing robot: {num_joints} joints found")
        
        self.controllable_joints = []
        self.joint_info = {}
        
        for i in range(num_joints):
            joint_info = p.getJointInfo(self.robot_id, i)
            joint_name = joint_info[1].decode('utf-8')
            joint_type = joint_info[2]
            
            # Check if joint is controllable
            if joint_type in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]:
                self.controllable_joints.append(i)
                self.joint_info[joint_name] = {
                    'index': i,
                    'type': joint_type,
                    'limits': (joint_info[8], joint_info[9])  # lower, upper limits
                }
                
                print(f"  Joint {i}: {joint_name} ({'revolute' if joint_type == p.JOINT_REVOLUTE else 'prismatic'})")
        
        print(f"✓ Found {len(self.controllable_joints)} controllable joints")
    
    def move_joints(self, joint_indices, target_angles, duration=2.0):
        """Move specified joints to target angles smoothly."""
        if not joint_indices or not target_angles:
            return
        
        # Ensure we don't exceed available joints
        valid_moves = []
        for i, angle in zip(joint_indices, target_angles):
            if i < len(self.controllable_joints):
                joint_idx = self.controllable_joints[i]
                valid_moves.append((joint_idx, math.radians(angle)))
        
        if not valid_moves:
            print("⚠ No valid joints to move")
            return
        
        # Get current positions
        current_positions = []
        for joint_idx, _ in valid_moves:
            joint_state = p.getJointState(self.robot_id, joint_idx)
            current_positions.append(joint_state[0])
        
        # Smooth interpolation
        steps = int(duration * 60)  # 60 steps per second
        for step in range(steps):
            t = step / float(steps - 1) if steps > 1 else 1.0
            
            for (joint_idx, target_pos), current_pos in zip(valid_moves, current_positions):
                # Smooth interpolation
                interp_pos = current_pos + t * (target_pos - current_pos)
                
                p.setJointMotorControl2(
                    bodyIndex=self.robot_id,
                    jointIndex=joint_idx,
                    controlMode=p.POSITION_CONTROL,
                    targetPosition=interp_pos,
                    force=500,
                    maxVelocity=2.0
                )
            
            p.stepSimulation()
            time.sleep(1./60.)
    
    def move_tcp(self, target_position, target_orientation=None, duration=2.0):
        """Move end effector to target position using inverse kinematics."""
        if len(self.controllable_joints) < 3:
            print("⚠ Need at least 3 DOF for TCP control")
            return
        
        try:
            # Use the last joint as end effector
            end_effector_link = len(self.controllable_joints) - 1
            
            if target_orientation:
                target_orn_quat = p.getQuaternionFromEuler(target_orientation)
                joint_poses = p.calculateInverseKinematics(
                    self.robot_id,
                    end_effector_link,
                    target_position,
                    target_orn_quat
                )
            else:
                joint_poses = p.calculateInverseKinematics(
                    self.robot_id,
                    end_effector_link,
                    target_position
                )
            
            # Apply the joint poses smoothly
            current_positions = []
            for joint_idx in self.controllable_joints:
                joint_state = p.getJointState(self.robot_id, joint_idx)
                current_positions.append(joint_state[0])
            
            # Limit joint poses to available joints
            target_poses = joint_poses[:len(self.controllable_joints)]
            
            # Smooth interpolation
            steps = int(duration * 60)
            for step in range(steps):
                t = step / float(steps - 1) if steps > 1 else 1.0
                
                for i, (joint_idx, target_pos, current_pos) in enumerate(zip(
                    self.controllable_joints, target_poses, current_positions
                )):
                    interp_pos = current_pos + t * (target_pos - current_pos)
                    
                    p.setJointMotorControl2(
                        bodyIndex=self.robot_id,
                        jointIndex=joint_idx,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=interp_pos,
                        force=500
                    )
                
                p.stepSimulation()
                time.sleep(1./60.)
        
        except Exception as e:
            print(f"❌ TCP control failed: {e}")
    
    def execute_instruction(self, instruction_data):
        """Execute a robot instruction."""
        instruction = instruction_data["instruction"]
        actions = instruction_data["actions"]
        
        print(f"\n🎯 Executing: {instruction}")
        
        for action in actions:
            function = action["function"]
            
            if function == "move_joints":
                joints = action.get("joints", [])
                targets = action.get("targets", [])
                print(f"  Moving joints {joints} to {targets}°")
                self.move_joints(joints, targets)
                
            elif function == "move_tcp":
                position = action.get("position", [0.3, 0, 0.5])
                orientation = action.get("orientation", None)
                print(f"  Moving TCP to {position}")
                self.move_tcp(position, orientation)
            
            # Small pause between actions
            time.sleep(0.5)
    
    def get_current_joint_positions(self):
        """Get current joint positions in degrees."""
        positions = []
        for joint_idx in self.controllable_joints:
            joint_state = p.getJointState(self.robot_id, joint_idx)
            positions.append(math.degrees(joint_state[0]))
        return positions
    
    def run_simulation(self):
        """Main simulation loop."""
        print("🤖 Starting Robot Simulation")
        print("=" * 50)
        
        # Setup PyBullet
        if not self.setup_pybullet():
            return False
        
        # Load environment
        if not self.load_environment():
            return False
        
        # Load robot
        if not self.load_robot():
            return False
        
        print(f"\n✅ Simulation setup complete!")
        print(f"🤖 Robot: {self.robot_type}")
        print(f"🔧 Controllable joints: {len(self.controllable_joints)}")
        print(f"📍 Initial joint positions: {[f'{p:.1f}°' for p in self.get_current_joint_positions()]}")
        
        # Add GUI controls info
        print(f"\n{'='*50}")
        print("CONTROLS:")
        print("- Mouse: Rotate camera view")
        print("- Mouse wheel: Zoom in/out")
        print("- ESC or close window: Exit simulation")
        print("- Watch robot execute instructions automatically")
        print(f"{'='*50}")
        
        # Execute instructions
        try:
            for i, instruction in enumerate(SAMPLE_INSTRUCTIONS):
                print(f"\n[Step {i+1}/{len(SAMPLE_INSTRUCTIONS)}]")
                self.execute_instruction(instruction)
                
                # Show current joint positions
                current_pos = self.get_current_joint_positions()
                print(f"  Current joint positions: {[f'{p:.1f}°' for p in current_pos]}")
                
                # Check if simulation window is still open
                try:
                    p.getConnectionInfo()
                except:
                    print("Simulation window closed by user")
                    return True
                
                # Pause between instructions
                time.sleep(1.0)
            
            print(f"\n🎉 All instructions completed successfully!")
            print("Close the window or press ESC to exit...")
            
            # Keep simulation running
            try:
                while True:
                    p.stepSimulation()
                    time.sleep(1./60.)
                    
                    # Check if window is still open
                    keys = p.getKeyboardEvents()
                    if p.B3G_ESCAPE in keys and keys[p.B3G_ESCAPE] & p.KEY_WAS_TRIGGERED:
                        break
                        
            except KeyboardInterrupt:
                print("\nSimulation interrupted by user")
            except:
                print("\nSimulation window closed")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during simulation: {e}")
            return False
        
        finally:
            try:
                p.disconnect()
                print("🔌 Disconnected from PyBullet")
            except:
                pass

def main():
    """Main entry point."""
    # Check PyBullet installation
    try:
        import pybullet
        import pybullet_data
        print(f"✓ PyBullet installed (data path: {pybullet_data.getDataPath()})")
    except ImportError:
        print("❌ PyBullet not found. Install with: pip install pybullet")
        return False
    
    # Create and run simulation
    simulator = RobotSimulator()
    success = simulator.run_simulation()
    
    if success:
        print("\n✅ Simulation completed successfully!")
    else:
        print("\n❌ Simulation failed")
    
    return success

if __name__ == "__main__":
    main()