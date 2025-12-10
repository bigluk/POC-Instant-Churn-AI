import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, f1_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler

from ml_algorithms.utils import build_reports, fetch_dataset_from_csv, prepare_dataset


def apply_logistic_regression(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # GridSearchCV
    model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
    param_grid = {
        'C': [0.01, 0.1, 1, 10],
        'penalty': ['l1', 'l2'],
        'solver': ['liblinear', 'saga']
    }
    scorer = make_scorer(f1_score, pos_label=1)
    grid_search = GridSearchCV(model, param_grid, scoring=scorer, cv=3, verbose=2, n_jobs=-1)
    grid_search.fit(X_train_scaled, y_train)

    best_model = grid_search.best_estimator_
    print("Best Logistic Regression parameters:", grid_search.best_params_)
    joblib.dump(best_model, "logistic-regression-model.pkl")

    y_pred = best_model.predict(X_test_scaled)
    build_reports(y_pred, y_test)
    return best_model, scaler


if __name__ == '__main__':
    bank_marketing = fetch_dataset_from_csv('../data/csv/bank-full-balanced.csv')
    X, y = prepare_dataset(bank_marketing)
    # plot_umap_2d(X, y)
    apply_logistic_regression(X, y)
