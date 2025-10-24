"""
Launcher script for the Streamlit AI Conversation Buffer app.
This script ensures proper setup and launches the web interface.
"""

import subprocess
import sys
import os

def check_streamlit_installed():
    """Check if Streamlit is installed"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_streamlit():
    """Install Streamlit if not available"""
    print("Installing Streamlit...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit>=1.28.0"])
    print("✅ Streamlit installed successfully!")

def main():
    """Main launcher function"""
    print("🚀 Starting AI Conversation Buffer Web Interface...")
    print("=" * 50)
    
    # Check if Streamlit is installed
    if not check_streamlit_installed():
        print("❌ Streamlit not found. Installing...")
        install_streamlit()
    else:
        print("✅ Streamlit is already installed")
    
    # Launch the Streamlit app
    print("\n🌐 Launching web interface...")
    print("The app will open in your default web browser.")
    print("Press Ctrl+C to stop the server.")
    print("=" * 50)
    
    try:
        # Run the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down the web interface...")
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")
        print("Please make sure Streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    main()
