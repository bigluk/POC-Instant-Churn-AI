import csv

import numpy as np
import pandas as pd
import seaborn as sns
import umap
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from ucimlrepo import fetch_ucirepo


def fetch_dataset_from_csv(file_name):
    df = pd.read_csv(file_name, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    return df[["age", "job", "marital", "education", "default", "balance", "housing", "loan", "y"]]


def fetch_dataset_from_internet():
    # fetch dataset
    bank_marketing = fetch_ucirepo(id=222)

    # data (as pandas dataframes)
    X = bank_marketing.data.features
    y = bank_marketing.data.targets

    df = pd.concat([X, y], axis=1)
    return df[["age", "job", "marital", "education", "default", "balance", "housing", "loan", "y"]]


def plot_umap_2d(X, y, title="UMAP Projection (2D)"):
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
    X_umap = reducer.fit_transform(X)

    plt.figure(figsize=(8, 6))
    plt.scatter(X_umap[:, 0], X_umap[:, 1], c=y, cmap='coolwarm', alpha=0.6, s=30)
    plt.title(title)
    plt.xlabel("UMAP dim 1")
    plt.ylabel("UMAP dim 2")
    plt.grid(True)
    plt.show()


def build_reports(y_pred, y_test):
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    # --- CONFUSION MATRIX ---
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=np.unique(y_test),
                yticklabels=np.unique(y_test))
    plt.title(f"Confusion Matrix\nAccuracy: {acc:.2%}", fontsize=14, weight='bold')
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=300)
    plt.show()

    # --- CLASSIFICATION REPORT ---
    report_df = pd.DataFrame(report).transpose().round(2)

    plt.figure(figsize=(8, 4))
    sns.heatmap(report_df.iloc[:-1, :-1], annot=True, cmap='Greens', cbar=False)
    plt.title("Classification Report", fontsize=14, weight='bold')
    plt.tight_layout()
    plt.savefig("classification_report.png", dpi=300)
    plt.show()


def prepare_dataset(df):
    binary_cols = ["default", "housing", "loan", "y"]
    df[binary_cols] = df[binary_cols].map(lambda x: 1 if x == "yes" else 0)

    bins = [0, 25, 35, 50, 65, 100]
    labels = ["<25", "25-35", "36-50", "51-65", "65+"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
    df = df.drop("age", axis=1)

    # One-Hot Encoding
    categorical_cols = ["job", "marital", "education", "age_group"]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True, dtype=int)

    X = df.drop("y", axis=1)
    y = df["y"]

    return X, y