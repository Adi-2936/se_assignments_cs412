# L6 L7 39 Password Policy Checker

Lab 7: Fuzz Testing

## About

A small Python module that classifies password characters, splits credentials, and measures digit density. The Lab 7 version adds defensive input validation and Hypothesis fuzz tests for all three functions.

## Files

| File | Description |
|------|-------------|
| `password_policy.py` | Fixed application with defensive input validation |
| `test_password_policy.py` | Completed deterministic and Hypothesis fuzz tests |
| `PES2UG24CS412_SE_Lab07_Report.pdf` | Final laboratory report |
| `screenshots/` | Genuine terminal evidence from before and after the fixes |

## Verification

```powershell
python -m pip install pytest hypothesis
python -m pytest -v test_password_policy.py
```

The completed test suite contains six tests and passes all deterministic and fuzz checks.
