import json, re, math
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def normalize(s):
    s = re.sub(r"https?://\S+", " ", str(s))
    s = re.sub(r"@\w+", " ", s)
    return re.sub(r"\s+", " ", s.lower()).strip()

def rouge_l_f1(a,b):
    aa, bb = normalize(a).split(), normalize(b).split()
    if not aa or not bb: return 0.0
    dp = [[0]*(len(bb)+1) for _ in range(len(aa)+1)]
    for i in range(1,len(aa)+1):
        for j in range(1,len(bb)+1):
            dp[i][j] = dp[i-1][j-1]+1 if aa[i-1]==bb[j-1] else max(dp[i-1][j],dp[i][j-1])
    l=dp[-1][-1]; p=l/len(bb); r=l/len(aa)
    return 0.0 if p+r==0 else 2*p*r/(p+r)

def main():
    result=json.loads((ROOT/"reports"/"results.json").read_text())
    print(json.dumps(result, indent=2))
    print("\nEvaluation caveat: intent proxy accuracy is agreement with the deterministic annotation rubric.")
    print("The candidate golden set must be human-reviewed before being described as hand-labelled.")

if __name__=="__main__":
    main()
