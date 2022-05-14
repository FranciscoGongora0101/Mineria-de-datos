import pandas as pd
import json
from typing import Tuple, List
from datetime import datetime
from tabulate import tabulate

def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))

def main() -> None:
    df_animes = pd.read_csv("../Practica 1/animes.csv")
    df_profiles = pd.read_csv("../Practica 1/profiles.csv")
    df_reviews = pd.read_csv("../Practica 1/reviews.csv")

    #Se eliminan campos que no utilizaremos
    df_animes = df_animes.drop(['img_url'], axis=1)
    df_animes = df_animes.drop(['link'], axis=1)
    df_profiles = df_profiles.drop(['link'], axis=1)
    df_reviews = df_reviews.drop(['link'], axis=1)

    #Separamos las fechas en dos campos de fecha inicial y final para cada anime
    df_animes[['start_date','end_date']] = df_animes.aired.str.split("to", expand=True)
    df_animes["start_date"] = pd.to_datetime(df_animes["start_date"], errors='coerce')
    df_animes["end_date"] = pd.to_datetime(df_animes["end_date"], errors='coerce')
    df_animes = df_animes.drop(['aired'], axis=1)

    #Se elminan caracteres para el campo de genero de cada anime
    df_animes['genre'] = df_animes['genre'].str.replace('[', '')
    df_animes['genre'] = df_animes['genre'].str.replace(']', '')
    df_animes['genre'] = df_animes['genre'].str.replace("'", "")
    

    #Se elminan duplicados de los csv
    print(df_animes.uid.duplicated().sum())
    df_animes.drop_duplicates(subset=['uid'], inplace=True)

    print(df_profiles.profile.duplicated().sum())
    df_profiles.drop_duplicates(inplace=True)

    print(df_reviews.uid.duplicated().sum())
    df_reviews.drop_duplicates(inplace=True)

    #Se imprimen y se generan los csv nuevos
    #print(df_animes)
    #print(df_animes.dtypes)
    #print(df_profiles)
    #print(df_profiles.dtypes) 
    #print(df_reviews)
    #print(df_reviews.dtypes)
    df_animes.to_csv("animes_clean.csv", index=False)
    df_reviews.to_csv("reviews_clean.csv", index=False)
    df_profiles.to_csv("profiles_clean.csv", index=False)

if __name__ == "__main__":
    main()