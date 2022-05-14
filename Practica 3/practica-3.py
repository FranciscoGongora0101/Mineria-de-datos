from msilib.schema import tables
import pandas as pd
import json
from typing import Tuple, List
from datetime import datetime
from tabulate import tabulate
import math

def main():
    df_animes = pd.read_csv("../Practica 2/animes_clean.csv")
    df_profiles = pd.read_csv("../Practica 2/profiles_clean.csv")

    
    df_animes["start_date"] = pd.to_datetime(df_animes["start_date"],format = '%Y-%m-%d')
    group_year = df_animes["start_date"].dt.year
    filter_year = df_animes.groupby(group_year)


    #Animes mas populares de cada año
    popular_anime = df_animes.loc[filter_year["members"].idxmax()][["start_date", "title", "members"]]
    popular_anime.to_csv("popular_anime_year.csv", index=False)
  
    #100 Animes mejor calificados 
    
    best_anime = df_animes.sort_values('ranked').head(100)[["start_date", "title", "score"]]
    best_anime.to_csv("best_anime.csv", index=False)

    #Animes con mas miembros de las 100 mejor calificadas

    best_popular_anime = df_animes.sort_values('ranked').head(100)[["start_date", "title", "score","members"]]
    best_popular_anime = best_popular_anime.sort_values('members', ascending=False)
    best_popular_anime.to_csv("best_popular_anime.csv", index=False)

    #Promedio de hombres y mujeres en los perfiles  
    total = len(df_profiles.index)
    males = df_profiles['gender'].str.contains('Male', na=False).sum()
    females = df_profiles['gender'].str.contains('Female', na=False).sum()
    non_binary = df_profiles['gender'].str.contains('Non-Binary', na=False).sum()
    not_identity = df_profiles['gender'].str.contains(' ', na=True).sum()
    print("Total de perfiles:",total, "1.0")
    print("Hombres:",males, round((males/total),2))
    print("Mujeres:",females, round((females/total),2))
    print("No binario:",non_binary, round((non_binary/total),2))
    print("Sin identificar:", not_identity, round((not_identity/total),2))
    
if __name__ == "__main__":
    main()