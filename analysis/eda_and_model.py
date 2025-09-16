"""analysis/eda_and_model.py
Run basic EDA (distributions, time-series) and a baseline model (RandomForest).
Usage:
  python analysis/eda_and_model.py --input data/transactions.csv --out reports/
"""
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
import joblib

def run_eda(df, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    # Simple plots
    plt.figure()
    df['tx_amount'].hist(bins=100)
    plt.title('Transaction amount distribution')
    plt.xlabel('amount')
    plt.ylabel('count')
    plt.savefig(os.path.join(out_dir, 'amount_hist.png'))
    plt.close()

    plt.figure()
    df['hour'].value_counts().sort_index().plot(kind='bar')
    plt.title('Transactions by hour')
    plt.savefig(os.path.join(out_dir, 'tx_by_hour.png'))
    plt.close()

    # Correlation heatmap for numeric columns
    plt.figure(figsize=(8,6))
    sns.heatmap(df.select_dtypes(include=['float64','int64']).corr(), annot=False)
    plt.title('Numeric Correlations')
    plt.savefig(os.path.join(out_dir, 'corr.png'))
    plt.close()

def train_model(df, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    # Simple feature set
    X = df[['tx_amount', 'hour']].fillna(0)
    y = df['is_fraud']
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    clf_report = classification_report(y_test, preds, output_dict=True)
    # Save model and report
    joblib.dump(model, os.path.join(out_dir, 'rf_model.joblib'))
    with open(os.path.join(out_dir, 'classification_report.json'), 'w') as f:
        import json
        json.dump(clf_report, f, indent=2)
    print('Model trained and saved.')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--out', default='reports')
    args = parser.parse_args()
    df = pd.read_csv(args.input, parse_dates=['event_time'])
    # quick derived features
    if 'hour' not in df.columns:
        df['hour'] = df['event_time'].dt.hour
    run_eda(df, args.out)
    train_model(df, args.out)

if __name__ == '__main__':
    main()
