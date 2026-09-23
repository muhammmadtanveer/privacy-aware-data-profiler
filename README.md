# Privacy-Aware Data Profiler

A dependency-free Python tool that profiles CSV exports before they enter an analytics or marketing-automation workflow.

## Why it matters

CRM and ad-platform exports can quietly contain personal data, missing identifiers, duplicate records, and inconsistent fields. This project turns those risks into an auditable report before data is shared, imported, or used for analysis.

## Capabilities

- Detects likely email addresses, phone numbers, and national-ID-like values
- Reports null rates, duplicate rows, and field cardinality
- Assigns a transparent data-risk score
- Produces JSON suitable for a pipeline quality gate
- Uses only Python's standard library

## Run

```bash
python3 app.py data/sample_leads.csv
```

## Responsible use

This tool identifies potential exposure; it does not make legal compliance decisions. Use synthetic or authorized data only, and review results before transferring datasets to external systems.
