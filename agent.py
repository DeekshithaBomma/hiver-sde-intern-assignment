from __future__ import annotations
import argparse, json, math, re
from collections import Counter
from pathlib import Path
import pandas as pd

BRAND = "AmazonHelp"

INTENTS = [
    "delivery_tracking", "delivery_not_received", "refund_payment",
    "order_cancel_change", "account_access", "prime_membership",
    "promotion_preorder", "product_support", "human_escalation",
    "acknowledgement", "other"
]

def normalize(s: str) -> str:
    s = re.sub(r"https?://\S+", " ", str(s))
    s = re.sub(r"@\w+", " ", s)
    return re.sub(r"\s+", " ", s.lower()).strip()

def classify(text: str) -> str:
    s = normalize(text)
    if any(k in s for k in ["corporate","corp","supervisor","manager","escalat","executive",
                            "no resolution","customer service again","call center","clueless",
                            "police matter","legal"]):
        return "human_escalation"
    if any(k in s for k in ["refund","charged","charge","payment","billing","credit card","money back","£","$"]):
        return "refund_payment"
    if any(k in s for k in ["cancel","cancellation","re-order","reorder","change my order","modify order"]):
        return "order_cancel_change"
    if any(k in s for k in ["locked","login","log in","password","account","email address",
                            "amazon household","sign in","verification code"]):
        return "account_access"
    if any(k in s for k in ["prime","membership","renewed","renewal","trial"]):
        return "prime_membership"
    if any(k in s for k in ["pre-order","preorder","bonus","20% off","discount","promo","promotion","deal"]):
        return "promotion_preorder"
    if any(k in s for k in ["echo","fire tv","firetv","kindle","alexa","device","wifi","bluetooth",
                            "won't turn","won’t turn","screen","app"]):
        return "product_support"
    if any(k in s for k in ["delivered","delivery","deliver","shipping","shipped","courier",
                            "package","parcel","order","out for delivery","tracking","dispatch","arrive","received"]):
        if any(k in s for k in ["not delivered","didn't arrive","did not arrive","haven't received",
                                "not received","where is my","still no","lost","missing","late",
                                "overdue","no show","never received","not dlvd","un-delivered"]):
            return "delivery_not_received"
        return "delivery_tracking"
    if any(k in s for k in ["thank","thanks","okay","ok","danke","gracias","worked","sorted","all good",
                            "already handled"]):
        return "acknowledgement"
    return "other"

def should_escalate(text: str, intent: str) -> tuple[bool, str]:
    s = normalize(text)
    if intent in {"human_escalation", "refund_payment", "account_access"}:
        return True, "High-risk or identity/payment-sensitive issue; human review is safer."
    if any(k in s for k in ["police","legal","lawsuit","fraud","stolen","counterfeit"]):
        return True, "Potential legal, fraud, theft, or counterfeit issue."
    if any(k in s for k in ["again","3-4 times","many calls","no resolution","nobody","no one responds"]):
        return True, "Repeated/failed support contact suggests the case needs human ownership."
    return False, "Routine support request with no explicit high-risk trigger."

def reply_for(intent: str) -> str:
    canned = {
        "delivery_tracking": "Sorry for the wait. Please share the order/tracking details through Amazon support so the current delivery status can be checked.",
        "delivery_not_received": "I'm sorry the package hasn't arrived. Please use Amazon support to provide the order details so the delivery can be investigated.",
        "refund_payment": "Because this involves payment or a refund, please contact Amazon support through the secure account channel so the transaction can be verified.",
        "order_cancel_change": "Please open the order in your Amazon account and check the available cancellation or change options. If they are unavailable, support can review the order.",
        "account_access": "For account or sign-in issues, please use the secure Amazon account-recovery/support flow. Do not post passwords or payment details here.",
        "prime_membership": "You can review or manage Prime membership from your Amazon account. If you were charged unexpectedly, please use the secure support channel for a billing review.",
        "promotion_preorder": "Promotion and preorder eligibility can depend on the item and offer terms. Please share the product/offer details through Amazon support for verification.",
        "product_support": "Sorry you're having trouble with the product. Please share the device/model and symptoms through Amazon support so troubleshooting can be provided.",
        "acknowledgement": "You're welcome, and I'm glad the issue is sorted.",
        "human_escalation": "Thanks for explaining the issue. This needs human support ownership; please use Amazon's secure phone/chat channel so the case can be reviewed.",
        "other": "Thanks for reaching out. Please provide a little more detail about the issue, without sharing sensitive account or payment information."
    }
    return canned[intent]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--message", required=True)
    args = ap.parse_args()
    intent = classify(args.message)
    esc, reason = should_escalate(args.message, intent)
    out = {
        "brand": BRAND,
        "intent": intent,
        "action": "escalate" if esc else "auto_handle",
        "reason": reason,
        "draft_reply": reply_for(intent)
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
