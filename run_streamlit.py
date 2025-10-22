"""
Workaround script to run the Jac streamlit app with proper path handling on Windows.
This fixes the Unicode escape error by using raw strings for paths.
"""
import subprocess
import sys
import os

def main():
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Run jac streamlit with just the filename (no path needed)
    try:
        result = subprocess.run(
            ["jac", "streamlit", "client.jac"],
            check=True,
            cwd=script_dir
        )
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"Error running jac streamlit: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'jac' command not found. Make sure jaclang is installed.")
        print("Install with: pip install jaclang jac-streamlit")
        sys.exit(1)

if __name__ == "__main__":
    main()
