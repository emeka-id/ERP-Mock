# ERP Invoice Payment Mock Desktop App

A simple desktop app for mocking invoice payments in:

- **Accounts Payable (AP)**
- **Accounts Receivable (AR)**

The app uses Python's built-in `tkinter` UI toolkit, so no third-party dependencies are required.

## Features

- Separate AP and AR mock entry tabs.
- Capture vendor/customer, amount, payment method, and mock status.
- Live totals for:
  - AP Paid (processed only)
  - AR Received (processed only)
- Central transaction log with timestamped entries.

## Run

```bash
python3 app.py
```
