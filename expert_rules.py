
def expert(row):
    """Hand-crafted, prioritised IF-THEN decision list; no fitted parameters."""
    if row['safety'] == 'low' or row['persons'] == '2': return 'unacc'
    if row['safety'] == 'med' and row['lug_boot'] == 'small': return 'unacc'
    if row['buying'] == 'vhigh' and row['maint'] == 'vhigh': return 'unacc'
    if row['safety'] == 'high' and row['persons'] == 'more' and row['lug_boot'] == 'big' and row['buying'] == 'low' and row['maint'] == 'low': return 'vgood'
    if row['safety'] == 'high' and row['buying'] in ('low','med') and row['maint'] in ('low','med') and row['lug_boot'] != 'small': return 'good'
    return 'acc'

