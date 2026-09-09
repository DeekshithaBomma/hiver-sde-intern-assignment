# Hiver SDE Intern Take-Home — Customer Support Agent

## Selected brand
**AmazonHelp**

The supplied `twcs_sample.csv` contains 5,000 rows. Within that sample there are **154 inbound AmazonHelp messages** and **192 AmazonHelp support replies**, so AmazonHelp is a practical choice for the required 150–250-example evaluation set.

## What this project does
1. Classifies an incoming customer message into a small intent taxonomy.
2. Produces a support reply grounded in patterns seen in historical AmazonHelp replies.
3. Decides between `auto_handle` and `escalate` using conservative rules for billing, account access, legal/fraud concerns, and repeated unresolved contacts.
4. Includes a 154-example **AI-assisted candidate** evaluation set and 116 linked customer/reply pairs.

## Important evaluation note
The assignment asks for a **hand-labelled** golden set. The supplied candidate set was created with an AI-assisted deterministic annotation rubric. **Review/correct the 154 rows manually before submitting if you want to claim it is hand-labelled.** Do not describe the current file as independently human-labelled.

## Run
```bash
pip install -r requirements.txt
python src/agent.py --message "@AmazonHelp My package says delivered but I never received it."
```

Example output:
```json
{
  "brand": "AmazonHelp",
  "intent": "delivery_not_received",
  "action": "auto_handle",
  "reason": "Routine support request with no explicit high-risk trigger.",
  "draft_reply": "I'm sorry the package hasn't arrived..."
}
```

Run evaluation:
```bash
python src/evaluate.py
```

## Repository structure
- `src/agent.py` — runnable support agent
- `src/evaluate.py` — evaluation entry point
- `data/twcs_sample.csv` — supplied sample data
- `data/amazonhelp_pairs.csv` — linked customer/reply examples
- `eval/golden_eval_candidate.csv` — 154 candidate evaluation examples
- `reports/report.md` — take-home report
- `reports/results.json` — measured dataset/evaluation facts
- `reports/decision_log.md` — non-obvious design decisions

## Intent taxonomy
- delivery_tracking
- delivery_not_received
- refund_payment
- order_cancel_change
- account_access
- prime_membership
- promotion_preorder
- product_support
- human_escalation
- acknowledgement
- other
