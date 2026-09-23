import csv, json, re, sys
from collections import Counter

PATTERNS = {
    "email": re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$"),
    "phone": re.compile(r"^\+?[0-9][0-9() .-]{6,}$"),
    "national_id_like": re.compile(r"^\d{5}-?\d{7}-?\d{1}$"),
}

def classify(value):
    value = value.strip()
    return [name for name, pattern in PATTERNS.items() if pattern.match(value)]

def profile(path):
    with open(path, newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise ValueError("CSV is empty")
    fields = list(rows[0])
    findings, field_stats = [], {}
    fingerprints = Counter()
    for index, row in enumerate(rows, start=2):
        fingerprints[tuple(row.get(field, "") for field in fields)] += 1
        for field, value in row.items():
            for kind in classify(value or ""):
                findings.append({"row": index, "field": field, "classification": kind})
    for field in fields:
        values = [row.get(field, "") for row in rows]
        field_stats[field] = {"null_rate": round(sum(not value.strip() for value in values)/len(rows), 3),
                              "unique_values": len(set(values))}
    duplicates = sum(count - 1 for count in fingerprints.values() if count > 1)
    score = min(100, len(findings) * 8 + duplicates * 10 + sum(int(stat["null_rate"] * 20) for stat in field_stats.values()))
    return {"rows": len(rows), "risk_score": score, "possible_sensitive_values": findings,
            "duplicate_rows": duplicates, "field_stats": field_stats,
            "recommendation": "review before external transfer" if score >= 30 else "basic review passed"}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 app.py path/to/export.csv")
    print(json.dumps(profile(sys.argv[1]), indent=2))
