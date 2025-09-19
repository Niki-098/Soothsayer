import re

def find_key_metrics_in_text(text: str, keywords=None):
    if keywords is None:
        keywords = ["revenue", "net income", "profit", "gross profit", "expenses", "total assets", "cash"]
    metrics = {}
    t = text.lower()
    for kw in keywords:
        idx = t.find(kw.lower())
        if idx != -1:
            snippet = t[idx: idx + 200]
            nums = re.findall(r"[\d\.,]+(?:\s*(?:thousand|million|billion|mn|bn))?", snippet, flags=re.IGNORECASE)
            metrics[kw] = nums[0] if nums else snippet.strip().split("\n")[0]
    return metrics
