import sys

import pandas as pd
import yt_dlp
import os
from tkinter import Tk, filedialog
def main:
    # Tkinter-Fenster verstecken
    Tk().withdraw()

    # Ordnerauswahl-Dialog öffnen
    folder_path = filedialog.askdirectory(
        title="Choose the folder with CSV-files with yt link"
    )

    folder_output_path = filedialog.askdirectory(
        title="Choose the file, where the downloaded mp3 files shall be saved!"
    )
    if getattr(sys, 'frozen', False):
        # Running from PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running from source
        base_path = os.path.dirname(__file__)
    skipped_urls = []
    ffmpeg_path = os.path.join(base_path, "ffmpeg-2025-09-18-git-c373636f55-essentials_build/ffmpeg-2025-09-18-git-c373636f55-essentials_build/bin")

    cookie_file_path = filedialog.askopenfilename(
        title="Choose a cookies.txt file (optional,escape when not needed)",
        filetypes=[("Text files", "*.txt"), ("Alle Dateien", "*.*")]
    )
    if folder_path and folder_output_path:
        # Optionen für MP3-Download
       ydl_opts = {
            "format": "bestaudio/best",
            "ffmpeg_location": ffmpeg_path,
            "outtmpl": f"{folder_output_path}/%(title)s.%(ext)s",
            "quiet": False,
        }
        if cookie_file_path:
            ydl_opts["cookiefile"] = cookie_file_path
            print(f"Cookie-file: {cookie_file_path}")

        # Alle CSV-Dateien im Ordner durchgehen
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                print(f"\nWorking on: {file_name}")

                # CSV laden
                df = pd.read_csv(file_path)

                # Prüfen, ob "YouTube Link"-Spalte existiert
                if "YouTube Link" not in df.columns:
                    print(f"️ File {file_name} doesn't have a column 'YouTube Link'.")
                    continue

                # Downloads starten
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    for url in df["YouTube Link"]:
                        if pd.notna(url) and url.startswith("http"):
                            print(f"⬇️ Lade herunter: {url}")
                            try:
                                ydl.download([url])
                            except Exception as e:
                                print(f"⚠️ Fehler beim Herunterladen von {url}: {e}")
                                skipped_urls.append((url, str(e)))
                                continue  # Skip and go to the next URL

                if skipped_urls:
                    skipped_file_path = os.path.join(folder_output_path, "skipped_urls.txt")
                    with open(skipped_file_path, "w", encoding="utf-8") as f:
                        for url, error in skipped_urls:
                            f.write(f"{url} - Fehler: {error}\n")
                    print(f"\nSome Videos coudn't be downloaded.")
                    print(f"Saved in: {skipped_file_path}")

        print("\n Finished Downloading!")
    else:
        print("No Output Folder chosen.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("An Error Occured. Try restarting")