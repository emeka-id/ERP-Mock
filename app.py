import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from datetime import date, datetime, timedelta


@dataclass
class ARItem:
    bu: str
    item_id: str
    customer_id: str
    customer_name: str
    accounting_date: date
    due_date: date
    gross_amount: float
    open_amount: float
    entry_type: str
    status: str


@dataclass
class APVoucher:
    bu: str
    voucher_id: str
    vendor_id: str
    vendor_name: str
    invoice_date: date
    due_date: date
    gross_amount: float
    open_amount: float
    origin: str
    status: str


class PeopleSoftMockApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PeopleSoft FSCM AR/AP Module Mock")
        self.root.geometry("1280x780")

        self.business_units = ["US001", "US002", "CAN01"]
        self.ar_items: list[ARItem] = []
        self.ap_vouchers: list[APVoucher] = []

        self.ar_open = tk.DoubleVar(value=0.0)
        self.ar_collected = tk.DoubleVar(value=0.0)
        self.ap_open = tk.DoubleVar(value=0.0)
        self.ap_paid = tk.DoubleVar(value=0.0)

        self._build_layout()
        self._seed_demo_data()

    def _build_layout(self) -> None:
        ttk.Label(
            self.root,
            text="PeopleSoft Accounts Receivable / Accounts Payable Mock",
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(10, 4))

        ttk.Label(
            self.root,
            text="Simulate AR item entry, AP voucher entry, payment posting, and reconciliation",
        ).pack(pady=(0, 8))

        kpi = ttk.Frame(self.root, padding=8)
        kpi.pack(fill="x")

        self._kpi_card(kpi, 0, "AR Open", self.ar_open)
        self._kpi_card(kpi, 1, "AR Collected", self.ar_collected)
        self._kpi_card(kpi, 2, "AP Open", self.ap_open)
        self._kpi_card(kpi, 3, "AP Paid", self.ap_paid)

        tabs = ttk.Notebook(self.root)
        tabs.pack(fill="both", expand=True, padx=10, pady=8)

        self.ar_tab = ttk.Frame(tabs, padding=10)
        self.ap_tab = ttk.Frame(tabs, padding=10)
        self.control_tab = ttk.Frame(tabs, padding=10)

        tabs.add(self.ar_tab, text="AR WorkCenter")
        tabs.add(self.ap_tab, text="AP WorkCenter")
        tabs.add(self.control_tab, text="Control & Posting")

        self._build_ar_tab()
        self._build_ap_tab()
        self._build_control_tab()

    @staticmethod
    def _kpi_card(parent: ttk.Frame, column: int, title: str, var: tk.DoubleVar) -> None:
        card = ttk.LabelFrame(parent, text=title, padding=8)
        card.grid(row=0, column=column, padx=5, sticky="ew")
        ttk.Label(card, textvariable=var, font=("Segoe UI", 12, "bold")).pack()
        parent.grid_columnconfigure(column, weight=1)

    def _build_ar_tab(self) -> None:
        form = ttk.LabelFrame(self.ar_tab, text="AR Item Entry", padding=10)
        form.pack(side="left", fill="y", padx=(0, 8))

        self.ar_bu = self._combo(form, "Business Unit", self.business_units, 0)
        self.ar_customer_id = self._entry(form, "Customer ID", 1)
        self.ar_customer_name = self._entry(form, "Customer Name", 2)
        self.ar_amount = self._entry(form, "Item Amount", 3)
        self.ar_due_days = self._entry(form, "Due Days", 4, default="30")
        self.ar_entry_type = self._combo(form, "Entry Type", ["INVOICE", "DEBIT_MEMO", "CREDIT_MEMO"], 5)

        ttk.Button(form, text="Create AR Item", command=self.create_ar_item).grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 3))

        pay = ttk.LabelFrame(form, text="AR Payment Worksheet", padding=8)
        pay.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.ar_payment_item = self._combo(pay, "Open Item", [], 0, width=28)
        self.ar_payment_amount = self._entry(pay, "Payment Amount", 1)
        self.ar_payment_method = self._combo(pay, "Method", ["ACH", "WIRE", "CHECK", "CARD"], 2)
        self.ar_post_action = self._combo(pay, "Post Action", ["POST", "PENDING", "ERROR"], 3)
        ttk.Button(pay, text="Post AR Payment", command=self.apply_ar_payment).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))

        list_box = ttk.LabelFrame(self.ar_tab, text="AR Open Item List", padding=8)
        list_box.pack(side="left", fill="both", expand=True)
        self.ar_tree = ttk.Treeview(
            list_box,
            columns=("bu", "item", "cust", "name", "acct", "due", "gross", "open", "entry", "status"),
            show="headings",
            height=24,
        )
        for col, txt, w in [
            ("bu", "BU", 70),
            ("item", "Item ID", 90),
            ("cust", "Cust ID", 90),
            ("name", "Customer", 130),
            ("acct", "Acct Date", 95),
            ("due", "Due Date", 95),
            ("gross", "Gross", 90),
            ("open", "Open", 90),
            ("entry", "Entry Type", 110),
            ("status", "Status", 110),
        ]:
            self.ar_tree.heading(col, text=txt)
            self.ar_tree.column(col, width=w, anchor="center")
        self.ar_tree.pack(fill="both", expand=True)

    def _build_ap_tab(self) -> None:
        form = ttk.LabelFrame(self.ap_tab, text="AP Voucher Entry", padding=10)
        form.pack(side="left", fill="y", padx=(0, 8))

        self.ap_bu = self._combo(form, "Business Unit", self.business_units, 0)
        self.ap_vendor_id = self._entry(form, "Vendor ID", 1)
        self.ap_vendor_name = self._entry(form, "Vendor Name", 2)
        self.ap_amount = self._entry(form, "Voucher Amount", 3)
        self.ap_due_days = self._entry(form, "Due Days", 4, default="30")
        self.ap_origin = self._combo(form, "Voucher Origin", ["ONLINE", "BATCH", "INTERUNIT"], 5)

        ttk.Button(form, text="Create Voucher", command=self.create_ap_voucher).grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 3))

        pay = ttk.LabelFrame(form, text="AP Payment Manager", padding=8)
        pay.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.ap_payment_voucher = self._combo(pay, "Open Voucher", [], 0, width=28)
        self.ap_payment_amount = self._entry(pay, "Payment Amount", 1)
        self.ap_payment_method = self._combo(pay, "Method", ["ACH", "WIRE", "CHECK", "CARD"], 2)
        self.ap_post_action = self._combo(pay, "Post Action", ["POST", "PENDING", "ERROR"], 3)
        ttk.Button(pay, text="Post AP Payment", command=self.apply_ap_payment).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))

        list_box = ttk.LabelFrame(self.ap_tab, text="AP Voucher List", padding=8)
        list_box.pack(side="left", fill="both", expand=True)
        self.ap_tree = ttk.Treeview(
            list_box,
            columns=("bu", "voucher", "vendor", "name", "inv", "due", "gross", "open", "origin", "status"),
            show="headings",
            height=24,
        )
        for col, txt, w in [
            ("bu", "BU", 70),
            ("voucher", "Voucher", 95),
            ("vendor", "Vendor ID", 90),
            ("name", "Vendor", 130),
            ("inv", "Inv Date", 95),
            ("due", "Due Date", 95),
            ("gross", "Gross", 90),
            ("open", "Open", 90),
            ("origin", "Origin", 100),
            ("status", "Status", 110),
        ]:
            self.ap_tree.heading(col, text=txt)
            self.ap_tree.column(col, width=w, anchor="center")
        self.ap_tree.pack(fill="both", expand=True)

    def _build_control_tab(self) -> None:
        left = ttk.LabelFrame(self.control_tab, text="Posting Actions", padding=10)
        left.pack(side="left", fill="y", padx=(0, 8))

        ttk.Button(left, text="Run AR Aging Snapshot", command=self.run_ar_aging).pack(fill="x", pady=3)
        ttk.Button(left, text="Run AP Pay Cycle Mock", command=self.run_ap_pay_cycle).pack(fill="x", pady=3)
        ttk.Button(left, text="Reconcile AR/AP Totals", command=self.run_reconciliation).pack(fill="x", pady=3)

        right = ttk.LabelFrame(self.control_tab, text="Process Monitor", padding=8)
        right.pack(side="left", fill="both", expand=True)
        self.monitor = tk.Text(right, height=35)
        self.monitor.pack(fill="both", expand=True)
        self.monitor.configure(state="disabled")

    @staticmethod
    def _entry(parent: ttk.Widget, label: str, row: int, default: str = "") -> ttk.Entry:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        e = ttk.Entry(parent, width=24)
        if default:
            e.insert(0, default)
        e.grid(row=row, column=1, sticky="w")
        return e

    @staticmethod
    def _combo(parent: ttk.Widget, label: str, values: list[str], row: int, width: int = 20) -> ttk.Combobox:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        c = ttk.Combobox(parent, values=values, state="readonly", width=width)
        if values:
            c.set(values[0])
        c.grid(row=row, column=1, sticky="w")
        return c

    def _seed_demo_data(self) -> None:
        self.ar_items.append(
            ARItem("US001", "AR1001", "CUST100", "Acme Retail", date.today(), date.today() + timedelta(days=15), 1200.0, 1200.0, "INVOICE", "OPEN")
        )
        self.ap_vouchers.append(
            APVoucher("US001", "AP2001", "VEND300", "Delta Supplies", date.today(), date.today() + timedelta(days=20), 840.0, 840.0, "ONLINE", "OPEN")
        )
        self._refresh_views()
        self._log("Seeded demo AR/AP transactions")

    def create_ar_item(self) -> None:
        amount = self._amount(self.ar_amount.get(), "Item Amount")
        due_days = self._positive_int(self.ar_due_days.get(), "Due Days")
        if amount is None or due_days is None:
            return

        cust_id = self.ar_customer_id.get().strip()
        cust_name = self.ar_customer_name.get().strip()
        if not cust_id or not cust_name:
            messagebox.showerror("Missing data", "Customer ID and Customer Name are required.")
            return

        item_id = f"AR{1000 + len(self.ar_items) + 1}"
        rec = ARItem(
            bu=self.ar_bu.get(),
            item_id=item_id,
            customer_id=cust_id,
            customer_name=cust_name,
            accounting_date=date.today(),
            due_date=date.today() + timedelta(days=due_days),
            gross_amount=amount,
            open_amount=amount,
            entry_type=self.ar_entry_type.get(),
            status="OPEN",
        )
        self.ar_items.append(rec)
        self._refresh_views()
        self._log(f"AR Item created: {rec.bu}/{rec.item_id} for {rec.customer_name} (${amount:,.2f})")

    def create_ap_voucher(self) -> None:
        amount = self._amount(self.ap_amount.get(), "Voucher Amount")
        due_days = self._positive_int(self.ap_due_days.get(), "Due Days")
        if amount is None or due_days is None:
            return

        vendor_id = self.ap_vendor_id.get().strip()
        vendor_name = self.ap_vendor_name.get().strip()
        if not vendor_id or not vendor_name:
            messagebox.showerror("Missing data", "Vendor ID and Vendor Name are required.")
            return

        voucher_id = f"AP{2000 + len(self.ap_vouchers) + 1}"
        rec = APVoucher(
            bu=self.ap_bu.get(),
            voucher_id=voucher_id,
            vendor_id=vendor_id,
            vendor_name=vendor_name,
            invoice_date=date.today(),
            due_date=date.today() + timedelta(days=due_days),
            gross_amount=amount,
            open_amount=amount,
            origin=self.ap_origin.get(),
            status="OPEN",
        )
        self.ap_vouchers.append(rec)
        self._refresh_views()
        self._log(f"AP Voucher created: {rec.bu}/{rec.voucher_id} for {rec.vendor_name} (${amount:,.2f})")

    def apply_ar_payment(self) -> None:
        selected = self.ar_payment_item.get()
        amount = self._amount(self.ar_payment_amount.get(), "Payment Amount")
        if not selected or amount is None:
            messagebox.showerror("Missing data", "Select open AR item and enter payment amount.")
            return

        item_id = selected.split(" | ")[0]
        item = next((x for x in self.ar_items if x.item_id == item_id), None)
        if not item or amount > item.open_amount:
            messagebox.showerror("Invalid payment", "Payment is invalid for selected AR item.")
            return

        action = self.ar_post_action.get()
        method = self.ar_payment_method.get()
        if action == "POST":
            item.open_amount = round(item.open_amount - amount, 2)
            self.ar_collected.set(round(self.ar_collected.get() + amount, 2))
            item.status = "CLOSED" if item.open_amount == 0 else "PARTIALLY_PAID"
        self._refresh_views()
        self._log(f"AR payment {action}: {item.item_id} amount ${amount:,.2f} via {method}")

    def apply_ap_payment(self) -> None:
        selected = self.ap_payment_voucher.get()
        amount = self._amount(self.ap_payment_amount.get(), "Payment Amount")
        if not selected or amount is None:
            messagebox.showerror("Missing data", "Select open AP voucher and enter payment amount.")
            return

        voucher_id = selected.split(" | ")[0]
        voucher = next((x for x in self.ap_vouchers if x.voucher_id == voucher_id), None)
        if not voucher or amount > voucher.open_amount:
            messagebox.showerror("Invalid payment", "Payment is invalid for selected AP voucher.")
            return

        action = self.ap_post_action.get()
        method = self.ap_payment_method.get()
        if action == "POST":
            voucher.open_amount = round(voucher.open_amount - amount, 2)
            self.ap_paid.set(round(self.ap_paid.get() + amount, 2))
            voucher.status = "CLOSED" if voucher.open_amount == 0 else "PARTIALLY_PAID"
        self._refresh_views()
        self._log(f"AP payment {action}: {voucher.voucher_id} amount ${amount:,.2f} via {method}")

    def run_ar_aging(self) -> None:
        today = date.today()
        buckets = {"Current": 0.0, "1-30": 0.0, "31-60": 0.0, "60+": 0.0}
        for item in self.ar_items:
            if item.open_amount <= 0:
                continue
            days = (today - item.due_date).days
            if days <= 0:
                buckets["Current"] += item.open_amount
            elif days <= 30:
                buckets["1-30"] += item.open_amount
            elif days <= 60:
                buckets["31-60"] += item.open_amount
            else:
                buckets["60+"] += item.open_amount
        self._log("AR Aging Snapshot -> " + ", ".join(f"{k}: ${v:,.2f}" for k, v in buckets.items()))

    def run_ap_pay_cycle(self) -> None:
        open_count = len([v for v in self.ap_vouchers if v.open_amount > 0])
        self._log(f"AP Pay Cycle mock executed. Open vouchers considered: {open_count}")

    def run_reconciliation(self) -> None:
        net = round(self.ar_open.get() - self.ap_open.get(), 2)
        self._log(f"Reconciliation snapshot -> AR Open ${self.ar_open.get():,.2f}, AP Open ${self.ap_open.get():,.2f}, Net ${net:,.2f}")

    def _refresh_views(self) -> None:
        self.ar_tree.delete(*self.ar_tree.get_children())
        for r in self.ar_items:
            self.ar_tree.insert(
                "",
                tk.END,
                values=(r.bu, r.item_id, r.customer_id, r.customer_name, r.accounting_date.isoformat(), r.due_date.isoformat(),
                        f"${r.gross_amount:,.2f}", f"${r.open_amount:,.2f}", r.entry_type, r.status),
            )

        self.ap_tree.delete(*self.ap_tree.get_children())
        for r in self.ap_vouchers:
            self.ap_tree.insert(
                "",
                tk.END,
                values=(r.bu, r.voucher_id, r.vendor_id, r.vendor_name, r.invoice_date.isoformat(), r.due_date.isoformat(),
                        f"${r.gross_amount:,.2f}", f"${r.open_amount:,.2f}", r.origin, r.status),
            )

        self.ar_open.set(round(sum(x.open_amount for x in self.ar_items), 2))
        self.ap_open.set(round(sum(x.open_amount for x in self.ap_vouchers), 2))

        ar_opts = [f"{x.item_id} | {x.customer_name} | ${x.open_amount:,.2f}" for x in self.ar_items if x.open_amount > 0]
        self.ar_payment_item["values"] = ar_opts
        self.ar_payment_item.set(ar_opts[0] if ar_opts else "")

        ap_opts = [f"{x.voucher_id} | {x.vendor_name} | ${x.open_amount:,.2f}" for x in self.ap_vouchers if x.open_amount > 0]
        self.ap_payment_voucher["values"] = ap_opts
        self.ap_payment_voucher.set(ap_opts[0] if ap_opts else "")

    def _log(self, msg: str) -> None:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{stamp}] {msg}\n"
        self.monitor.configure(state="normal")
        self.monitor.insert(tk.END, line)
        self.monitor.see(tk.END)
        self.monitor.configure(state="disabled")

    @staticmethod
    def _amount(raw: str, label: str) -> float | None:
        try:
            value = float(raw)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            messagebox.showerror("Invalid amount", f"{label} must be > 0")
            return None

    @staticmethod
    def _positive_int(raw: str, label: str) -> int | None:
        try:
            value = int(raw)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            messagebox.showerror("Invalid value", f"{label} must be a positive integer")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = PeopleSoftMockApp(root)
    root.mainloop()
