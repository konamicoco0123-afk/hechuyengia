#!/usr/bin/env python
# Simple script to run the web app with better output

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("=" * 60)
    print("He Chuyen Gia - Computer Recommendation Web Application")
    print("=" * 60)
    print()
    
    # Check if app.py exists
    app_path = Path(__file__).parent / "app.py"
    if not app_path.exists():
        print("Error: app.py not found!")
        sys.exit(1)
    
    print("Starting Flask application...")
    print()
    print("The application will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print()
    print("-" * 60)
    print()
    
    try:
        # Run Flask app
        subprocess.run([sys.executable, str(app_path)], check=False)
    except KeyboardInterrupt:
        print()
        print("-" * 60)
        print("Application stopped. Thank you for using He Chuyen Gia!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
