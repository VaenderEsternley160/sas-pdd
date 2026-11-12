import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Aplikasi stok sederhana berbasis memori (data hilang saat aplikasi ditutup).
BG = "#eef9fb"
BLUE = "#4f98aa"
BLUE_DARK = "#286b7c"
TEAL = "#55aaa6"
TEAL_DARK = "#287f7b"
RED = "#a6382d"
WHITE = "#ffffff"
INK = "#18343b"


class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple In-Memory Stock Application")
        self.root.geometry("1180x680")
        self.root.minsize(1000, 620)
        self.root.configure(bg=BG)

        self.inbound = []
        self.outbound = []
        self.products = {
            "SKU-001": {"name": "Beras Premium", "category": "Sembako",
                        "unit": "Pcs", "stock": 30}
        }

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Stock.Treeview", background="#f7fcfd", foreground=INK,
            fieldbackground="#f7fcfd", rowheight=27, font=("Arial", 9)
        )
        self.style.configure(
            "Stock.Treeview.Heading", background="#315d68",
            foreground="white", font=("Arial", 9, "bold"), relief="flat"
        )
        self.style.map("Stock.Treeview.Heading",
                       background=[("active", "#315d68")])
        self.show_home()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def header(self, parent, title, subtitle=None):
        bar = tk.Frame(parent, bg=BLUE, height=58)
        bar.pack(fill="x", padx=12, pady=(10, 12))
        bar.pack_propagate(False)
        tk.Label(bar, text=title, bg=BLUE, fg="white",
                 font=("Arial", 18, "bold")).pack(expand=True)
        if subtitle:
            tk.Label(bar, text=subtitle, bg=BLUE, fg="#eaf7fa",
                     font=("Arial", 9)).pack()

    def make_button(self, parent, text, command, color=BLUE,
                    fg="white", width=None, height=2):
        b = tk.Button(parent, text=text, command=command, bg=color, fg=fg,
                      activebackground=color, activeforeground=fg,
                      relief="flat", bd=0, cursor="hand2",
                      font=("Arial", 9, "bold"), padx=12, pady=7,
                      width=width, height=height)
        return b

    def show_home(self):
        self.clear()
        self.root.geometry("780x520")
        self.root.configure(bg=BG)

        outer = tk.Frame(self.root, bg=BG, highlightbackground="#b8d0d5",
                         highlightthickness=1)
        outer.pack(fill="both", expand=True, padx=10, pady=10)

        title = tk.Frame(outer, bg=BLUE, height=56)
        title.pack(fill="x", padx=0, pady=0)
        title.pack_propagate(False)
        tk.Label(title, text="SIMPLE IN-MEMORY STOCK APPLICATION",
                 bg=BLUE, fg="white", font=("Arial", 17, "bold")).pack(
                     pady=(7, 0))
        tk.Label(title, text="TAMPILAN UTAMA SEDERHANA",
                 bg=BLUE, fg="#e7f4f6", font=("Arial", 9)).pack()

        menu = tk.Frame(outer, bg=BG)
        menu.pack(expand=True)

        
        cards = [
            ("📦  ↑", "1. STOK BARANG\nMASUK", self.show_inbound, BLUE),
            ("🛒  ↓", "2. STOK BARANG\nKELUAR", self.show_outbound, TEAL),
            ("⏻", "3. KELUAR\nAPLIKASI", self.root.destroy, RED),
        ]

        for i, (symbol, label, action, color) in enumerate(cards):
            card = tk.Frame(menu, bg=color, width=185, height=185,
                            highlightbackground="#d4e5e8",
                            highlightthickness=2)
            card.grid(row=0, column=i, padx=12, pady=20)
            card.pack_propagate(False)
            tk.Button(card, text=symbol, command=action, bg=color, fg=INK if i < 2 else "#333333", activebackground=color,
                      relief="flat", bd=0, font=("Arial", 39, "bold"),
                      cursor="hand2").pack(expand=True, pady=(12, 0))
            tk.Button(card, text=label, command=action, bg=color, fg="white",
                      activebackground=color, activeforeground="white",
                      relief="flat", bd=0, font=("Arial", 12, "bold"),
                      cursor="hand2").pack(pady=(0, 14))
            
    def show_inbound(self):
        self.clear()
        self.root.geometry("1180x680")
        self.root.configure(bg=BG)

        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=8, pady=8)

        self.build_inbound_panel(container)

    def show_outbound(self):
        self.clear()
        self.root.geometry("1180x680")
        self.root.configure(bg=BG)

        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=8, pady=8)

        self.build_outbound_panel(container)

    def panel_title(self, parent, title):
        bar = tk.Frame(parent, bg=BLUE, height=46)
        bar.pack(fill="x", pady=(0, 12))
        bar.pack_propagate(False)
        tk.Label(bar, text=title, bg=BLUE, fg="white",
                 font=("Arial", 15, "bold")).pack(expand=True)

    def build_table(self, parent, columns, headings, widths):
        frame = tk.Frame(parent, bg=BG, highlightbackground="#b7cdd1",
                         highlightthickness=1)
        frame.pack(fill="x", padx=5, pady=(0, 12))
        tree = ttk.Treeview(frame, columns=columns, show="headings",
                            height=5, style="Stock.Treeview")
        for col, heading, width in zip(columns, headings, widths):
            tree.heading(col, text=heading)
            tree.column(col, width=width, minwidth=45, anchor="center",
                        stretch=True)
        tree.pack(fill="x", padx=2, pady=2)
        return tree

    def form_box(self, parent, title, color):
        box = tk.Frame(parent, bg=color, padx=12, pady=8,
                       highlightbackground="#b5d0d3", highlightthickness=1)
        box.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        tk.Label(box, text=title, bg=color, fg="white",
                 font=("Arial", 13, "bold")).pack(pady=(0, 8))
        return box

    def field(self, parent, label, default="", readonly=False):
        row = tk.Frame(parent, bg=parent["bg"])
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label, bg=parent["bg"], fg=INK,
                 width=12, anchor="w", font=("Arial", 9)).pack(side="left")
        var = tk.StringVar(value=default)
        entry = ttk.Entry(row, textvariable=var, font=("Arial", 9))
        entry.pack(side="left", fill="x", expand=True, ipady=3)
        if readonly:
            entry.configure(state="readonly")
        return var, entry

    def build_inbound_panel(self, parent):
        self.panel_title(parent, "STOK BARANG MASUK")
        self.in_tree = self.build_table(
            parent,
            ("no", "sku", "name", "category", "qty", "unit", "date"),
            ("No.", "Kode SKU", "Nama Barang", "Kategori",
             "Qty Masuk", "Satuan", "Tanggal Masuk"),
            (30, 75, 105, 75, 65, 55, 85)
        )

        box = self.form_box(parent, "TAMBAH BARANG MASUK", BLUE_DARK)
        self.in_sku, _ = self.field(box, "Kode SKU")
        self.in_name, _ = self.field(box, "Nama Barang")
        self.in_qty, _ = self.field(box, "Qty Masuk")
        self.in_unit, _ = self.field(box, "Satuan", "Pcs")
        self.in_note, _ = self.field(box, "Keterangan")

        buttons = tk.Frame(box, bg=BLUE_DARK)
        buttons.pack(fill="x", pady=(8, 0))
        self.make_button(buttons, "1. PROSES MASUK", self.process_in,
                         BLUE, width=15).pack(side="left", padx=(0, 5))
        self.make_button(buttons, "2. BATAL MASUK", self.clear_in,
                         WHITE, fg=INK, width=15).pack(side="left", padx=5)
        self.make_button(buttons, "3. KEMBALI KE\nMENU UTAMA", self.show_home,
                         "#b4a94b", width=16).pack(side="right")

        self.refresh_inbound()

    def build_outbound_panel(self, parent):
        self.panel_title(parent, "STOK BARANG KELUAR")
        self.out_tree = self.build_table(
            parent,
            ("no", "sku", "name", "qty", "destination", "date"),
            ("No.", "Kode SKU", "Nama Barang", "Qty Keluar",
             "Tujuan", "Tanggal Keluar"),
            (30, 75, 110, 75, 95, 90)
        ) 
        box = self.form_box(parent, "TAMBAH BARANG KELUAR", TEAL_DARK)
        row = tk.Frame(box, bg=TEAL_DARK)
        row.pack(fill="x", pady=3)
        tk.Label(row, text="Kode SKU", bg=TEAL_DARK, fg=INK,
                 width=12, anchor="w", font=("Arial", 9)).pack(side="left")
        self.out_sku = tk.StringVar()
        sku_combo = ttk.Combobox(row, textvariable=self.out_sku,
                                 values=list(self.products.keys()),
                                 state="readonly", font=("Arial", 9))
        sku_combo.pack(side="left", fill="x", expand=True, ipady=2)
        sku_combo.bind("<<ComboboxSelected>>", self.select_product)

        self.out_name, _ = self.field(box, "Nama Barang", readonly=True)
        self.out_qty, _ = self.field(box, "Qty Keluar")
        self.out_destination, _ = self.field(box, "Tujuan", "Pelanggan A")
        self.out_note, _ = self.field(box, "Nota", "Nota")

        buttons = tk.Frame(box, bg=TEAL_DARK)
        buttons.pack(fill="x", pady=(8, 0))
        self.make_button(buttons, "1. PROSES KELUAR", self.process_out,
                         BLUE, width=15).pack(side="left", padx=(0, 5))
        self.make_button(buttons, "2. BATAL KELUAR", self.clear_out,
                         WHITE, fg=INK, width=15).pack(side="left", padx=5)
        self.make_button(buttons, "3. KEMBALI KE\nMENU UTAMA", self.show_home,
                         RED, width=16).pack(side="right")

        

 
if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
        
