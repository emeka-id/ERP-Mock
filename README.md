# PeopleSoft AR/AP Mock Desktop App

A desktop app that mocks core **PeopleSoft FSCM** workflows for:

- **Accounts Receivable (AR)**
- **Accounts Payable (AP)**

It is designed for demos, training, and non-production process walkthroughs.

## What is mocked

### AR WorkCenter

- Create AR items by business unit with customer, amount, and due date offset.
- Apply incoming payments with posting outcomes (`Post`, `Pending`, `Error`).
- Track open balance and status (`Open`, `Partially Paid`, `Closed`).

### AP WorkCenter

- Create AP vouchers by business unit with vendor, amount, and due date offset.
- Apply outgoing payments with posting outcomes (`Post`, `Pending`, `Error`).
- Track open balance and status (`Open`, `Partially Paid`, `Closed`).

### Operational dashboards

- KPI cards for AR open/collected and AP open/paid.
- Timestamped activity log that simulates posting messages.

## Run from source

```bash
python3 app.py
```

## Build a Windows `.exe`

### Option A: one-command PowerShell build (recommended)

On a Windows machine with Python installed:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows_exe.ps1
```

Output:

- `dist\ERPInvoiceMock.exe`

### Option B: manual build with PyInstaller

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-build.txt
pyinstaller --noconfirm --clean --windowed --onefile --name ERPInvoiceMock app.py
```

Output:

- `dist\ERPInvoiceMock.exe`

## Create an installer (`.exe` setup wizard)

1. Install **Inno Setup** on Windows.
2. Build the app first so `dist\ERPInvoiceMock.exe` exists.
3. Open `installer.iss` in Inno Setup and click **Build**.

Output:

- `dist\ERPInvoiceMockInstaller.exe`
