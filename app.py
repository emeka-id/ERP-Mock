import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LedgerEntry:
    side: str
    account: str
    amount: float
    method: str
    status: str
    timestamp: str


class InvoiceMockApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ERP Invoice Payment Mock")
        self.root.geometry("860x560")

        self.entries: list[LedgerEntry] = []
        self.ap_total = tk.DoubleVar(value=0.0)
        self.ar_total = tk.DoubleVar(value=0.0)

        self._build_ui()

    def _build_ui(self) -> None:
        header = ttk.Label(
            self.root,
            text="Invoice Payment Mock Console",
            font=("Segoe UI", 16, "bold"),
        )
        header.pack(pady=(12, 4))

        sub = ttk.Label(
            self.root,
            text="Simulate invoice payments for Accounts Payable and Accounts Receivable",
        )
        sub.pack(pady=(0, 10))

        summary = ttk.Frame(self.root, padding=10)
        summary.pack(fill="x")
        ttk.Label(summary, text="AP Paid:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(summary, textvariable=self.ap_total).grid(row=0, column=1, sticky="w", padx=(8, 20))
        ttk.Label(summary, text="AR Received:", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w")
        ttk.Label(summary, textvariable=self.ar_total).grid(row=0, column=3, sticky="w", padx=(8, 20))

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="x", padx=10, pady=8)

        self.ap_frame = ttk.Frame(notebook, padding=12)
        self.ar_frame = ttk.Frame(notebook, padding=12)

        notebook.add(self.ap_frame, text="Accounts Payable")
        notebook.add(self.ar_frame, text="Accounts Receivable")

        self._build_form(self.ap_frame, side="AP")
        self._build_form(self.ar_frame, side="AR")

        log_frame = ttk.LabelFrame(self.root, text="Transaction Log", padding=8)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        columns = ("time", "side", "account", "amount", "method", "status")
        self.log = ttk.Treeview(log_frame, columns=columns, show="headings", height=11)
        headings = {
            "time": "Timestamp",
            "side": "Type",
            "account": "Vendor/Customer",
            "amount": "Amount",
            "method": "Method",
            "status": "Status",
        }
        for col in columns:
            self.log.heading(col, text=headings[col])
            self.log.column(col, width=130 if col != "account" else 190, anchor="center")

        self.log.pack(fill="both", expand=True)

    def _build_form(self, frame: ttk.Frame, side: str) -> None:
        entity_label = "Vendor" if side == "AP" else "Customer"
        status_options = ["Pending", "Processed", "Failed"]
        method_options = ["Bank Transfer", "Card", "Check", "Cash"]

        ttk.Label(frame, text=f"{entity_label} Name").grid(row=0, column=0, sticky="w", pady=6)
        name_entry = ttk.Entry(frame, width=32)
        name_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(frame, text="Invoice Amount").grid(row=1, column=0, sticky="w", pady=6)
        amount_entry = ttk.Entry(frame, width=18)
        amount_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(frame, text="Payment Method").grid(row=2, column=0, sticky="w", pady=6)
        method_box = ttk.Combobox(frame, values=method_options, state="readonly", width=18)
        method_box.set(method_options[0])
        method_box.grid(row=2, column=1, sticky="w")

        ttk.Label(frame, text="Mock Status").grid(row=3, column=0, sticky="w", pady=6)
        status_box = ttk.Combobox(frame, values=status_options, state="readonly", width=18)
        status_box.set(status_options[1])
        status_box.grid(row=3, column=1, sticky="w")

        action = ttk.Button(
            frame,
            text="Record Mock Payment",
            command=lambda: self.record_entry(
                side=side,
                account=name_entry.get(),
                amount_raw=amount_entry.get(),
                method=method_box.get(),
                status=status_box.get(),
                amount_widget=amount_entry,
            ),
        )
        action.grid(row=4, column=0, columnspan=2, pady=(10, 4), sticky="w")

    def record_entry(
        self,
        side: str,
        account: str,
        amount_raw: str,
        method: str,
        status: str,
        amount_widget: ttk.Entry,
    ) -> None:
        account = account.strip()
        if not account:
            messagebox.showerror("Missing field", "Please provide a vendor/customer name.")
            return

        try:
            amount = float(amount_raw)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid amount", "Invoice amount must be a number greater than 0.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = LedgerEntry(side=side, account=account, amount=amount, method=method, status=status, timestamp=now)
        self.entries.append(entry)

        self.log.insert(
            "",
            tk.END,
            values=(entry.timestamp, entry.side, entry.account, f"${entry.amount:,.2f}", entry.method, entry.status),
        )

        if status == "Processed":
            if side == "AP":
                self.ap_total.set(round(self.ap_total.get() + amount, 2))
            else:
                self.ar_total.set(round(self.ar_total.get() + amount, 2))

        amount_widget.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceMockApp(root)
    root.mainloop()
