import numpy as np
import pandas as pd

import csv


def generate_balanced_balance(sample, balance_stats, balance_by_job, balance_by_education):
    base_balance = np.random.normal(balance_stats[2], balance_stats[3])

    if sample['job'] in balance_by_job:
        job_adjustment = balance_by_job[sample['job']] - balance_stats[2]
        base_balance += job_adjustment * 0.5  # Partially applies the correlation

    # Adjust for education (if available in real data)
    if sample['education'] in balance_by_education:
        education_adjustment = balance_by_education[sample['education']] - balance_stats[2]
        base_balance += education_adjustment * 0.3

    # Adjust for age (general trend)
    if sample['age'] < 25:
        base_balance *= 0.7
    elif sample['age'] < 35:
        base_balance *= 0.9
    elif sample['age'] > 55:
        base_balance *= 1.1

    if sample['default'] == 'yes':
        base_balance *= 0.3
    elif sample['default'] == 'unknown':
        base_balance *= 0.8

    if sample['housing'] == 'yes':
        base_balance *= 0.9

    balance_value = max(balance_stats[0], min(balance_stats[1], base_balance))
    return int(balance_value)


def generate_synthetic_samples(original_df, num_samples=20000):
    synthetic_data = []

    # Distributions of categorical variables
    job_dist = original_df['job'].value_counts(normalize=True)
    marital_dist = original_df['marital'].value_counts(normalize=True)
    education_dist = original_df['education'].value_counts(normalize=True)
    default_dist = original_df['default'].value_counts(normalize=True)
    housing_dist = original_df['housing'].value_counts(normalize=True)
    loan_dist = original_df['loan'].value_counts(normalize=True)
    contact_dist = original_df['contact'].value_counts(normalize=True)
    month_dist = original_df['month'].value_counts(normalize=True)
    day_dist = original_df['day'].value_counts(normalize=True)
    poutcome_dist = original_df['poutcome'].value_counts(normalize=True)

    # Statistics for numeric variables
    age_stats = (original_df['age'].min(), original_df['age'].max(), original_df['age'].mean(),
                 original_df['age'].std())
    duration_stats = (original_df['duration'].min(), original_df['duration'].max(), original_df['duration'].mean(),
                      original_df['duration'].std())
    campaign_stats = (original_df['campaign'].min(), original_df['campaign'].max(), original_df['campaign'].mean(),
                      original_df['campaign'].std())
    balance_stats = (original_df['balance'].min(), original_df['balance'].max(), original_df['balance'].mean(),
                     original_df['balance'].std())

    # Analyze correlations between balance and other variables
    balance_by_job = original_df.groupby('job')['balance'].mean()
    balance_by_education = original_df.groupby('education')['balance'].mean()

    for _ in range(num_samples):
        sample = {
            'age': max(18, min(95, int(np.random.normal(age_stats[2], age_stats[3])))),
            'job': np.random.choice(job_dist.index, p=job_dist.values),
            'marital': np.random.choice(marital_dist.index, p=marital_dist.values),
            'education': np.random.choice(education_dist.index, p=education_dist.values),
            'default': np.random.choice(default_dist.index, p=default_dist.values),
            'housing': np.random.choice(housing_dist.index, p=housing_dist.values),
            'loan': np.random.choice(loan_dist.index, p=loan_dist.values),
            'contact': np.random.choice(contact_dist.index, p=contact_dist.values),
            'day': np.random.choice(day_dist.index, p=day_dist.values),
            'month': np.random.choice(month_dist.index, p=month_dist.values),
            'duration': max(0, int(np.random.normal(duration_stats[2], duration_stats[3]))),
            'campaign': max(1, min(50, int(np.random.normal(campaign_stats[2], campaign_stats[3])))),
            'pdays': 999,
            'previous': 0,
            'poutcome': np.random.choice(poutcome_dist.index, p=poutcome_dist.values),
            'y': 'yes'
        }

        # Realistic balance generation based on real statistics
        balance_value = generate_balanced_balance(sample, balance_stats, balance_by_job, balance_by_education)
        sample_with_balance = {}
        for key in sample.keys():
            sample_with_balance[key] = sample[key]
            if key == 'default':
                sample_with_balance['balance'] = int(balance_value)  # aggiungi balance dopo default

        # Adjust correlations (e.g., age and job)
        if sample_with_balance['age'] > 50 and sample_with_balance['job'] == 'student':
            sample_with_balance['job'] = np.random.choice(['retired', 'admin.', 'technician'])
        if sample_with_balance['age'] < 25 and sample_with_balance['job'] == 'retired':
            sample_with_balance['job'] = np.random.choice(['student', 'unemployed', 'blue-collar'])

        synthetic_data.append(sample_with_balance)

    return pd.DataFrame(synthetic_data)


if __name__ == '__main__':
    base_path = '\\csv'
    df_original = pd.read_csv('%s\\bank-full.csv' % base_path, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    df_yes = df_original[df_original['y'] == "yes"]

    df_synthetic = generate_synthetic_samples(df_yes, 20000)
    cols_int = ['age', 'balance', 'duration', 'campaign', 'day', 'pdays', 'previous']
    df_synthetic[cols_int] = df_synthetic[cols_int].astype('int64')
    df_original[cols_int] = df_original[cols_int].astype('int64')

    df_balanced = pd.concat([df_original, df_synthetic], ignore_index=True)
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

    balanced_filename = f'{base_path}\\bank-full-balanced.csv'
    df_balanced.to_csv(balanced_filename, sep=';', index=False, quoting=csv.QUOTE_NONNUMERIC)
