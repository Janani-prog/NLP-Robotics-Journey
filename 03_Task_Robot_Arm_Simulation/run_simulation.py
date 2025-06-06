#!/usr/bin/env python3
"""
Simple runner for the robot simulation.
"""

if __name__ == "__main__":
    try:
        from robot_sim_working import main
        main()
    except ImportError:
        print("Error: robot_sim_working.py not found!")
        print("Make sure the robot simulation script is in the same directory.")
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
    except Exception as e:
        print(f"Error running simulation: {e}")
