$ErrorActionPreference = "Stop"

Write-Host "[1/4] Creating build virtual environment..."
python -m venv .venv-build

Write-Host "[2/4] Installing build dependencies..."
.\.venv-build\Scripts\python.exe -m pip install --upgrade pip
.\.venv-build\Scripts\python.exe -m pip install -r requirements-build.txt

Write-Host "[3/4] Building standalone .exe with PyInstaller..."
.\.venv-build\Scripts\pyinstaller.exe --noconfirm --clean --windowed --onefile --name ERPInvoiceMock app.py

Write-Host "[4/4] Build complete. Output: dist\ERPInvoiceMock.exe"
