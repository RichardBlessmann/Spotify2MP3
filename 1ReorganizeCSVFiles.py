import pandas as pd
from tkinter import Tk, filedialog
import os

# Tkinter-Fenster verstecken
Tk().withdraw()

# Ordnerauswahl-Dialog öffnen
folder_path = filedialog.askdirectory(
    title="Wähle den Ordner mit deinen Playlist-CSV-Dateien"
)
folder_output_path = filedialog.askdirectory(
    title="Wähle den Ordner, in den die bearbeiteten CSV-Dateien gespeichert werden sollen!"
)

if folder_path and folder_output_path:
    # Alle CSV-Dateien im Eingabe-Ordner durchgehen
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)

            print(f"Verarbeite Datei: {file_name}")

            # CSV laden
            df = pd.read_csv(file_path)

            # Relevante Spalten auswählen (falls vorhanden)
            if all(col in df.columns for col in ["Track Name", "Album Name", "Artist Name(s)"]):
                df_reduced = df[["Track Name", "Album Name", "Artist Name(s)"]]

                # Neuen Dateipfad im Ausgabeordner erstellen
                output_file = file_name.replace(".csv", "_reduced.csv")
                output_path = os.path.join(folder_output_path, output_file)

                # Neue CSV speichern
                df_reduced.to_csv(output_path, index=False)

                print(f"Gespeichert unter: {output_path}\n")
            else:
                print(f"Datei {file_name} hat nicht die erwarteten Spalten.\n")
else:
    print("Kein Ordner ausgewählt.")
