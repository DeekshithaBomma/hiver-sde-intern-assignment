# Decision Log

1. **Selected AmazonHelp.** It has 154 inbound examples in the supplied 5,000-row sample, which fits the requested 150–250 evaluation-set size.
2. **Used inbound messages as evaluation candidates.** This avoids inventing customer text.
3. **Kept the taxonomy compact.** Eleven intents are enough to separate the most actionable support themes without creating dozens of sparse labels.
4. **Separated delivery tracking from non-receipt.** “Where is my package?” and “tracking says delivered but it is missing” require different workflows.
5. **Escalated payment/refund cases.** These can require account verification and transaction-specific action.
6. **Escalated account-access cases.** The agent should never request passwords or sensitive credentials in public replies.
7. **Escalated repeated unresolved contacts.** Repeated failures indicate that routing to a human owner is more valuable than another generic bot reply.
8. **Added legal/fraud/counterfeit triggers.** These are high-risk and should not be handled solely by a lightweight classifier.
9. **Used historical support replies as grounding evidence.** The dataset contains real brand responses, so response style and routing patterns can be learned without fabricating policy.
10. **Used deterministic rules for the baseline agent.** This keeps the demo reproducible and runnable without a paid API key.
11. **Kept the public reply conservative.** The system avoids promising refunds, delivery dates, or account changes it cannot verify.
12. **Included multilingual/short-message examples in evaluation.** Real Twitter support data contains very short and multilingual messages; these are useful failure cases.
13. **Added an explicit “other” and “acknowledgement” class.** Not every inbound tweet is a problem report; forcing thanks/confirmation into a problem class would create noisy automation.
14. **Reported retrieval quality separately from intent quality.** A good intent label does not guarantee a useful reply.
15. **Flagged the golden-set limitation.** The candidate labels are AI-assisted and require human review before being called hand-labelled.
