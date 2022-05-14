import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

def main():
    df = pd.read_csv("../Practica 2/animes_clean.csv")

    df["start_date"] = pd.to_datetime(df["start_date"],format = '%Y-%m-%d')
    group_year = df["start_date"].dt.year
    filter_year = df.groupby(group_year)
    
    #filter_comedy = df['genre'].str.contains('Comedy')
    #group_comedy = df.groupby([filter_comedy, group_year])
    #print(group_comedy)
    #comedy_anime = df['genre'].str.contains('Comedy').groupby(group_year).sum()
    #print(comedy_anime)
    group_animes_years = df.groupby(["title", group_year])
    total_members = group_animes_years[["members", "score"]].sum()
    total_members.reset_index(inplace=True)
    total_members.drop("start_date", inplace=True, axis=1)

    print(total_members)
    
    animes_x_members = total_members[["title", "members"]]

    print(animes_x_members)
    model = ols("members ~ title", data=animes_x_members).fit()
    df_anova = sm.stats.anova_lm(model, typ=2)

    if df_anova["PR(>F)"][0] < 0.005:
        print("Hay diferencias")
        print(df_anova)
    else:
        print("No hay diferencias")



if __name__ == "__main__":
    main()