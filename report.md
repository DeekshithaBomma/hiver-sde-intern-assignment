# Hiver SDE Intern Take-Home Report
## AmazonHelp Customer-Support Agent

### 1. Problem framing
The goal is to turn noisy customer-support conversations into a small, auditable support agent. I selected **AmazonHelp** from the supplied 5,000-row TWCS sample because it contains **154 inbound AmazonHelp messages and 192 outbound AmazonHelp replies**. The agent has three jobs: (1) classify the incoming message, (2) draft a reply consistent with historical support behaviour, and (3) decide whether the request is safe to auto-handle or should be owned by a human.

I use eleven intents: `delivery_tracking`, `delivery_not_received`, `refund_payment`, `order_cancel_change`, `account_access`, `prime_membership`, `promotion_preorder`, `product_support`, `human_escalation`, `acknowledgement`, and `other`.

“Good” for this brand means a reply should be empathetic, specific to the issue, avoid unsupported promises, protect account/payment information, and route high-risk or repeatedly unresolved cases to a human.

### 2. Build
The implementation is deliberately reproducible and API-free. A deterministic intent layer identifies high-signal phrases, while an escalation layer applies conservative safety rules. The reply layer uses short templates derived from recurring patterns in the historical AmazonHelp responses: delivery investigation, secure support for account/payment issues, troubleshooting for devices, and escalation for unresolved cases.

The key safety rule is that the public Twitter response should not ask for passwords, full payment details, or other secrets. Billing, account-access, fraud/legal, and repeated unresolved cases are routed to secure support/human ownership.

### 3. Evaluation design
The supplied sample provides **154 inbound AmazonHelp messages**, which I exported to `eval/golden_eval_candidate.csv`. I also linked **116 inbound messages to a historical AmazonHelp response** using the dataset's response pointers. The linked set is used for response-retrieval testing.

**Important limitation:** the candidate intent labels were generated with an AI-assisted deterministic annotation rubric. They are not independent human labels. Therefore, before submission, the 154 rows should be reviewed/corrected by a human annotator and the file should then be treated as the final golden set. The code and report intentionally make this limitation explicit rather than presenting synthetic labels as human evidence.

For the response component, an 80/20 chronological split of the 116 linked examples is used. The held-out examples are matched to the closest historical customer message and the retrieved reply is compared with the observed reply using ROUGE-L F1.

### 4. Results vs baselines
**Baseline A — majority/simple response:** always use the most common intent or a generic “please contact support” response. This is strong on no-code simplicity but cannot distinguish delivery, account, payment, or product cases.

**Baseline B — nearest historical example:** retrieve the closest historical customer message and reuse its response. This provides grounding but can transfer the wrong workflow when two messages are lexically similar.

**Proposed system:** deterministic intent + conservative escalation + policy-safe reply templates. Its primary advantage is auditability: every escalation has an explicit reason and the agent avoids unsupported account actions.

Measured facts on the supplied sample:
- 5,000 total rows.
- 154 inbound AmazonHelp evaluation candidates.
- 192 outbound AmazonHelp replies.
- 116 linked customer/reply pairs.
- Held-out retrieval test: 24 examples.
- Retrieval ROUGE-L F1: **0.0977**.

The intent “accuracy” against the current deterministic labels is **1.0000**, but this is **not an independent quality metric** because the same rubric generated those candidate labels. It must not be presented as human-validated accuracy.

### 5. Failure analysis
1. **Very short messages.** Messages such as “Yes”, “Details sent”, or “Please call me” contain too little semantic information. The classifier can overuse `acknowledgement` or `other`. Fix: maintain conversation context and require a minimum confidence threshold.
2. **Multilingual messages.** The sample contains Japanese, German, Spanish and other languages. English keyword rules can miss the intent. Fix: add language detection and multilingual embeddings/LLM classification.
3. **Overlapping intents.** A Prime renewal can also be a payment/refund issue. The current precedence rules may choose the safer but less specific class. Fix: multi-label classification followed by policy-based routing.
4. **Lexical retrieval mismatch.** Similar words can point to different workflows, especially “order”, “support”, and “account”. Fix: retrieve within an intent first and rerank with a semantic model.
5. **Historical reply is not always the ideal reply.** Real Twitter responses can be terse, repetitive, or ask the customer to move to phone/chat. Fix: use historical replies as grounding examples, then generate a response constrained by an explicit policy rubric.
6. **Repeated-contact ambiguity.** A frustrated customer may not explicitly state that earlier support failed. Fix: track thread-level history rather than classifying one tweet in isolation.
7. **The dataset is a sample.** The supplied 5,000 rows may not represent the full distribution of Amazon support. Fix: validate on a larger, temporally separated sample if available.
8. **Escalation precision/recall trade-off.** Conservative escalation reduces harmful automation but increases human workload. Fix: tune thresholds using a human-labelled escalation set and business cost weights.

### 6. Misleading headline number
The most misleading headline would be **intent accuracy = 1.0000**. It looks like a strong model-quality number, but it only measures agreement with the deterministic annotation rubric that generated the labels. It is not independent human ground truth. A more trustworthy submission should report human-reviewed intent accuracy, escalation precision/recall, and response-quality ratings.

### 7. What I would do with one more week
- Manually review the full 154-example golden set and add a second annotator for disagreement analysis.
- Replace keyword rules with a small supervised classifier or embedding-based classifier.
- Add thread context rather than classifying isolated tweets.
- Add a semantic reranker for historical replies.
- Build a proper human evaluation form with 1–5 ratings for correctness, helpfulness, tone, grounding, and escalation appropriateness.
- Calibrate an escalation threshold using the cost of false auto-handling vs unnecessary human escalation.
