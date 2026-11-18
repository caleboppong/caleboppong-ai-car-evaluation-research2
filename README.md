
# Comparative Investigation of Prioritised and Weighted Rule-Based Inference for Vehicle Acceptability Classification

## Project Overview

This research investigates the effectiveness of two deterministic rule-based artificial intelligence systems for vehicle acceptability classification using the UCI Car Evaluation dataset.

The primary objective is to determine whether weighted rule-based inference improves minority-class recognition compared with prioritised IF–THEN inference.

## Research Problem

The Car Evaluation dataset contains an imbalanced distribution of vehicle acceptability categories. Consequently, overall classification accuracy may conceal poor recognition of underrepresented classes.

## Research Question

To what extent does weighted rule-based inference improve vehicle acceptability classification, particularly minority-class recognition, compared with prioritised IF–THEN inference?

## Proposed Solution

The proposed solution combines weighted attribute scoring with mandatory rejection rules to evaluate vehicle acceptability while maintaining transparent and explainable decision-making.

## Dataset

Source: UCI Machine Learning Repository — Car Evaluation.

https://doi.org/10.24432/C5JP48

The dataset contains 1,728 records and six categorical input attributes.

| Classification | Records |
|---|---:|
| Unacceptable (unacc) | 1,210 |
| Acceptable (acc) | 384 |
| Good (good) | 69 |
| Very good (vgood) | 65 |
| Total | 1,728 |

### Input Attributes

- Buying price
- Maintenance cost
- Number of doors
- Passenger capacity
- Luggage boot capacity
- Safety

## Algorithm A: Prioritised IF–THEN Inference

Implemented in `expert_rules.py`.

This algorithm evaluates predefined conditional rules sequentially. The first applicable rule determines the vehicle classification.

The approach provides transparent decision-making through explicit rule prioritisation.

## Algorithm B: Weighted Rule-Based Inference

Implemented in `weighted_rules.py`.

This algorithm assigns numerical points to each vehicle attribute and calculates an aggregate score.

### Scoring Knowledge Base

| Attribute | Assigned points |
|---|---|
| Buying price | vhigh=0, high=1, med=2, low=3 |
| Maintenance | vhigh=0, high=1, med=2, low=3 |
| Doors | 2=0, 3=1, 4=2, 5more=2 |
| Passenger capacity | 2=0, 4=2, more=3 |
| Luggage boot | small=0, med=1, big=2 |
| Safety | low=0, med=2, high=4 |

The maximum aggregate score is 17.

### Classification Thresholds

| Score | Classification |
|---|---|
| Below 9 | unacc |
| 9–12 | acc |
| 13–14 | good |
| 15–17 | vgood |

### Mandatory Rejection Rules

A vehicle is classified as unacceptable regardless of its aggregate score when:

- Safety is low.
- Passenger capacity is two.

Neither algorithm requires model training. Both use explicitly defined knowledge bases and deterministic inference mechanisms.

## Experimental Methodology

The research evaluates three classification approaches:

1. Prioritised IF–THEN inference.
2. Weighted rule-based inference.
3. Majority-class baseline.

The experimental procedure includes:

- A stratified evaluation subset of 432 records.
- A fixed random seed of 42.
- Full dataset evaluation using 1,728 records.
- Twenty repeated stratified subset evaluations.
- Functional and boundary testing.
- Sensitivity analysis using five scoring configurations.

## Experimental Results

| Metric | Prioritised | Weighted | Majority baseline |
|---|---:|---:|---:|
| Accuracy | 0.8356 | 0.8519 | 0.7014 |
| Balanced accuracy | 0.4594 | 0.7117 | 0.2500 |
| Macro F1 | 0.4342 | 0.6795 | 0.2061 |
| Weighted F1 | 0.8222 | 0.8645 | 0.5783 |

The weighted system improved balanced accuracy by 25.23 percentage points and macro F1 by 24.53 percentage points.

The findings demonstrate the importance of evaluating class-sensitive performance rather than relying exclusively on overall accuracy.

## Repeated Evaluation

Twenty repeated stratified subset evaluations were conducted to investigate performance variability.

