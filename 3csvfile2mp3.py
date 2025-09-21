import sys

import pandas as pd
import yt_dlp
import os
from tkinter import Tk, filedialog

# Tkinter-Fenster verstecken
Tk().withdraw()

# Ordnerauswahl-Dialog öffnen
folder_path = filedialog.askdirectory(
    title="Wähle den Ordner mit deinen CSV-Dateien mit yt link"
)

folder_output_path = filedialog.askdirectory(
    title="Wähle den Ordner, in den die bearbeiteten mp3-Dateien gespeichert werden sollen!"
)
if getattr(sys, 'frozen', False):
    # Running from PyInstaller bundle
    base_path = sys._MEIPASS
else:
    # Running from source
    base_path = os.path.dirname(__file__)

ffmpeg_path = os.path.join(base_path, "ffmpeg-2025-09-18-git-c373636f55-essentials_build/ffmpeg-2025-09-18-git-c373636f55-essentials_build/bin")

if folder_path and folder_output_path:
    # Optionen für MP3-Download
    ydl_opts = {
        "format": "bestaudio/best",
        "ffmpeg_location": ffmpeg_path,
        "outtmpl": f"{folder_output_path}/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": False,
    }

    # Alle CSV-Dateien im Ordner durchgehen
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            print(f"\n Verarbeite Datei: {file_name}")

            # CSV laden
            df = pd.read_csv(file_path)

            # Prüfen, ob "YouTube Link"-Spalte existiert
            if "YouTube Link" not in df.columns:
                print(f"️ Datei {file_name} enthält keine Spalte 'YouTube Link'.")
                continue

            # Downloads starten
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for url in df["YouTube Link"]:
                    if pd.notna(url) and url.startswith("http"):
                        print(f"Lade herunter: {url}")
                        ydl.download([url])

    print("\n Alle Downloads abgeschlossen!")
else:
    print("Kein Ordner ausgewählt.")
