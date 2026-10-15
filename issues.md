# Lab 5: Static Code Analysis — Issues and Fixes

**File analysed:** `blood_donation.py`  
**Note:** Line numbers below refer to the original, unmodified version of `blood_donation.py` and may differ in the cleaned version.

| Issue | Type / Tool | Original line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command execution from constructed input (`B605`) | Security — Bandit, High severity | 65 | `os.system()` ran a shell command constructed using values from `phoneList`, creating a command-injection risk. | Removed shell execution. The SMS helper now clearly reports that an SMS provider must be configured before sending messages. |
| Unsafe temporary file creation (`B306`) | Security — Bandit, Medium severity | 60 | `tempfile.mktemp()` can leave a gap between choosing a filename and creating the file. | Replaced it with `tempfile.NamedTemporaryFile()` and explicit file handling. |
| Hardcoded password (`B105`) | Security — Bandit, Low severity | 5 | A password-like value was stored directly in source code. | Removed the hardcoded demo password. Credentials should be provided through a proper configuration or secrets mechanism if authentication is added. |
| Use of `assert` for input validation (`B101`) | Security — Bandit, Low severity | 18 | Python assertions can be disabled in optimized mode, so they should not enforce runtime input validation. | Replaced the assertion with an explicit condition that raises `ValueError` for an unsupported blood group. |
| Mutable default argument | Bug / Code quality — Pylint | 17 | `notes=[]` could reuse the same list across calls when no list was supplied. | Changed the default to `None` and create a fresh list inside the function. |
| Overly broad exception handler | Code quality — Pylint | 45 | `except Exception` could hide errors unrelated to an invalid patient blood group. | Removed broad exception handling and check whether `patient_group` exists in `COMPATIBLE` before calculating units. |
| Missing module and function docstrings | Code quality — Pylint | 1 and multiple function definitions | The module and several functions did not explain their purpose. | Added a module docstring and docstrings to each function. |
| Function and argument naming violations | Code quality — Pylint | 17, 27, 33, 42, 49, 53, 58, 63 | Names such as `registerDonor`, `canDonate`, and `patientGroup` did not follow `snake_case`. | Renamed functions and parameters to `snake_case` and updated the call sites. |
| Repeated equality comparison | Code quality — Pylint | 50 | The universal-group check used a repeated `or` comparison. | Used set membership: `blood_group in {"O-", "AB+"}`. |
| Line exceeded 79 characters (`E501`) | Style — Flake8 | 7 | The stock dictionary was on a line longer than the configured limit. | Split the dictionary across multiple lines. |
| Too many blank lines (`E303`) | Style — Flake8 | 58 | There were three blank lines before a top-level function. | Kept the standard two blank lines between top-level function definitions. |
| Insufficient space before inline comment (`E261`) | Style — Flake8 | 80 | The inline comment did not have the required spacing. | Added two spaces before the inline comment, or removed the unnecessary comment. |
| Missing whitespace around assignment operator (`E225`) | Style — Flake8 | 81 | The `eligible` assignment lacked spaces around `=`. | Added spaces around the operator and formatted the comprehension across multiple lines. |
| Incomplete blood-group compatibility mapping | Functional correctness | `COMPATIBLE` dictionary | The original mapping omitted `A-`, `B-`, and `AB-` as patient groups, so valid requests for these groups returned zero through the broad exception handler. | Added entries for all eight blood groups and used an explicit validity check in `units_for()`. |
| Non-positive donation units | Input validation | `record_donation()` | The original function accepted zero or negative units, which could leave stock unchanged or reduce it. | Added explicit validation that donation units must be positive. |

## Verification summary

The reported runs showed a Pylint score of **10.00/10**, no Flake8 violations, and a Bandit result of **“No issues identified”** after the syntax error was corrected. Run all three tools again against the final `blood_donation.py` included with this submission before turning it in.
