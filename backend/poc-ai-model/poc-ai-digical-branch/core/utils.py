import pandas as pd


def prepare_sample(df):
    df = df.copy()

    binary_cols = ["default", "housing", "loan"]
    df[binary_cols] = df[binary_cols].map(lambda x: 1 if x == "yes" else 0)

    bins = [0, 25, 35, 50, 65, 100]
    labels = ["<25", "25-35", "36-50", "51-65", "65+"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
    df = df.drop("age", axis=1)

    # One-Hot encoding
    categorical_cols = ["job", "marital", "education", "age_group"]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=False, dtype=int)

    # Generated columns during model training phase
    expected_columns = ['default', 'balance', 'housing', 'loan', 'job_blue-collar',
                        'job_entrepreneur', 'job_housemaid', 'job_management', 'job_retired',
                        'job_self-employed', 'job_services', 'job_student', 'job_technician',
                        'job_unemployed', 'job_unknown', 'marital_married', 'marital_single',
                        'education_secondary', 'education_tertiary', 'education_unknown',
                        'age_group_25-35', 'age_group_36-50', 'age_group_51-65',
                        'age_group_65+']
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[expected_columns]
    return df
