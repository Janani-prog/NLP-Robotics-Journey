#!/usr/bin/env python3
"""
Robot Simulation Setup and Requirements Checker
Run this script first to verify your environment is ready.
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(f"❌ Python 3.6+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_package(package_name, import_name=None, install_command=None):
    """Check if a package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        spec = importlib.util.find_spec(import_name)
        if spec is not None:
            print(f"✓ {package_name} is installed")
            return True
    except ImportError:
        pass
    
    print(f"❌ {package_name} is not installed")
    if install_command:
        print(f"   Install with: {install_command}")
    return False

def install_requirements():
    """Install required packages."""
    packages = [
        ("pybullet", "pip install pybullet"),
        ("numpy", "pip install numpy")
    ]
    
    missing_packages = []
    
    for package, install_cmd in packages:
        if not check_package(package):
            missing_packages.append((package, install_cmd))
    
    if missing_packages:
        print(f"\n📦 Missing packages detected. Installing...")
        for package, install_cmd in missing_packages:
            try:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False
    
    return True

def test_pybullet():
    """Test PyBullet functionality."""
    try:
        import pybullet as p
        import pybullet_data
        
        print("\n🧪 Testing PyBullet...")
        
        # Test connection
        physics_client = p.connect(p.DIRECT)  # Headless mode for testing
        if physics_client < 0:
            print("❌ Failed to connect to PyBullet")
            return False
        
        # Test data path
        data_path = pybullet_data.getDataPath()
        print(f"✓ PyBullet data path: {data_path}")
        
        # Test loading a simple URDF
        p.setAdditionalSearchPath(data_path)
        try:
            plane_id = p.loadURDF("plane.urdf")
            print("✓ Successfully loaded test URDF")
        except:
            print("⚠ Warning: Could not load test URDF (may affect robot loading)")
        
        # Test robot loading
        robot_loaded = False
        test_robots = ["kuka_iiwa/model.urdf", "r2d2.urdf", "cartpole.urdf"]
        
        for robot_urdf in test_robots:
            try:
                robot_id = p.loadURDF(robot_urdf)
                print(f"✓ Successfully loaded {robot_urdf}")
                robot_loaded = True
                break
            except:
                continue
        
        if not robot_loaded:
            print("⚠ No standard robots available, will use custom robot")
        
        p.disconnect()
        print("✓ PyBullet test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ PyBullet test failed: {e}")
        return False

def create_run_script():
    """Create a simple run script."""
    run_script = '''#!/usr/bin/env python3
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
        print("\\nSimulation stopped by user")
    except Exception as e:
        print(f"Error running simulation: {e}")
'''
    
    try:
        with open("run_simulation.py", "w") as f:
            f.write(run_script)
        print("✓ Created run_simulation.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create run script: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Robot Simulation Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install and check packages
    print("\n📦 Checking packages...")
    if not install_requirements():
        print("❌ Failed to install required packages")
        return False
    
    # Re-check packages after installation
    all_packages_ok = True
    packages_to_check = [
        ("PyBullet", "pybullet"),
        ("NumPy", "numpy")
    ]
    
    print("\n✅ Verifying installations...")
    for name, import_name in packages_to_check:
        if not check_package(name, import_name):
            all_packages_ok = False
    
    if not all_packages_ok:
        print("❌ Some packages are still missing")
        return False
    
    # Test PyBullet functionality
    if not test_pybullet():
        print("❌ PyBullet functionality test failed")
        return False
    
    # Create run script
    print("\n📝 Creating run script...")
    if not create_run_script():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nTo run the robot simulation:")
    print("1. python robot_sim_working.py")
    print("   OR")
    print("2. python run_simulation.py")
    print("\nThe simulation will:")
    print("• Open a 3D PyBullet window")
    print("• Load a robot (Kuka, R2D2, or custom)")
    print("• Execute 8 different movement instructions")
    print("• Show smooth joint movements and TCP control")
    print("\nControls in the simulation:")
    print("• Mouse: Rotate camera")
    print("• Mouse wheel: Zoom")
    print("• ESC: Exit simulation")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    else:
        print(f"\n✅ Setup successful! Run the simulation now.")