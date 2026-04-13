# PeopleSoft AR/AP Module Mock (Desktop)

This desktop app simulates core **PeopleSoft FSCM Accounts Receivable and Accounts Payable** flows for demos and training.

## Included module simulations

### AR WorkCenter
- AR Item Entry (BU, customer, entry type, due days, amount)
- AR Payment Worksheet (post/pending/error payment outcomes)
- AR open-item list and real-time status transitions (`OPEN`, `PARTIALLY_PAID`, `CLOSED`)

### AP WorkCenter
- AP Voucher Entry (BU, vendor, origin, due days, amount)
- AP Payment Manager (post/pending/error payment outcomes)
- AP voucher list and real-time status transitions (`OPEN`, `PARTIALLY_PAID`, `CLOSED`)

### Control & Posting
- AR aging snapshot simulation
- AP pay cycle simulation
- AR/AP reconciliation snapshot with process monitor log

## Quick start

```bash
python3 app.py
```

## Build Windows `.exe`

```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows_exe.ps1
```

Output:
- `dist\ERPInvoiceMock.exe`

## Optional installer (`.exe` setup wizard)
1. Build `dist\ERPInvoiceMock.exe` first.
2. Open `installer.iss` in Inno Setup.
3. Click **Build**.

Output:
- `dist\ERPInvoiceMockInstaller.exe`
