# Prioritised versus weighted rule-based vehicle classification

Development experiment for CPU5006-20. Original expert rules retained. Weighted rules are proposed manually specified ordinal points and thresholds, not fitted parameters or recovered DEX rules. Safety and seating are mandatory rejection conditions. Safety has the largest individual maximum contribution (4); affordability and capacity contribute up to 3 each; doors and luggage up to 2 each. Thresholds 9, 13 and 15 are heuristic design choices, not empirically established optimal values. Both classifiers are fixed; the comparison changes rule content as well as inference strategy, so cannot isolate the causal effect of aggregation alone.

Run `python -m pip install -r requirements.txt` and `python experiment.py`. The script evaluates the same stratified 432 records (seed 42), the entire provided dataset, and 20 repeated stratified subsets (seeds 0–19). No training is required. Repeated subsets overlap and are not independent. These are descriptive comparisons, not proof of statistical significance or generalisation to real vehicles. Review and justify the proposed rules before adopting them; changes after inspecting results must be disclosed as exploratory.

Results include class-specific metrics, confusion matrices (label order unacc, acc, good, vgood), and score explanations. Original decision-tree research remains separate.

