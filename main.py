import tkinter as tk
from tkinter import ttk, filedialog
from utils.paths import resource_path
import os

class FolderAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Analyzer")
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        toolbar = ttk.Frame(frame)
        toolbar.pack(fill="x")

        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(toolbar, textvariable=self.path_var, width=60)
        path_entry.pack(side="left", padx=5, pady=5)

        browse_btn = ttk.Button(toolbar, text="Browse", command=self.browse_folder)
        browse_btn.pack(side="left", padx=5)

        analyze_btn = ttk.Button(toolbar, text="Analyze", command=self.analyze_folder)
        analyze_btn.pack(side="left", padx=5)

        self.tree = ttk.Treeview(frame, columns=("size",), show="tree headings")
        self.tree.heading("#0", text="Folder")
        self.tree.heading("size", text="Size")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def analyze_folder(self):
        root_path = self.path_var.get()
        if not os.path.isdir(root_path):
            return
        self.tree.delete(*self.tree.get_children())
        self.walk_and_display(root_path, "", root_path)

    def walk_and_display(self, path, parent, root_path):
        total_size = 0
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                dir_size = self.get_folder_size(entry.path)
                display_name = entry.name
                node = self.tree.insert(parent, "end", text=display_name, values=(self.format_size(dir_size),))
                self.walk_and_display(entry.path, node, root_path)
                total_size += dir_size
            elif entry.is_file():
                total_size += entry.stat().st_size
        return total_size

    def get_folder_size(self, path):
        total = 0
        for root, dirs, files in os.walk(path, topdown=True):
            for f in files:
                try:
                    fp = os.path.join(root, f)
                    total += os.path.getsize(fp)
                except Exception:
                    continue
        return total

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

def run_app():
    root = tk.Tk()
    app = FolderAnalyzerApp(root)
    root.mainloop()
