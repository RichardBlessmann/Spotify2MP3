import subprocess
import sys
import os

def run_script(script_name):
    """Hilfsfunktion, die ein anderes Python-Skript startet."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    print(f"\n--- Starte {script_name} ---\n")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        print(f"⚠️ Fehler in {script_name}")
        sys.exit(result.returncode)

def main():
    print("▶ Running Step 1 & 2: Reduce CSV File & Search for YouTube links...")
    run_script("2SearchForYTLinks.py")
    print("▶ Running Step 3: Download MP3 files...")
    run_script("3csvfile2mp3.py")
    print("\nAlle Schritte erfolgreich abgeschlossen!")

if __name__ == "__main__":
    main()