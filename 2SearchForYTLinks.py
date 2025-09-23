import pandas as pd
from tkinter import Tk, filedialog
import os
from youtubesearchpython import VideosSearch


def main():
    # Tkinter-Fenster verstecken
    Tk().withdraw()

    # Ordnerauswahl-Dialog öffnen
    folder_path = filedialog.askdirectory(
        title="Choose the folder with the csv files"
    )
    folder_output_path = filedialog.askdirectory(
        title="Choose the folder where the new csv files are supposed to be saved with youtube links!\n Preferrably not in the same folder as the origin folder"
    )

    if folder_path and folder_output_path:
        # Alle CSV-Dateien im Eingabe-Ordner durchgehen
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)

                print(f"\nWorking on: {file_name}")

                # CSV laden
                df = pd.read_csv(file_path)

                # Relevante Spalten prüfen
                required_columns = ["Track Name", "Album Name", "Artist Name(s)"]
                if all(col in df.columns for col in required_columns):
                    # Nur relevante Spalten kopieren
                    df_reduced = df[required_columns].copy()

                    youtube_links = []

                    # YouTube-Suche für jeden Track
                    for _, row in df_reduced.iterrows():
                        query = f"{row['Track Name']} {row['Artist Name(s)']}"
                        print(f"🔍 Suche auf YouTube: {query}")

                        search = VideosSearch(query, limit=1)
                        result = search.result()

                        if result["result"]:
                            url = result["result"][0]["link"]
                            youtube_links.append(url)
                        else:
                            youtube_links.append("Kein Ergebnis")

                    # Neue Spalte mit Links hinzufügen
                    df_reduced["YouTube Link"] = youtube_links

                    # Neue Datei speichern
                    output_file = file_name.replace(".csv", "_reduced_with_youtube.csv")
                    output_path = os.path.join(folder_output_path, output_file)
                    df_reduced.to_csv(output_path, index=False)

                    print(f"Saved in: {output_path}\n")
                else:
                    print(f"File {file_name} doesn't have the expected column.\n")
    else:
        print("No folder chosen.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("An Error occured. Press Enter to finish.")
