import pandas as pd
import yt_dlp
import os
from tkinter import Tk, filedialog

# Tkinter-Fenster verstecken
Tk().withdraw()

# Ordnerauswahl-Dialog öffnen
folder_path = filedialog.askdirectory(
    title="Wähle den Ordner mit deinen CSV-Dateien"
)

if folder_path:
    # Optionen für MP3-Download
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",   # Dateiname = Videotitel
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
