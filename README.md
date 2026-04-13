# ERP Invoice Payment Mock Desktop App

A simple desktop app for mocking invoice payments for:

- **Accounts Payable (AP)**
- **Accounts Receivable (AR)**

The app uses Python's built-in `tkinter` UI toolkit.

## Features

- Separate AP and AR tabs.
- Capture vendor/customer, invoice amount, payment method, and status.
- Live totals for processed AP and AR entries.
- Central timestamped transaction log.

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

If you want an installable setup executable:

1. Install **Inno Setup** on Windows.
2. Build the app first so `dist\ERPInvoiceMock.exe` exists.
3. Open `installer.iss` in Inno Setup and click **Build**.

Output:

- `dist\ERPInvoiceMockInstaller.exe`
