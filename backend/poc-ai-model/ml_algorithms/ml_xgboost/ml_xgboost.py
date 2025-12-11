import joblib
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from xgboost import XGBClassifier

from utils import fetch_dataset_from_csv, build_reports, prepare_dataset


def apply_xg_boost(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    model = XGBClassifier(
        scale_pos_weight=len(y_train[y_train == 0]) / len(y_train[y_train == 1]),
        random_state=42, eval_metric='logloss')

    # RandomizedSearchCV
    param_grid = {
        'n_estimators': [300, 500, 800, 1000],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.05, 0.1],
        'subsample': [0.7, 0.8, 1.0],
        'colsample_bytree': [0.7, 0.8, 1.0],
        'min_child_weight': [1, 3, 5],
        'gamma': [0, 0.1, 0.3],
        'reg_alpha': [0, 0.1, 0.5],
        'reg_lambda': [1, 2, 3]
    }
    grid_search = RandomizedSearchCV(estimator=model,
                                     param_distributions=param_grid,
                                     n_iter=40,  # 40 random combinations
                                     scoring='f1',
                                     cv=3,
                                     verbose=1,
                                     random_state=42,
                                     n_jobs=-1)

    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    print("Best XGBoost parameters:", grid_search.best_params_)
    joblib.dump(best_model, "xg-boost-model.pkl")

    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba > 0.4).astype(int)  # threshold 0.4 instead of 0.5
    build_reports(y_pred, y_test)


if __name__ == '__main__':
    bank_marketing = fetch_dataset_from_csv('../data/csv/bank-full-balanced.csv')
    X, y = prepare_dataset(bank_marketing)
    # plot_umap_2d(X, y)
    apply_xg_boost(X, y)
