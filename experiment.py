from pathlib import Path
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, confusion_matrix, classification_report
from expert_rules import expert
from weighted_rules import weighted, explain
ROOT=Path(__file__).resolve().parent
COLS=['buying','maint','doors','persons','lug_boot','safety','class']
LABELS=['unacc','acc','good','vgood']
def evaluate(data):
    y=data['class']; out={}
    for name,p in [('expert',data.apply(expert,axis=1)),('weighted',data.apply(weighted,axis=1)),('majority_baseline',['unacc']*len(data))]:
        out[name]={'accuracy':accuracy_score(y,p),'balanced_accuracy':balanced_accuracy_score(y,p),'macro_f1':f1_score(y,p,labels=LABELS,average='macro'),'weighted_f1':f1_score(y,p,average='weighted'),'confusion_matrix':confusion_matrix(y,p,labels=LABELS).tolist(),'classification_report':classification_report(y,p,labels=LABELS,output_dict=True,zero_division=0)}
    return out

def main():
    data=pd.read_csv(ROOT/'data'/'Car Evaluation Dataset'/'car.data',header=None,names=COLS,dtype=str)
    assert data.shape==(1728,7)
    _,test=train_test_split(data,test_size=.25,stratify=data['class'],random_state=42)
    result=evaluate(test); folder=ROOT/'results'; folder.mkdir(exist_ok=True)
    (folder/'metrics.json').write_text(json.dumps(result,indent=2))
    full=evaluate(data); (folder/'full_dataset_metrics.json').write_text(json.dumps(full,indent=2))
    examples=[]
    for _,row in test.iterrows():
        label,score,points,reason=explain(row)
        examples.append({**row.to_dict(),'expert':expert(row),'weighted':label,'score':score,'reason':reason,**{f'points_{k}':v for k,v in points.items()}})
    pd.DataFrame(examples).to_csv(folder/'decision_examples.csv',index=False)
    repeated=[]
    for seed in range(20):
        _,subset=train_test_split(data,test_size=.25,stratify=data['class'],random_state=seed)
        for name,m in evaluate(subset).items():
            repeated.append({'seed':seed,'model':name,**{k:v for k,v in m.items() if isinstance(v,float)}})
    r=pd.DataFrame(repeated); r.to_csv(folder/'repeated_holdout.csv',index=False)
    summary=r.groupby('model').agg({k:['mean','std'] for k in ['accuracy','balanced_accuracy','macro_f1']}); (folder/'robustness_summary.txt').write_text(summary.to_string())
    print(json.dumps({n:{k:round(v,4) for k,v in m.items() if isinstance(v,float)} for n,m in result.items()},indent=2)); print(summary)
if __name__=='__main__': main()
