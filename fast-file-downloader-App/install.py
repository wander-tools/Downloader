import sys
import subprocess
import os
import time
import shutil

def check_python_version():
    """Check if Python version is sufficient"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        print("📥 Download from: https://python.org")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    requirements = [
        "requests>=2.25.1",
        "urllib3>=1.26.0"
    ]
    
    for package in requirements:
        try:
            package_name = package.split('>=')[0] if '>=' in package else package
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package_name} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("🔄 Upgrading pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Pip upgrade failed, continuing with current version")
        return True  # Continue even if pip upgrade fails

def create_desktop_shortcut():
    """Create desktop shortcut for Windows"""
    if os.name == 'nt':  # Windows
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "Fast Downloader Pro.lnk")
            
            # Get current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            bat_file = os.path.join(current_dir, "RunDownloader.bat")
            python_exe = sys.executable
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = bat_file
            shortcut.WorkingDirectory = current_dir
            shortcut.IconLocation = python_exe
            shortcut.Description = "Fast Downloader Pro - Professional File Downloader"
            shortcut.save()
            
            print("✅ Desktop shortcut created successfully!")
            return True
        except ImportError:
            print("ℹ️  Desktop shortcut creation skipped (optional packages not available)")
            return True
        except Exception as e:
            print(f"ℹ️  Desktop shortcut creation skipped: {e}")
            return True
    else:
        print("ℹ️  Desktop shortcut creation is for Windows only")
        return True

def create_start_menu_shortcut():
    """Create start menu shortcut for Windows"""
    if os.name == 'nt':
        try:
            import winshell
            
            start_menu = winshell.start_menu()
            programs_dir = os.path.join(start_menu, "Programs")
            app_dir = os.path.join(programs_dir, "Fast Downloader Pro")
            
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
            
            shortcut_path = os.path.join(app_dir, "Fast Downloader Pro.lnk")
            current_dir = os.path.dirname(os.path.abspath(__file__))
            bat_file = os.path.join(current_dir, "RunDownloader.bat")
            
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = bat_file
            shortcut.WorkingDirectory = current_dir
            shortcut.IconLocation = sys.executable
            shortcut.Description = "Professional File Downloader Application"
            shortcut.save()
            
            print("✅ Start menu shortcut created successfully!")
            return True
        except Exception as e:
            print(f"ℹ️  Start menu shortcut skipped: {e}")
            return True
    return True

def verify_installation():
    """Verify that everything is installed correctly"""
    print("🔍 Verifying installation...")
    
    try:
        import requests
        print("✅ Requests library verified")
        
        # Test basic functionality
        test_url = "https://httpbin.org/get"
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            print("✅ Network connectivity verified")
        else:
            print("⚠️  Network test failed, but installation is complete")
            
        return True
    except Exception as e:
        print(f"❌ Installation verification failed: {e}")
        return False

def create_quick_launch_bat():
    """Create a quick launch batch file"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        quick_launch_path = os.path.join(current_dir, "QuickLaunch.bat")
        
        with open(quick_launch_path, 'w') as f:
            f.write('''@echo off
chcp 65001 >nul
title Fast Downloader Pro - Quick Launch
echo 🚀 Starting Fast Downloader Pro...
python fast_downloader.py
pause
''')
        print("✅ Quick launch file created")
        return True
    except Exception as e:
        print(f"ℹ️  Quick launch file creation skipped: {e}")
        return True

def display_welcome_message():
    """Display welcome message"""
    print("\n" + "="*60)
    print("           🎉 FAST DOWNLOADER PRO - READY! 🎉")
    print("="*60)
    print("\n📋 Features:")
    print("  ✅ Professional dark theme UI")
    print("  ✅ Real-time download statistics")
    print("  ✅ Time remaining estimation")
    print("  ✅ Pause/Resume functionality")
    print("  ✅ Download history")
    print("  ✅ Support for all file types")
    print("\n🚀 The application will start automatically...")
    print("⚡ Terminal will minimize in 5 seconds...")
    print("="*60)

def main():
    """Main installation function"""
    print("🚀 Fast Downloader Pro - Auto Installer")
    print("="*50)
    
    # Check Python
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Upgrade pip
    if not upgrade_pip():
        print("⚠️  Continuing with existing pip version...")
    
    # Install requirements
    if not install_requirements():
        print("❌ Installation failed during package installation")
        input("Press Enter to exit...")
        return
    
    # Create shortcuts
    create_desktop_shortcut()
    create_start_menu_shortcut()
    create_quick_launch_bat()
    
    # Verify installation
    if not verify_installation():
        print("⚠️  Installation completed with warnings")
    else:
        print("✅ Installation completed successfully!")
    
    # Display welcome message
    display_welcome_message()
    
    # Wait before launching
    time.sleep(5)
    
    # Launch the application
    try:
        print("🎯 Launching application...")
        subprocess.Popen([sys.executable, "fast_downloader.py"])
    except Exception as e:
        print(f"❌ Failed to launch application: {e}")
        print("📝 You can manually run: python fast_downloader.py")
    
    input("\nPress Enter to close this window...")

if __name__ == "__main__":
    main()