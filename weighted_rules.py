WEIGHTS = {
    'buying': {'vhigh':0,'high':1,'med':2,'low':3},
    'maint': {'vhigh':0,'high':1,'med':2,'low':3},
    'doors': {'2':0,'3':1,'4':2,'5more':2},
    'persons': {'2':0,'4':2,'more':3},
    'lug_boot': {'small':0,'med':1,'big':2},
    'safety': {'low':0,'med':2,'high':4},
}
def explain(row):
    points = {k: values[row[k]] for k, values in WEIGHTS.items()}
    score = sum(points.values())
    if row['safety']=='low' or row['persons']=='2':
        label, reason = 'unacc', 'Mandatory rejection'
    elif score < 9: label, reason = 'unacc', 'Score below 9'
    elif score < 13: label, reason = 'acc', 'Score 9–12'
    elif score < 15: label, reason = 'good', 'Score 13–14'
    else: label, reason = 'vgood', 'Score 15–17'
    return label, score, points, reason

def weighted(row):
    return explain(row)[0]
