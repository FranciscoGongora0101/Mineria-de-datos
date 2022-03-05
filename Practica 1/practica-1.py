from kaggle.api.kaggle_api_extended import KaggleApi
import os, kaggle
from zipfile import ZipFile

def main():
    api = kaggle.api
    api.authenticate()
    dataset_name = "marlesson/myanimelist-dataset-animes-profiles-reviews"

    api.dataset_download_file(dataset_name, "animes.csv")
    api.dataset_download_file(dataset_name, "profiles.csv")
    api.dataset_download_file(dataset_name, "reviews.csv")

    with ZipFile("animes.csv.zip", "r") as zip_obj1:
        zip_obj1.extractall()
    with ZipFile("profiles.csv.zip", "r") as zip_obj2:
        zip_obj2.extractall()
    with ZipFile("reviews.csv.zip", "r") as zip_obj3:
        zip_obj3.extractall()
    
    os.remove("animes.csv.zip")
    os.remove("profiles.csv.zip")
    os.remove("reviews.csv.zip")

if __name__ == "__main__":
    main()