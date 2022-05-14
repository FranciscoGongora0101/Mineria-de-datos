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
    file_path: str, df: pd.DataFrame, x_column: str, y_column: str, label_column: str
):
    fig, ax = plt.subplots()
    labels = pd.unique(df[label_column])
    cmap = get_cmap(len(labels) + 1)
    for i, label in enumerate(labels):
        filter_df = df.query(f'{label_column} == "{label}"')
        ax.scatter(filter_df[x_column], filter_df[y_column], label=label, color=cmap(i))
    ax.legend(prop={'size': 5})
    plt.savefig(file_path)
    plt.close()

def euclidean_distance(p_1: np.array, p_2: np.array) -> float:
    return np.sqrt(np.sum((p_2 - p_1) ** 2))


def k_means(points: list([np.array]), k: int):
    DIM = len(points[0])
    N = len(points)
    num_cluster = k
    iterations = 15

    x = np.array(points)
    y = np.random.randint(0, num_cluster, N)

    mean = np.zeros((num_cluster, DIM))
    for t in range(iterations):
        for k in range(num_cluster):
            mean[k] = np.mean(x[y == k], axis=0)
        for i in range(N):
            dist = np.sum((mean - x[i]) ** 2, axis=1)
            pred = np.argmin(dist)
            y[i] = pred

    for kl in range(num_cluster):
        xp = x[y == kl, 0]
        yp = x[y == kl, 1]
        plt.scatter(xp, yp)
    plt.savefig("k_means.png")
    plt.close()
    return mean

def main():
    df = pd.read_csv("../Practica 2/animes_clean.csv")
    df['genre'] = df['genre'].str.replace(",.*$", "")
    df["start_date"] = pd.to_datetime(df["start_date"],format = '%Y-%m-%d')
    fantasy = df["genre"] == "Fantasy"
    romance = df["genre"] == "Romance"
    comedy = df["genre"] == "Comedy"
    harem = df["genre"] == "Harem"

    ini_time = df["start_date"] > "2017-01-01"
    fin_time = df["start_date"] < "2018-04-01"
    #popular = df["members"] > 0000
    time_range = ini_time & fin_time
    categories = fantasy | harem | romance | comedy

    y = "members"
    x = "score"
    grp = "genre"

    df = df[time_range & categories]
    df = df[[x, y, grp]]
    scatter_group_by("clustering.png", df, x, y, grp)

    list_t = [
        (np.array(tuples[0:2]), tuples[2])
        for tuples in df.itertuples(index=False, name=None)
    ]
    points = [point for point, _ in list_t]
    labels = [label for _, label in list_t]

    kn = k_means(
        points,
        4,
    )
    print(kn)

if __name__ == "__main__":
    main()