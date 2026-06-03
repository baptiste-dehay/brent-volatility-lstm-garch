import pandas as pd
from pathlib import Path

# Chemins
file_1 = "d:/Documents/ESLSCA - MBA2 Finance de marché/Machine Learning/Projet LSTM/repository/brent-volatility-lstm-garch/data/raw/brent_part1.csv"
file_2 = "d:/Documents/ESLSCA - MBA2 Finance de marché/Machine Learning/Projet LSTM/repository/brent-volatility-lstm-garch/data/raw/brent_part2.csv"

output_file = "d:/Documents/ESLSCA - MBA2 Finance de marché/Machine Learning/Projet LSTM/repository/brent-volatility-lstm-garch/data/raw/brent_oil_futures_2005_2024.csv"

# Lecture des CSV
# sep=";" car vos fichiers sont séparés par des points-virgules
# encoding="utf-8-sig" permet de retirer le BOM éventuel avant Date
df1 = pd.read_csv(file_1, sep=";", encoding="utf-8-sig")
df2 = pd.read_csv(file_2, sep=";", encoding="utf-8-sig")

# Nettoyage des noms de colonnes
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

print("Colonnes fichier 1 :", df1.columns.tolist())
print("Colonnes fichier 2 :", df2.columns.tolist())

# Fusion verticale
df = pd.concat([df1, df2], ignore_index=True)

# Vérification de la colonne Date
if "Date" not in df.columns:
    raise ValueError(f"Colonne 'Date' introuvable. Colonnes disponibles : {df.columns.tolist()}")

# Conversion de la colonne Date
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce")

# Supprimer les lignes dont la date n'a pas pu être convertie
df = df.dropna(subset=["Date"])

# Suppression des doublons de dates
df = df.drop_duplicates(subset=["Date"], keep="first")

# Tri chronologique réel
df = df.sort_values("Date", ascending=True).reset_index(drop=True)

# Sauvegarde au format propre YYYY-MM-DD
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

# Sauvegarde finale
df.to_csv(output_file, index=False)

print("\nFichier fusionné sauvegardé :", output_file)
print("Nombre d'observations :", len(df))
print("Date de début :", df["Date"].min())
print("Date de fin :", df["Date"].max())
print("Colonnes :", df.columns.tolist())

print("\nPremières lignes :")
print(df.head())

print("\nDernières lignes :")
print(df.tail())