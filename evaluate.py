import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    result = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    print(json.dumps(result, indent=2))
    print("\nCaveat: intent proxy accuracy is agreement with the deterministic annotation rubric, not independent human ground truth.")
    print("The candidate golden set must be human-reviewed before being described as hand-labelled.")

if __name__ == "__main__":
    main()
