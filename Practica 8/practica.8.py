from tkinter import Y
import scipy.stats as spy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json


def get_cmap(n, name="hsv"):
    """Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name."""
    return plt.cm.get_cmap(name, n)


def scatter_group_by(
    df: pd.DataFrame, x_column: str, y_column: str, label_column: str
):
    fig, ax = plt.subplots()
    labels = pd.unique(df[label_column])
    cmap = get_cmap(len(labels) + 1)
    for i, label in enumerate(labels):
        filter_df = df.query(f'{label_column} == "{label}"')
        ax.scatter(filter_df[x_column], filter_df[y_column], label=label,color=cmap(i))
    ax.legend(prop={'size': 5})
    ax.set_xlabel('Calificaciones')
    ax.set_ylabel('Seguidores')
    ax.set_title('KNN Animes 2010-2018')
    ax.ticklabel_format(style='plain')
    plt.savefig("knn.png")
    plt.close()

def euclidean_distance(p_1: np.array, p_2: np.array) -> float:
    return np.sqrt(np.sum((p_2 - p_1) ** 2))


def k_nearest_neightbors(
    points: list([np.array]), labels: np.array, input_data: list([np.array]), k: int):
    input_distances = [
        [euclidean_distance(input_point, point) for point in points]
        for input_point in input_data
    ]
    points_k_nearest = [
        np.argsort(input_point_dist)[:k] for input_point_dist in input_distances
    ]
    return [
        spy.mode([labels[index] for index in point_nearest])
        for point_nearest in points_k_nearest
    ]

def main():
    df = pd.read_csv("../Practica 2/animes_clean.csv")
    df['genre'] = df['genre'].str.replace(",.*$", "")
    df["start_date"] = pd.to_datetime(df["start_date"],format = '%Y-%m-%d')
    fantasy = df["genre"] == "Fantasy"
    #romance = df["genre"] == "Romance"
    mystery = df["genre"] == "Mystery"
    harem = df["genre"] == "Harem"
    hentai = df["genre"] == "Hentai"


    ini_time = df["start_date"] > "2010-01-01"
    fin_time = df["start_date"] < "2018-04-01"
    #popular = df["members"] > 0000
    time_range = ini_time & fin_time
    categories = fantasy | harem | hentai | mystery

    y = "members"
    x = "score"
    grp = "genre"

    df = df[time_range & categories]
    df = df[[x, y, grp]]

    scatter_group_by(df, x, y, grp)

    list_t = [
        (np.array(tuples[0:1]), tuples[2])
        for tuples in df.itertuples(index=False, name=None)
    ]
    points = [point for point, _ in list_t]
    labels = [label for _, label in list_t]

    kn = k_nearest_neightbors(
        points,labels,
        [
            np.array([9, 1200000]),
            np.array([5, 400000]),
            np.array([0, 0]),
            np.array([7, 50000]),
        ],4,
    )
    print(np.array(kn))

if __name__ == "__main__":
    main()