from itertools import count
import matplotlib.pyplot as plt
import pandas as pd


def main():
    df = pd.read_csv("../Practica 2/animes_clean.csv")

    df["start_date"] = pd.to_datetime(df["start_date"],format = '%Y-%m-%d')
    group_year = df["start_date"].dt.year
    years = {2015, 2016, 2017, 2018, 2019}
    filter_year = df.groupby(group_year)
    
    #Animes mas vistos del 2018-2019

    for year in years:
        
        df_year = df[group_year == year]
        print(df_year)
        df_year["members"].plot(
        kind="line", figsize=(10, 10), title=f"Miembros(millones) por anime en el {year}")
        plt.savefig(f"miembros_por_anime_{year}.png")
        plt.close()
    

    

    #Calificacion vs Popularidad

    df.plot(
        kind="scatter", x="members", y="score", xlabel="Miembros(millones)",ylabel="Calificacion",title="Popularidad vs Calificacion")
    plt.savefig("Popular vs Calidad.png")
    plt.close()

    #Animes calificados del 2010-2016

    for year in years:
        
        df_year = df[group_year == year]
        print(df_year)
        df_year["score"].plot(
        kind="hist",ylabel="Frecuencia",figsize=(10, 10), title=f"Grafica de calificaciones de animes {year}")
        plt.savefig(f"animes_calificados_{year}.png")
        plt.close()

if __name__ == "__main__":
    main()