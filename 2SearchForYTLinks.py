import pandas as pd
from tkinter import Tk, filedialog
import os
from youtubesearchpython import VideosSearch

# Tkinter-Fenster verstecken
Tk().withdraw()

# Ordnerauswahl-Dialog öffnen
folder_path = filedialog.askdirectory(
    title="Wähle den Ordner mit deinen Playlist-CSV-Dateien"
)

# Ordnerauswahl-Dialog öffnen
folder_output_path = filedialog.askdirectory(
    title="Wähle den Ordner, in den die neuen CSV Dateien gespeichert werden sollen"
)

if folder_path and folder_output_path:
    # Alle CSV-Dateien im Ordner durchgehen
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)

            print(f"\nVerarbeite Datei: {file_name}")

            # CSV laden
            df = pd.read_csv(file_path)

            # Relevante Spalten prüfen
            if all(col in df.columns for col in ["Track Name", "Album Name", "Artist Name(s)"]):
                df_reduced = df[["Track Name", "Album Name", "Artist Name(s)"]].copy()

                youtube_links = []

                # YouTube-Suche für jeden Track
                for _, row in df_reduced.iterrows():
                    query = f"{row['Track Name']} {row['Artist Name(s)']}"
                    print(f"Suche auf YouTube: {query}")

                    search = VideosSearch(query, limit=1)
                    result = search.result()

                    if result["result"]:
                        url = result["result"][0]["link"]
                        youtube_links.append(url)
                    else:
                        youtube_links.append("Kein Ergebnis")

                # Neue Spalte mit Links hinzufügen
                df_reduced["YouTube Link"] = youtube_links

                # Neue CSV speichern
                output_file = file_name.replace(".csv", "_with_youtube.csv")
                output_path = os.path.join(folder_output_path, output_file)
                df_reduced.to_csv(output_path, index=False)

                print(f"Gespeichert unter: {output_path}")
            else:
                print(f"Datei {file_name} hat nicht die erwarteten Spalten.")
else:
    print("Kein Ordner ausgewählt.")
