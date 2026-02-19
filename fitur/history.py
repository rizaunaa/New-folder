from collections import deque
import tkinter as tk
from tkinter import ttk


class HistoryStore:
    def __init__(self, max_items: int = 100) -> None:
        self._items: deque[tuple[str, str]] = deque(maxlen=max_items)

    def add(self, expression: str, result: str) -> None:
        self._items.append((expression, result))

    def all(self) -> list[tuple[str, str]]:
        return list(self._items)

    def clear(self) -> None:
        self._items.clear()


def _center_window(window: tk.Toplevel, width: int, height: int) -> None:
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_history_table(parent: tk.Widget, rows: list[tuple[str, str]]) -> None:
    window = tk.Toplevel(parent)
    try:
        parent_icon = parent.iconbitmap()
        if parent_icon:
            window.iconbitmap(default=parent_icon)
    except tk.TclError:
        pass
    window.title("Histori")
    _center_window(window, 420, 300)

    table = ttk.Treeview(
        window,
        columns=("expression", "result"),
        show="headings",
    )
    table.heading("expression", text="Ekspresi")
    table.heading("result", text="Hasil")
    table.column("expression", anchor="w", width=280)
    table.column("result", anchor="center", width=120)

    for expression, result in rows:
        table.insert("", "end", values=(expression, result))

    scroll = ttk.Scrollbar(window, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scroll.set)

    table.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=12)
    scroll.pack(side="right", fill="y", padx=(0, 12), pady=12)
