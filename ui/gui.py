import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from lexer.lexer import Lexer
from lexer.symbol_table import SymbolTable
from parser.parser import Parser
from parser.semantic_analyzer import SemanticAnalyzer
from parser.ast_nodes import export_ast_text


class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Two-Pass Compiler - Student ID: 230601008")
        self.root.geometry("1280x800")
        self.root.minsize(1000, 650)

        # --- KOYU TEMA RENK PALETİ ---
        self.bg_dark = "#1e1e1e"  # Ana arka plan
        self.bg_panel = "#252526"  # Panellerin arka planı
        self.bg_input = "#2d2d2d"  # Metin alanlarının içi
        self.fg_light = "#d4d4d4"  # Genel açık renk metinler
        self.accent_blue = "#007acc"  # Canlı VS Code Mavisi
        self.accent_green = "#4ec9b0"  # Canlı Neon Yeşil (Başarı)
        self.accent_orange = "#ce9178"  # Canlı Turuncu

        self.root.configure(bg=self.bg_dark)

        # Stilleri Yapılandır
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Sekme Tasarımları
        self.style.configure("TNotebook", background=self.bg_dark, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.bg_panel, foreground=self.fg_light,
                             font=("Arial", 10, "bold"), padding=[12, 6])
        self.style.map("TNotebook.Tab", background=[("selected", self.accent_blue)], foreground=[("selected", "white")])

        # Tablo (Treeview) Tasarımları
        self.style.configure("Treeview", background=self.bg_input, fieldbackground=self.bg_input,
                             foreground=self.fg_light, font=("Consolas", 10), rowheight=26)
        self.style.configure("Treeview.Heading", background=self.bg_panel, foreground=self.fg_light,
                             font=("Arial", 10, "bold"), borderwidth=1)
        self.style.map("Treeview.Heading", background=[("active", self.accent_blue)])

        # Çerçeve Stilleri
        self.style.configure("TLabelframe", background=self.bg_dark, foreground=self.fg_light,
                             font=("Arial", 11, "bold"))
        self.style.configure("TLabelframe.Label", background=self.bg_dark, foreground=self.accent_green)

        # Canlı Buton Stilleri
        self.style.configure("Compile.TButton", font=("Arial", 11, "bold"), background=self.accent_green,
                             foreground="black")
        self.style.map("Compile.TButton", background=[("active", "#3eb39a")])

        self.style.configure("Sample.TButton", font=("Arial", 10, "bold"), background=self.accent_blue,
                             foreground="white")
        self.style.map("Sample.TButton", background=[("active", "#0062a3")])

        self.create_widgets()

    def create_widgets(self):
        # --- ÜST MENÜ BAR ---
        menubar = tk.Menu(self.root, bg=self.bg_panel, fg=self.fg_light, activebackground=self.accent_blue)
        filemenu = tk.Menu(menubar, tearoff=0, bg=self.bg_panel, fg=self.fg_light)
        filemenu.add_command(label="Dosya Aç", command=self.open_file)
        filemenu.add_separator()
        filemenu.add_command(label="Çıkış", command=self.root.quit)
        menubar.add_cascade(label="Dosya", menu=filemenu)
        self.root.config(menu=menubar)

        # --- ANA PANEL ---
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # ================= SOL TARAF: EDİTÖR =================
        left_frame = ttk.Labelframe(main_paned, text=" KAYNAK KOD EDİTÖRÜ ", padding=8)
        main_paned.add(left_frame, weight=1)

        editor_frame = ttk.Frame(left_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        self.code_input = tk.Text(editor_frame, font=("Consolas", 12), wrap=tk.NONE, undo=True,
                                  bg=self.bg_input, fg="#9cdcfe", insertbackground="white",
                                  selectbackground="#264f78", bd=0, padx=8, pady=8)

        scrollbar_y = ttk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self.code_input.yview)
        scrollbar_x = ttk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=self.code_input.xview)
        self.code_input.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.code_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.compile_btn = ttk.Button(left_frame, text="⚡ KODU DERLE (RUN COMPILER)", style="Compile.TButton",
                                      command=self.compile_code)
        self.compile_btn.pack(fill=tk.X, pady=(8, 0), ipady=5)

        self.load_sample_btn = ttk.Button(left_frame, text="📋 Örnek Senaryo Yükle", style="Sample.TButton",
                                          command=self.load_sample)
        self.load_sample_btn.pack(fill=tk.X, pady=(4, 0), ipady=3)

        # ================= SAĞ TARAF: SEKMELER =================
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Token Stream
        self.token_tab = ttk.Frame(self.notebook, style="TNotebook")
        self.notebook.add(self.token_tab, text=" Token Stream ")
        self.setup_token_treeview()

        # Tab 2: Sembol Tablosu
        self.symbol_tab = ttk.Frame(self.notebook, style="TNotebook")
        self.notebook.add(self.symbol_tab, text=" Sembol Tablosu ")
        self.setup_symbol_treeview()

        # Tab 3: AST
        self.ast_tab = ttk.Frame(self.notebook, style="TNotebook")
        self.notebook.add(self.ast_tab, text=" AST (Ağaç Yapısı) ")
        self.setup_ast_view()

        # Tab 4: Hata Raporu
        self.error_tab = ttk.Frame(self.notebook, style="TNotebook")
        self.notebook.add(self.error_tab, text=" Hata Raporu ")
        self.setup_error_view()

    def setup_token_treeview(self):
        columns = ("line", "token", "type")
        self.token_tree = ttk.Treeview(self.token_tab, columns=columns, show="headings")
        self.token_tree.heading("line", text="Satır No")
        self.token_tree.heading("token", text="Ham Kelime (Lexeme)")
        self.token_tree.heading("type", text="Token Tipi")

        self.token_tree.column("line", width=80, anchor=tk.CENTER)
        self.token_tree.column("token", width=200, anchor=tk.W)
        self.token_tree.column("type", width=200, anchor=tk.W)

        scroll = ttk.Scrollbar(self.token_tab, orient=tk.VERTICAL, command=self.token_tree.yview)
        self.token_tree.configure(yscrollcommand=scroll.set)
        self.token_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_symbol_treeview(self):
        columns = ("name", "type", "scope", "address")
        self.symbol_tree = ttk.Treeview(self.symbol_tab, columns=columns, show="headings")
        self.symbol_tree.heading("name", text="Değişken Adı")
        self.symbol_tree.heading("type", text="Veri Tipi")
        self.symbol_tree.heading("scope", text="Kapsam (Scope)")
        self.symbol_tree.heading("address", text="Hafıza Adresi")

        self.symbol_tree.column("name", width=150, anchor=tk.W)
        self.symbol_tree.column("type", width=100, anchor=tk.CENTER)
        self.symbol_tree.column("scope", width=100, anchor=tk.CENTER)
        self.symbol_tree.column("address", width=120, anchor=tk.CENTER)

        scroll = ttk.Scrollbar(self.symbol_tab, orient=tk.VERTICAL, command=self.symbol_tree.yview)
        self.symbol_tree.configure(yscrollcommand=scroll.set)
        self.symbol_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_ast_view(self):
        self.ast_text = tk.Text(self.ast_tab, font=("Consolas", 12, "bold"), bg=self.bg_input, fg="#b5cea8",
                                state=tk.DISABLED, bd=0, padx=12, pady=12)
        scroll = ttk.Scrollbar(self.ast_tab, orient=tk.VERTICAL, command=self.ast_text.yview)
        self.ast_text.configure(yscrollcommand=scroll.set)
        self.ast_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_error_view(self):
        # Listbox scroll entegrasyonu
        scroll = ttk.Scrollbar(self.error_tab, orient=tk.VERTICAL)

        # DÜZELTİLDİ: padx ve pady parametreleri buradan kaldırıldı!
        self.error_listbox = tk.Listbox(self.error_tab, font=("Consolas", 11, "bold"), fg="#f44336",
                                        bg=self.bg_input, bd=0, highlightthickness=0,
                                        yscrollcommand=scroll.set)
        scroll.config(command=self.error_listbox.yview)

        # DÜZELTİLDİ: İç boşluklar (padx/pady) pack fonksiyonunun içine taşındı
        self.error_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=12)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.code_input.delete("1.0", tk.END)
                self.code_input.insert("1.0", f.read())

    def load_sample(self):
        sample = "int x;\nint y;\nfloat result;\n\nx = 10;\ny = 3;\nresult = x + y * 2;\n\nif (result > 15) {\n    print(\"Result is large\");\n} else {\n    print(\"Result is small\");\n}\n\nwhile (x > 0) {\n    x = x - 1;\n}"
        self.code_input.delete("1.0", tk.END)
        self.code_input.insert("1.0", sample)

    def compile_code(self):
        # Ekranları Temizle
        self.token_tree.delete(*self.token_tree.get_children())
        self.symbol_tree.delete(*self.symbol_tree.get_children())
        self.error_listbox.delete(0, tk.END)
        self.update_text_area(self.ast_text, "")

        source_code = self.code_input.get("1.0", tk.END).strip()
        if not source_code:
            messagebox.showwarning("Uyarı", "Lütfen önce kaynak kod giriniz!")
            return

        # 1. PASS: Lexer
        lexer = Lexer(source_code)
        tokens, lexical_errors = lexer.tokenize()

        for t in tokens:
            self.token_tree.insert("", tk.END, values=(f"{t.line:02d}", t.value, t.type.name))

        if lexical_errors:
            for err in lexical_errors:
                self.error_listbox.insert(tk.END, f"❌ [LEXICAL ERROR] {err}")
            self.error_listbox.configure(fg="#f44336")
            self.notebook.select(3)
            return

        # 2. PASS: Parser
        parser = Parser(tokens)
        ast_root, syntax_errors = parser.parse()

        if syntax_errors:
            for err in syntax_errors:
                self.error_listbox.insert(tk.END, f"❌ [SYNTAX ERROR] {err}")
            self.error_listbox.configure(fg="#f44336")
            self.notebook.select(3)
            return

        # 3. PASS: Semantic Analysis
        symbol_table = SymbolTable()
        analyzer = SemanticAnalyzer(symbol_table)
        semantic_errors = analyzer.analyze(ast_root)

        for sym in symbol_table.get_all_symbols():
            self.symbol_tree.insert("", tk.END, values=(sym.name, sym.type, sym.scope, sym.memory_location))

        if semantic_errors:
            for err in semantic_errors:
                self.error_listbox.insert(tk.END, f"❌ [SEMANTIC ERROR] {err}")
            self.error_listbox.configure(fg="#f44336")
            self.notebook.select(3)
            return

        # Derleme Başarılıysa Çıktıları Bas
        ast_string = export_ast_text(ast_root)
        self.update_text_area(self.ast_text, ast_string)

        self.error_listbox.configure(fg=self.accent_green)
        self.error_listbox.insert(tk.END, "✅ Compilation successful. Zero errors found.")
        self.notebook.select(0)

    def update_text_area(self, text_widget, content):
        text_widget.configure(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", content)
        text_widget.configure(state=tk.DISABLED)


def launch_gui():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()