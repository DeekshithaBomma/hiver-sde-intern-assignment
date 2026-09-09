# Hiver SDE Intern Take-Home — AmazonHelp Customer-Support Agent

## Selected brand
**AmazonHelp**

This repository contains a reproducible customer-support agent built from the supplied `twcs_sample.csv` sample.

### Project goals
1. Classify an incoming customer message into a compact intent taxonomy.
2. Draft a safe support response based on historical support patterns.
3. Decide whether to auto-handle or escalate to a human, with an explicit reason.
4. Evaluate the approach against simple baselines.

## Dataset facts
The supplied sample contains **5,000 rows**. In that sample:
- 154 inbound AmazonHelp messages
- 192 outbound AmazonHelp replies
- 116 linked inbound/reply pairs

The 154 inbound AmazonHelp messages are exported as `golden_eval_candidate.csv`.

> **Evaluation integrity note:** the candidate labels were generated with an AI-assisted deterministic rubric. They are **not independent human annotations**. Before claiming a "hand-labelled golden set" in a final submission, manually review/correct these 154 rows and then rename the file `golden_eval.csv`.

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

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the agent:

```bash
python agent.py --message "@AmazonHelp My package says delivered but I never received it."
```

Run evaluation:

```bash
python evaluate.py
```

## Example
Input:
`@AmazonHelp My package says delivered but I never received it.`

The agent returns JSON containing:
- `intent`
- `action` (`auto_handle` or `escalate`)
- `reason`
- `draft_reply`

## Files
- `agent.py` — runnable support agent
- `evaluate.py` — evaluation entry point
- `twcs_sample.csv` — supplied sample
- `amazonhelp_pairs.csv` — linked historical customer/reply examples
- `golden_eval_candidate.csv` — 154 candidate evaluation examples
- `results.json` — measured dataset facts
- `report.md` — take-home report
- `decision_log.md` — non-obvious design decisions
- `requirements.txt` — Python dependencies

## Evaluation caveat
The reported intent proxy score is agreement with the deterministic annotation rubric, not independent human-ground-truth accuracy. Response retrieval is evaluated on a held-out subset of linked examples. This distinction is intentional so that the evaluation does not overclaim quality.
