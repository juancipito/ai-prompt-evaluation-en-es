from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "sample_synthetic_data.csv"
WEIGHTS = {
    "helpfulness": 0.25,
    "accuracy": 0.25,
    "safety": 0.20,
    "clarity": 0.15,
    "bilingual_quality": 0.15,
}


def weighted_score(row: pd.Series) -> float:
    return round(sum(row[col] * weight for col, weight in WEIGHTS.items()), 2)


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    df["weighted_score"] = df.apply(weighted_score, axis=1)
    df["needs_review"] = (df["safety"] < 4) | (df["accuracy"] < 3) | (df["weighted_score"] < 3.5)
    print("Prompt evaluation summary")
    print(df.groupby(["language", "category"])["weighted_score"].mean().round(2))
    print("\nRows needing review:")
    print(df[df["needs_review"]][["prompt_id", "language", "category", "weighted_score", "risk_flag"]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
