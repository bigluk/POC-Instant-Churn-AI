import numpy as np
from common_utils import fetch_dataset_from_csv, prepare_dataset, build_reports
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from xgboost import XGBClassifier


def apply_xg_boost(X, y, use_smote=False):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    # RandomizedSearchCV per XGBoost
    if use_smote:
        model = XGBClassifier(random_state=42, eval_metric='logloss')
    else:
        model = XGBClassifier(
            scale_pos_weight=len(y_train[y_train == 0]) / len(y_train[y_train == 1]),
            random_state=42, eval_metric='logloss')

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
                                     n_iter=40,  # prova 30 combinazioni casuali
                                     scoring='f1',  # metrica più adatta in caso di sbilanciamento
                                     cv=3,
                                     verbose=1,
                                     random_state=42,
                                     n_jobs=-1)

    if use_smote:
        # --- Applica SMOTE SOLO al training set ---
        smote = SMOTE(random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
        print("Distribuzione classi prima di SMOTE:", np.bincount(y_train))
        print("Distribuzione classi dopo SMOTE:", np.bincount(y_train_res))
        grid_search.fit(X_train_res, y_train_res)
    else:
        grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    print("Migliori parametri XGBoost:", grid_search.best_params_)

    # Predizioni
    # y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba > 0.4).astype(int)  # soglia 0.4 invece di 0.5

    build_reports(y_pred, y_test)


if __name__ == '__main__':
    bank_marketing = fetch_dataset_from_csv('../data/csv/bank-full-balanced.csv')
    print(bank_marketing)
    X, y = prepare_dataset(bank_marketing)
    # save_into_csv(X, y)
    # plot_umap_2d(X, y)

    # apply_xg_boost(X, y, False)
    # apply_xg_boost(X, y, True)
    # print("\n\n")

    apply_xg_boost(X, y, use_smote=False)
