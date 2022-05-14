import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import numbers

def transform_variable(df: pd.DataFrame, x: str) -> pd.Series:
    if isinstance(df[x][0], numbers.Number):
        return df[x]  # type: pd.Series
    else:
        return pd.Series([i for i in range(0, len(df[x]))])

def linear_regression(df: pd.DataFrame, x, y) -> None:
    fixed_x = transform_variable(df, x)
    model = sm.OLS(df[y], sm.add_constant(fixed_x)).fit()
    print(model.summary())
    html = model.summary().tables[1].as_html()
    coef = pd.read_html(html, header=0, index_col=0)[0]["coef"]
    df.plot(x=x, y=y, kind="scatter")
    plt.plot(df[x], [pd.DataFrame.mean(df[y]) for _ in fixed_x.items()], color="green")
    plt.plot(
        df[x],
        [coef.values[1] * x + coef.values[0] for _, x in fixed_x.items()],
        color="red",
    )
    plt.xticks(rotation=90)
    plt.savefig(f"linear_reg_{y}_{x}.png")
    plt.close()

def main():
    df = pd.read_csv("../Practica 2/animes_clean.csv")
    df["start_date"] = pd.to_datetime(df["start_date"],format = '%Y-%m-%d')
    group_year = df["start_date"].dt.year
    filter_year = df.groupby(group_year)

    df_most_viewed = df["members"] >= 500000
    grp_year = df[df_most_viewed].groupby(df["start_date"].dt.year)
    grp_year = grp_year.mean()
    grp_year.reset_index(inplace=True)
    grp_year.drop("start_date", inplace=True, axis=1)

    dt_month = df["start_date"].dt.month
    after2017= df["start_date"] > "2017-01"
    before2018 = df["start_date"] < "2018-01"

    df_2017 = df[after2017 & before2018]
    grp_month = df_2017.groupby(dt_month)
    grp_month = grp_month.mean()
    grp_month.reset_index(inplace=True)
    grp_month.drop("start_date", inplace=True, axis=1)
    
    linear_regression(grp_year, "members", "ranked")
    linear_regression(grp_year, "ranked", "members")
    linear_regression(grp_year, "members", "score")
    linear_regression(grp_year, "score", "popularity")




if __name__ == "__main__":
    main()