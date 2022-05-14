import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import json
import numbers
from typing import Dict, Tuple

def transform_variable(df: pd.DataFrame, x: str) -> pd.Series:
    if isinstance(df[x][df.index[0]], numbers.Number):
        return df[x]  # type: pd.Series
    else:
        return pd.Series([i for i in range(0, len(df[x]))])

def linear_regression(df: pd.DataFrame, x: str, y: str) -> Dict[str, float]:
    fixed_x = transform_variable(df, x)
    model = sm.OLS(list(df[y]), sm.add_constant(fixed_x), alpha=0.05).fit()
    bands = pd.read_html(model.summary().tables[1].as_html(), header=0, index_col=0)[0]
    coef = bands["coef"]
    tables_0 = model.summary().tables[0].as_html()
    r_2_t = pd.read_html(tables_0, header=None, index_col=None)[0]
    return {
        "m": coef.values[1],
        "b": coef.values[0],
        "r2": r_2_t.values[0][3],
        "r2_adj": r_2_t.values[1][3],
        "low_band": bands["[0.025"][0],
        "hi_band": bands["0.975]"][0],
    }

def plt_lr(
    df: pd.DataFrame,
    x: str,
    y: str,
    m: float,
    b: float,
    r2: float,
    r2_adj: float,
    low_band: float,
    hi_band: float,
    colors: Tuple[str, str],
):
    fixed_x = transform_variable(df, x)
    plt.plot(df[x], [m * x + b for _, x in fixed_x.items()], color=colors[0])
    plt.fill_between(
        df[x],
        [m * x + low_band for _, x in fixed_x.items()],
        [m * x + hi_band for _, x in fixed_x.items()],
        alpha=0.2,
        color=colors[1],
    )

def main():
    df = pd.read_csv("../Practica 2/animes_clean.csv")
    df['genre'] = df['genre'].str.replace(",.*$", "")
    comedy = df["genre"] == "Comedy"
    df["start_date"] = pd.to_datetime(df["start_date"],format = '%Y-%m-%d')
    group_date = df["start_date"].dt.date

    df = df[comedy].groupby(group_date).sum()
    print(df)
    df.reset_index(inplace=True)
    df = df[["start_date", "members"]]
    print(df)
    #df.drop(df.tail(300).index,inplace=True)
    df_comedy_100 = df.tail(100)

    x = "start_date"
    y = "members"
    df_comedy_100.plot(x=x, y=y, kind="scatter")
    lr = linear_regression(df_comedy_100, x, y)
    plt_lr(df=df_comedy_100, x=x, y=y, colors=("red", "orange"), **lr)

    lr = linear_regression(df_comedy_100.tail(10), x, y)
    plt_lr(df=df_comedy_100.tail(10), x=x, y=y, colors=("red", "orange"), **lr)
    df_comedy_friday = df_comedy_100[pd.to_datetime(df_comedy_100[x]).dt.dayofweek == 5]
    print(df_comedy_friday)

    lr = linear_regression(df_comedy_friday, x, y)
    plt_lr(df=df_comedy_friday, x=x, y=y, colors=("blue", "blue"), **lr)

    plt.xticks(rotation=90)
    plt.savefig(f"lr_{y}_{x}_m.png")
    plt.close()

    df_2018 = df.loc[
    (pd.to_datetime(df[x]) >= "2018-01-01") & (pd.to_datetime(df[x]) < "2019-01-01")]
    print(df_2018)
    
    dfs = [
    ("100D", df_comedy_100),
    ("10D", df_comedy_100.tail(10)),
    ("5D", df_comedy_100.tail(5)),
    (
        "viernes",
        df_comedy_100[pd.to_datetime(df_comedy_100[x]).dt.dayofweek == 5],
    ),
    ("100D-1Y", df_2018),
    ("10D-Y", df_2018.tail(10)),
    ("5D-Y", df_2018.tail(5)),
    (
        "viernes-Y",
        df_2018[pd.to_datetime(df_2018[x]).dt.dayofweek == 5],
    ),
    ]
    lrs = [(title, linear_regression(_df, x=x, y=y), len(_df)) for title, _df in dfs]
    lrs_p = [
        (title, lr_dict["m"] * size + lr_dict["b"], lr_dict)
        for title, lr_dict, size in lrs
    ]
    print(lrs_p)


if __name__ == "__main__":
    main()