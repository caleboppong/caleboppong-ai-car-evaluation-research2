from copy import deepcopy
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    classification_report
)

from weighted_rules import WEIGHTS, weighted
from experiment import ROOT, COLS, LABELS



CONFIGURATIONS = [
    ("Original", 4, (9, 13, 15)),
    ("Reduced safety weight", 3, (9, 13, 15)),
    ("Increased safety weight", 5, (9, 13, 15)),
    ("Lower thresholds", 4, (8, 12, 14)),
    ("Higher thresholds", 4, (10, 14, 16))
]


def classify(row, safety_weight, thresholds):

    weights = deepcopy(WEIGHTS)
    weights["safety"]["high"] = safety_weight

    # Apply mandatory rejection rules
    if row["safety"] == "low" or row["persons"] == "2":
        return "unacc"

    # Calculate the aggregate score
    score = sum(
        values[row[attribute]]
        for attribute, values in weights.items()
    )

    t1, t2, t3 = thresholds

    # Apply classification thresholds
    if score < t1:
        return "unacc"
    elif score < t2:
        return "acc"
    elif score < t3:
        return "good"
    else:
        return "vgood"


def evaluate(data, name, safety_weight, thresholds):

    actual = data["class"]

    predicted = data.apply(
        lambda row: classify(
            row, safety_weight, thresholds
        ),
        axis=1
    )

    report = classification_report(
        actual,
        predicted,
        labels=LABELS,
        output_dict=True,
        zero_division=0
    )

    return {
        "configuration": name,
        "safety_weight": safety_weight,
        "thresholds": str(thresholds),
        "accuracy": accuracy_score(actual, predicted),
        "balanced_accuracy": balanced_accuracy_score(
            actual, predicted
        ),
        "macro_f1": f1_score(
            actual, predicted,
            labels=LABELS,
            average="macro",
            zero_division=0
        ),
        "weighted_f1": f1_score(
            actual, predicted,
            average="weighted",
            zero_division=0
        ),
        "unacc_recall": report["unacc"]["recall"],
        "acc_recall": report["acc"]["recall"],
        "good_recall": report["good"]["recall"],
        "vgood_recall": report["vgood"]["recall"]
    }


def main():

    data = pd.read_csv(
        ROOT / "data" / "Car Evaluation Dataset" / "car.data",
        header=None,
        names=COLS,
        dtype=str
    )

    assert data.shape == (1728, 7)

    # Verify that the original configuration reproduces
    # the existing weighted algorithm on every record.
    original = data.apply(weighted, axis=1)

    reproduced = data.apply(
        lambda row: classify(row, 4, (9, 13, 15)),
        axis=1
    )

    assert original.equals(reproduced), (
        "Original configuration does not match."
    )

    print("Original configuration verification: PASSED")

    # Use exactly the same evaluation subset
    # as the original comparative experiment.
    _, test = train_test_split(
        data,
        test_size=0.25,
        stratify=data["class"],
        random_state=42
    )

    results = []

    for name, safety_weight, thresholds in CONFIGURATIONS:

        result = evaluate(
            test, name, safety_weight, thresholds
        )

        results.append(result)

    results_df = pd.DataFrame(results)

    folder = ROOT / "results"
    folder.mkdir(exist_ok=True)

    results_df.to_csv(
        folder / "sensitivity_analysis.csv",
        index=False
    )

    summary = results_df.to_string(
        index=False,
        float_format=lambda value: f"{value:.4f}"
    )

    (folder / "sensitivity_summary.txt").write_text(
        summary, encoding="utf-8"
    )

    print("\nSENSITIVITY ANALYSIS")
    print("Evaluation records:", len(test))
    print("Random seed: 42")

    print("\nPERFORMANCE COMPARISON")

    print(results_df[[
        "configuration",
        "accuracy",
        "balanced_accuracy",
        "macro_f1",
        "weighted_f1"
    ]].round(4).to_string(index=False))

    print("\nCLASS-SPECIFIC RECALL")

    print(results_df[[
        "configuration",
        "unacc_recall",
        "acc_recall",
        "good_recall",
        "vgood_recall"
    ]].round(4).to_string(index=False))

    print("\nResults successfully saved.")


if __name__ == "__main__":
    main()
