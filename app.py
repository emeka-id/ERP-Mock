import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ARInvoice:
    business_unit: str
    customer: str
    invoice_id: str
    invoice_date: str
    due_date: str
    amount: float
    balance: float
    status: str


@dataclass
class APVoucher:
    business_unit: str
    vendor: str
    voucher_id: str
    invoice_date: str
    due_date: str
    amount: float
    balance: float
    status: str


class PeopleSoftARAPMockApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PeopleSoft FSCM AR/AP Mock Console")
        self.root.geometry("1200x760")

        self.business_units = ["US001", "US002", "CAN01"]
        self.ar_invoices: list[ARInvoice] = []
        self.ap_vouchers: list[APVoucher] = []
        self.activity_log: list[str] = []

        self.ar_open_total = tk.DoubleVar(value=0.0)
        self.ar_collected_total = tk.DoubleVar(value=0.0)
        self.ap_open_total = tk.DoubleVar(value=0.0)
        self.ap_paid_total = tk.DoubleVar(value=0.0)

        self._build_ui()

    def _build_ui(self) -> None:
        title = ttk.Label(
            self.root,
            text="PeopleSoft Accounts Receivable / Accounts Payable Mock",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(pady=(10, 4))

        subtitle = ttk.Label(
            self.root,
            text="Mock AR items, AP vouchers, payments, and posting outcomes by Business Unit",
        )
        subtitle.pack(pady=(0, 8))

        self._build_kpi_bar()

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=8)

        self.ar_tab = ttk.Frame(notebook, padding=10)
        self.ap_tab = ttk.Frame(notebook, padding=10)
        self.log_tab = ttk.Frame(notebook, padding=10)

        notebook.add(self.ar_tab, text="AR WorkCenter")
        notebook.add(self.ap_tab, text="AP WorkCenter")
        notebook.add(self.log_tab, text="Activity Log")

        self._build_ar_tab()
        self._build_ap_tab()
        self._build_log_tab()

    def _build_kpi_bar(self) -> None:
        kpi_frame = ttk.Frame(self.root, padding=10)
        kpi_frame.pack(fill="x")

        cards = [
            ("AR Open Items", self.ar_open_total),
            ("AR Collected", self.ar_collected_total),
            ("AP Open Vouchers", self.ap_open_total),
            ("AP Paid", self.ap_paid_total),
        ]

        for idx, (label, var) in enumerate(cards):
            card = ttk.LabelFrame(kpi_frame, text=label, padding=(12, 8))
            card.grid(row=0, column=idx, padx=6, sticky="ew")
            ttk.Label(card, textvariable=var, font=("Segoe UI", 12, "bold")).pack()
            kpi_frame.grid_columnconfigure(idx, weight=1)

    def _build_ar_tab(self) -> None:
        left = ttk.LabelFrame(self.ar_tab, text="Create AR Item", padding=10)
        left.pack(side="left", fill="y", padx=(0, 8))

        ttk.Label(left, text="Business Unit").grid(row=0, column=0, sticky="w", pady=4)
        self.ar_bu = ttk.Combobox(left, values=self.business_units, state="readonly", width=16)
        self.ar_bu.set(self.business_units[0])
        self.ar_bu.grid(row=0, column=1, sticky="w")

        ttk.Label(left, text="Customer").grid(row=1, column=0, sticky="w", pady=4)
        self.ar_customer = ttk.Entry(left, width=24)
        self.ar_customer.grid(row=1, column=1, sticky="w")

        ttk.Label(left, text="Invoice Amount").grid(row=2, column=0, sticky="w", pady=4)
        self.ar_amount = ttk.Entry(left, width=18)
        self.ar_amount.grid(row=2, column=1, sticky="w")

        ttk.Label(left, text="Due (days)").grid(row=3, column=0, sticky="w", pady=4)
        self.ar_due_days = ttk.Entry(left, width=18)
        self.ar_due_days.insert(0, "30")
        self.ar_due_days.grid(row=3, column=1, sticky="w")

        ttk.Button(left, text="Create AR Item", command=self.create_ar_invoice).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(10, 4)
        )

        payment_box = ttk.LabelFrame(left, text="Apply AR Payment", padding=8)
        payment_box.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        ttk.Label(payment_box, text="Invoice").grid(row=0, column=0, sticky="w", pady=4)
        self.ar_payment_invoice = ttk.Combobox(payment_box, values=[], state="readonly", width=24)
        self.ar_payment_invoice.grid(row=0, column=1, sticky="w")

        ttk.Label(payment_box, text="Amount").grid(row=1, column=0, sticky="w", pady=4)
        self.ar_payment_amount = ttk.Entry(payment_box, width=18)
        self.ar_payment_amount.grid(row=1, column=1, sticky="w")

        ttk.Label(payment_box, text="Method").grid(row=2, column=0, sticky="w", pady=4)
        self.ar_method = ttk.Combobox(payment_box, values=["Wire", "ACH", "Check", "Card"], state="readonly", width=16)
        self.ar_method.set("ACH")
        self.ar_method.grid(row=2, column=1, sticky="w")

        ttk.Label(payment_box, text="Posting").grid(row=3, column=0, sticky="w", pady=4)
        self.ar_posting = ttk.Combobox(payment_box, values=["Post", "Pending", "Error"], state="readonly", width=16)
        self.ar_posting.set("Post")
        self.ar_posting.grid(row=3, column=1, sticky="w")

        ttk.Button(payment_box, text="Apply Payment", command=self.apply_ar_payment).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )

        right = ttk.LabelFrame(self.ar_tab, text="AR Item List", padding=8)
        right.pack(side="left", fill="both", expand=True)

        self.ar_tree = ttk.Treeview(
            right,
            columns=("bu", "invoice", "customer", "invoice_date", "due_date", "amount", "balance", "status"),
            show="headings",
            height=21,
        )
        for col, text, width in [
            ("bu", "BU", 80),
            ("invoice", "Invoice", 110),
            ("customer", "Customer", 140),
            ("invoice_date", "Inv Date", 100),
            ("due_date", "Due Date", 100),
            ("amount", "Amount", 95),
            ("balance", "Balance", 95),
            ("status", "Status", 120),
        ]:
            self.ar_tree.heading(col, text=text)
            self.ar_tree.column(col, width=width, anchor="center")

        self.ar_tree.pack(fill="both", expand=True)

    def _build_ap_tab(self) -> None:
        left = ttk.LabelFrame(self.ap_tab, text="Create AP Voucher", padding=10)
        left.pack(side="left", fill="y", padx=(0, 8))

        ttk.Label(left, text="Business Unit").grid(row=0, column=0, sticky="w", pady=4)
        self.ap_bu = ttk.Combobox(left, values=self.business_units, state="readonly", width=16)
        self.ap_bu.set(self.business_units[0])
        self.ap_bu.grid(row=0, column=1, sticky="w")

        ttk.Label(left, text="Vendor").grid(row=1, column=0, sticky="w", pady=4)
        self.ap_vendor = ttk.Entry(left, width=24)
        self.ap_vendor.grid(row=1, column=1, sticky="w")

        ttk.Label(left, text="Voucher Amount").grid(row=2, column=0, sticky="w", pady=4)
        self.ap_amount = ttk.Entry(left, width=18)
        self.ap_amount.grid(row=2, column=1, sticky="w")

        ttk.Label(left, text="Due (days)").grid(row=3, column=0, sticky="w", pady=4)
        self.ap_due_days = ttk.Entry(left, width=18)
        self.ap_due_days.insert(0, "30")
        self.ap_due_days.grid(row=3, column=1, sticky="w")

        ttk.Button(left, text="Create Voucher", command=self.create_ap_voucher).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(10, 4)
        )

        payment_box = ttk.LabelFrame(left, text="Apply AP Payment", padding=8)
        payment_box.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        ttk.Label(payment_box, text="Voucher").grid(row=0, column=0, sticky="w", pady=4)
        self.ap_payment_voucher = ttk.Combobox(payment_box, values=[], state="readonly", width=24)
        self.ap_payment_voucher.grid(row=0, column=1, sticky="w")

        ttk.Label(payment_box, text="Amount").grid(row=1, column=0, sticky="w", pady=4)
        self.ap_payment_amount = ttk.Entry(payment_box, width=18)
        self.ap_payment_amount.grid(row=1, column=1, sticky="w")

        ttk.Label(payment_box, text="Method").grid(row=2, column=0, sticky="w", pady=4)
        self.ap_method = ttk.Combobox(payment_box, values=["ACH", "Wire", "Check", "Card"], state="readonly", width=16)
        self.ap_method.set("ACH")
        self.ap_method.grid(row=2, column=1, sticky="w")

        ttk.Label(payment_box, text="Posting").grid(row=3, column=0, sticky="w", pady=4)
        self.ap_posting = ttk.Combobox(payment_box, values=["Post", "Pending", "Error"], state="readonly", width=16)
        self.ap_posting.set("Post")
        self.ap_posting.grid(row=3, column=1, sticky="w")

        ttk.Button(payment_box, text="Apply Payment", command=self.apply_ap_payment).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )

        right = ttk.LabelFrame(self.ap_tab, text="AP Voucher List", padding=8)
        right.pack(side="left", fill="both", expand=True)

        self.ap_tree = ttk.Treeview(
            right,
            columns=("bu", "voucher", "vendor", "invoice_date", "due_date", "amount", "balance", "status"),
            show="headings",
            height=21,
        )
        for col, text, width in [
            ("bu", "BU", 80),
            ("voucher", "Voucher", 110),
            ("vendor", "Vendor", 140),
            ("invoice_date", "Inv Date", 100),
            ("due_date", "Due Date", 100),
            ("amount", "Amount", 95),
            ("balance", "Balance", 95),
            ("status", "Status", 120),
        ]:
            self.ap_tree.heading(col, text=text)
            self.ap_tree.column(col, width=width, anchor="center")

        self.ap_tree.pack(fill="both", expand=True)

    def _build_log_tab(self) -> None:
        ttk.Label(self.log_tab, text="Posting and activity messages", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.log_widget = tk.Text(self.log_tab, height=30)
        self.log_widget.pack(fill="both", expand=True, pady=(8, 0))
        self.log_widget.configure(state="disabled")

    def create_ar_invoice(self) -> None:
        customer = self.ar_customer.get().strip()
        if not customer:
            messagebox.showerror("Missing data", "Customer is required.")
            return

        amount = self._parse_positive_amount(self.ar_amount.get(), "Invoice amount")
        if amount is None:
            return

        due_days = self._parse_positive_int(self.ar_due_days.get(), "Due days")
        if due_days is None:
            return

        today = datetime.now().date()
        due = today + timedelta(days=due_days)
        invoice_id = f"AR{len(self.ar_invoices) + 1001}"

        inv = ARInvoice(
            business_unit=self.ar_bu.get(),
            customer=customer,
            invoice_id=invoice_id,
            invoice_date=today.isoformat(),
            due_date=due.isoformat(),
            amount=amount,
            balance=amount,
            status="Open",
        )
        self.ar_invoices.append(inv)
        self._append_log(f"AR Item Created: {inv.business_unit}/{inv.invoice_id} {inv.customer} ${inv.amount:,.2f}")
        self._refresh_ar_view()
        self.ar_customer.delete(0, tk.END)
        self.ar_amount.delete(0, tk.END)

    def create_ap_voucher(self) -> None:
        vendor = self.ap_vendor.get().strip()
        if not vendor:
            messagebox.showerror("Missing data", "Vendor is required.")
            return

        amount = self._parse_positive_amount(self.ap_amount.get(), "Voucher amount")
        if amount is None:
            return

        due_days = self._parse_positive_int(self.ap_due_days.get(), "Due days")
        if due_days is None:
            return

        today = datetime.now().date()
        due = today + timedelta(days=due_days)
        voucher_id = f"AP{len(self.ap_vouchers) + 2001}"

        voucher = APVoucher(
            business_unit=self.ap_bu.get(),
            vendor=vendor,
            voucher_id=voucher_id,
            invoice_date=today.isoformat(),
            due_date=due.isoformat(),
            amount=amount,
            balance=amount,
            status="Open",
        )
        self.ap_vouchers.append(voucher)
        self._append_log(f"AP Voucher Created: {voucher.business_unit}/{voucher.voucher_id} {voucher.vendor} ${voucher.amount:,.2f}")
        self._refresh_ap_view()
        self.ap_vendor.delete(0, tk.END)
        self.ap_amount.delete(0, tk.END)

    def apply_ar_payment(self) -> None:
        selected = self.ar_payment_invoice.get().strip()
        if not selected:
            messagebox.showerror("Missing data", "Select an AR invoice first.")
            return

        amount = self._parse_positive_amount(self.ar_payment_amount.get(), "Payment amount")
        if amount is None:
            return

        posting = self.ar_posting.get()
        method = self.ar_method.get()

        invoice_id = selected.split(" | ")[0]
        invoice = next((i for i in self.ar_invoices if i.invoice_id == invoice_id), None)
        if not invoice:
            messagebox.showerror("Not found", "Selected AR invoice could not be found.")
            return

        if amount > invoice.balance:
            messagebox.showerror("Invalid amount", "Payment cannot exceed open balance.")
            return

        if posting == "Post":
            invoice.balance = round(invoice.balance - amount, 2)
            self.ar_collected_total.set(round(self.ar_collected_total.get() + amount, 2))
            invoice.status = "Closed" if invoice.balance == 0 else "Partially Paid"
            self._append_log(
                f"AR Payment Posted: {invoice.invoice_id} ${amount:,.2f} via {method}. Balance ${invoice.balance:,.2f}"
            )
        elif posting == "Pending":
            self._append_log(f"AR Payment Pending: {invoice.invoice_id} ${amount:,.2f} via {method}")
        else:
            self._append_log(f"AR Payment Error: {invoice.invoice_id} ${amount:,.2f} via {method}")

        self.ar_payment_amount.delete(0, tk.END)
        self._refresh_ar_view()

    def apply_ap_payment(self) -> None:
        selected = self.ap_payment_voucher.get().strip()
        if not selected:
            messagebox.showerror("Missing data", "Select an AP voucher first.")
            return

        amount = self._parse_positive_amount(self.ap_payment_amount.get(), "Payment amount")
        if amount is None:
            return

        posting = self.ap_posting.get()
        method = self.ap_method.get()

        voucher_id = selected.split(" | ")[0]
        voucher = next((v for v in self.ap_vouchers if v.voucher_id == voucher_id), None)
        if not voucher:
            messagebox.showerror("Not found", "Selected AP voucher could not be found.")
            return

        if amount > voucher.balance:
            messagebox.showerror("Invalid amount", "Payment cannot exceed open balance.")
            return

        if posting == "Post":
            voucher.balance = round(voucher.balance - amount, 2)
            self.ap_paid_total.set(round(self.ap_paid_total.get() + amount, 2))
            voucher.status = "Closed" if voucher.balance == 0 else "Partially Paid"
            self._append_log(
                f"AP Payment Posted: {voucher.voucher_id} ${amount:,.2f} via {method}. Balance ${voucher.balance:,.2f}"
            )
        elif posting == "Pending":
            self._append_log(f"AP Payment Pending: {voucher.voucher_id} ${amount:,.2f} via {method}")
        else:
            self._append_log(f"AP Payment Error: {voucher.voucher_id} ${amount:,.2f} via {method}")

        self.ap_payment_amount.delete(0, tk.END)
        self._refresh_ap_view()

    def _refresh_ar_view(self) -> None:
        self.ar_tree.delete(*self.ar_tree.get_children())
        for inv in self.ar_invoices:
            self.ar_tree.insert(
                "",
                tk.END,
                values=(
                    inv.business_unit,
                    inv.invoice_id,
                    inv.customer,
                    inv.invoice_date,
                    inv.due_date,
                    f"${inv.amount:,.2f}",
                    f"${inv.balance:,.2f}",
                    inv.status,
                ),
            )

        open_total = sum(i.balance for i in self.ar_invoices)
        self.ar_open_total.set(round(open_total, 2))

        open_options = [f"{i.invoice_id} | {i.customer} | ${i.balance:,.2f}" for i in self.ar_invoices if i.balance > 0]
        self.ar_payment_invoice["values"] = open_options
        if open_options:
            self.ar_payment_invoice.set(open_options[0])
        else:
            self.ar_payment_invoice.set("")

    def _refresh_ap_view(self) -> None:
        self.ap_tree.delete(*self.ap_tree.get_children())
        for voucher in self.ap_vouchers:
            self.ap_tree.insert(
                "",
                tk.END,
                values=(
                    voucher.business_unit,
                    voucher.voucher_id,
                    voucher.vendor,
                    voucher.invoice_date,
                    voucher.due_date,
                    f"${voucher.amount:,.2f}",
                    f"${voucher.balance:,.2f}",
                    voucher.status,
                ),
            )

        open_total = sum(v.balance for v in self.ap_vouchers)
        self.ap_open_total.set(round(open_total, 2))

        open_options = [f"{v.voucher_id} | {v.vendor} | ${v.balance:,.2f}" for v in self.ap_vouchers if v.balance > 0]
        self.ap_payment_voucher["values"] = open_options
        if open_options:
            self.ap_payment_voucher.set(open_options[0])
        else:
            self.ap_payment_voucher.set("")

    def _append_log(self, message: str) -> None:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{stamp}] {message}"
        self.activity_log.append(entry)

        self.log_widget.configure(state="normal")
        self.log_widget.insert(tk.END, entry + "\n")
        self.log_widget.see(tk.END)
        self.log_widget.configure(state="disabled")

    @staticmethod
    def _parse_positive_amount(raw: str, label: str) -> float | None:
        try:
            value = float(raw)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            messagebox.showerror("Invalid amount", f"{label} must be a number greater than 0.")
            return None

    @staticmethod
    def _parse_positive_int(raw: str, label: str) -> int | None:
        try:
            value = int(raw)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            messagebox.showerror("Invalid value", f"{label} must be a whole number greater than 0.")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = PeopleSoftARAPMockApp(root)
    root.mainloop()
