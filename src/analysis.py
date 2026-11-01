from pathlib import Path
import json, pandas as pd, numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

NUMERIC = ["flight_number","payload_mass","block","reused_count","flights","gridfins","legs"]
CATEGORICAL = ["orbit","launch_site"]

def lcg(seed=42):
    x = seed
    while True:
        x = (1664525*x + 1013904223) % (2**32)
        yield x / 2**32

def build_features(df):
    d = df.copy()
    for c in ["gridfins","legs"]:
        d[c] = d[c].astype(str).str.lower().eq("true").astype(float)
    for c in ["flight_number","payload_mass","block","reused_count","flights"]:
        d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0.0)
    levels = {c: sorted(d[c].fillna("Unknown").astype(str).unique().tolist()) for c in CATEGORICAL}
    cols = NUMERIC.copy()
    X = d[NUMERIC].astype(float).to_numpy().tolist()
    for c in CATEGORICAL:
        vals = d[c].fillna("Unknown").astype(str).tolist()
        for lv in levels[c][1:]:
            cols.append(f"{c}_{lv}")
            X = [row + [1.0 if v == lv else 0.0] for row, v in zip(X, vals)]
    return np.asarray(X, dtype=float), cols

def run_analysis(csv_path="data/dataset_part_1.csv"):
    df = pd.read_csv(csv_path)
    df = df[df["class"].isin([0,1])].copy().reset_index(drop=True)
    y = df["class"].astype(int).to_numpy()
    X, feature_names = build_features(df)
    rng = lcg(42)
    keys = [next(rng) for _ in range(len(df))]
    order = np.argsort(keys)
    n_test = round(len(df)*0.2)
    test_idx, train_idx = order[:n_test], order[n_test:]
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    mu = X_train.mean(axis=0)
    sd = X_train.std(axis=0)
    sd[sd == 0] = 1.0
    A = np.column_stack([np.ones(len(X_train)), (X_train-mu)/sd])
    B = np.column_stack([np.ones(len(X_test)), (X_test-mu)/sd])
    w = np.zeros(A.shape[1])
    for _ in range(7000):
        z = np.clip(A @ w, -25, 25)
        p = 1/(1+np.exp(-z))
        grad = A.T @ (p-y_train)/len(y_train)
        grad[1:] += 0.02*w[1:]
        w -= 0.025*grad
    pred = (1/(1+np.exp(-np.clip(B@w,-25,25))) >= 0.5).astype(int)
    result = {
        "rows": int(len(df)), "successes": int(y.sum()), "failures": int(len(y)-y.sum()),
        "success_rate_pct": round(float(y.mean()*100),1),
        "train_rows": int(len(train_idx)), "test_rows": int(len(test_idx)),
        "accuracy_pct": round(accuracy_score(y_test,pred)*100,1),
        "precision_pct": round(precision_score(y_test,pred,zero_division=0)*100,1),
        "recall_pct": round(recall_score(y_test,pred,zero_division=0)*100,1),
        "f1_pct": round(f1_score(y_test,pred,zero_division=0)*100,1),
        "confusion_matrix": confusion_matrix(y_test,pred).tolist(),
        "feature_names": feature_names,
        "coefficients": w.tolist()
    }
    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/model_metrics.json").write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
    return df, result

if __name__ == "__main__":
    run_analysis()