| Measurement | Prioritised | Weighted |
|---|---:|---:|
| Mean accuracy | 0.836343 | 0.845023 |
| Accuracy SD | 0.015466 | 0.014897 |
| Mean balanced accuracy | 0.491080 | 0.707979 |
| Balanced accuracy SD | 0.017498 | 0.043628 |
| Mean macro F1 | 0.470530 | 0.676001 |
| Macro F1 SD | 0.021378 | 0.038470 |

The weighted system achieved higher mean performance, although its class-sensitive measurements exhibited greater variability.

## Functional and Boundary Testing

The `test_algorithms.py` programme contains 16 unit tests covering:

- Prioritised rule behaviour.
- Classification score boundaries.
- Mandatory safety rejection.
- Mandatory passenger capacity rejection.
- Consistency of weighted scoring and classification.

All 16 unit tests passed during local execution.

## Sensitivity Analysis

The `sensitivity_analysis.py` programme investigates the effects of modifying the high-safety score and classification thresholds.

| Configuration | Accuracy | Balanced accuracy | Macro F1 |
|---|---:|---:|---:|
| Original | 0.8519 | 0.7117 | 0.6795 |
| Reduced safety score | 0.8565 | 0.6317 | 0.5962 |
| Increased safety score | 0.8218 | 0.7067 | 0.6329 |
| Lower thresholds | 0.7894 | 0.7193 | 0.6173 |
| Higher thresholds | 0.8657 | 0.5795 | 0.5730 |

The original configuration achieved the highest macro F1 among the five tested configurations.

The higher-threshold configuration achieved the highest overall accuracy but considerably lower balanced accuracy.

These findings illustrate the trade-off between overall accuracy and minority-class recognition.

## Project Structure

    Rule_Based_Comparison/
    ├── data/
    ├── results/
    ├── AI_Assessment1_Testing_Evidence/
    ├── expert_rules.py
    ├── weighted_rules.py
    ├── experiment.py
    ├── sensitivity_analysis.py
    ├── test_algorithms.py
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## Installation and Execution

### Clone the Repository

    git clone https://github.com/caleboppong/caleboppong-ai-car-evaluation-research2.git
    cd caleboppong-ai-car-evaluation-research2

### Create a Virtual Environment

    python -m venv .venv

### Activate on Windows PowerShell

    .\.venv\Scripts\Activate.ps1

### Install Dependencies

    python -m pip install -r requirements.txt

### Execute the Comparative Experiment

    python experiment.py

### Execute Unit Tests

    python -m unittest test_algorithms -v

### Execute Sensitivity Analysis

    python sensitivity_analysis.py

## Experimental Evidence

Generated research artefacts are stored in the `results` directory.

| File | Description |
|---|---|
| metrics.json | Primary comparative results |
| full_dataset_metrics.json | Full dataset evaluation |
| decision_examples.csv | Individual classification explanations |
| repeated_holdout.csv | Repeated evaluation results |
| robustness_summary.txt | Statistical summaries |
| sensitivity_analysis.csv | Sensitivity comparison |
| sensitivity_summary.txt | Formatted sensitivity results |
| sensitivity_execution.txt | Sensitivity execution evidence |
| unit_test_results.txt | Functional and boundary test results |

## Research Limitations

- The investigation uses a single benchmark dataset.
- The scoring weights and thresholds are manually specified.
- Repeated evaluation subsets may overlap.
- Sensitivity experiments use the same primary evaluation subset.
- The two algorithms differ in both rule content and inference mechanisms.
- Statistical significance has not been established.
- The results do not establish real-world vehicle safety or universal classifier superiority.

## Conclusion

The experimental findings demonstrate that weighted rule-based inference can improve class-sensitive classification performance on the selected dataset while retaining interpretable decision-making.

Nevertheless, the sensitivity analysis demonstrates that performance depends on the selected weights and thresholds.

Further independent evaluation is required before establishing broader generalisability.

## Reference

Bohanec, M. (1997) Car Evaluation [Dataset].
UCI Machine Learning Repository.
https://doi.org/10.24432/C5JP48

## Author

Caleb Oppong

Module: CPU5006-20 Artificial Intelligence

Assessment 1: Rule-Based AI Scientific Research Paper

Academic Year: 2026–2027
