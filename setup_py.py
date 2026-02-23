"""
Automatic Setup Script
Installs dependencies and generates database automatically
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    print("=" * 60)
    print("INSTALLING DEPENDENCIES...")
    print("=" * 60)
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("\n✗ Failed to install dependencies")
        return False

def generate_database():
    """Generate handwriting database"""
    print("\n" + "=" * 60)
    print("GENERATING HANDWRITING DATABASE...")
    print("=" * 60)
    
    try:
        # Import and run database generator
        from iam_processor import IAMProcessor
        import config
        
        processor = IAMProcessor(config.IAM_DATA_DIR)
        db = processor.process_iam_database(max_styles=100)
        processor.save_database(db, config.DATABASE_PATH)
        
        print("\n✓ Database generated successfully!")
        return True
    except Exception as e:
        print(f"\n✗ Failed to generate database: {e}")
        return False

def main():
    """Main setup function"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "   HANDWRITING GENERATOR - AUTOMATIC SETUP   ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("\nSetup failed. Please check your internet connection.")
        input("Press Enter to exit...")
        return
    
    # Step 2: Generate database
    if not generate_database():
        print("\nDatabase generation failed, but you can try running the app.")
        input("Press Enter to continue...")
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nYou can now run the application:")
    print("  • Double-click: run_app.bat (Windows)")
    print("  • Or run: python gui_app.py")
    print("\n")
    input("Press Enter to exit...")

if __name__ == '__main__':
    main()