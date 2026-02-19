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


def create_history_sidebar(parent: tk.Widget) -> tuple[tk.Frame, ttk.Treeview]:
    sidebar = tk.Frame(parent, width=260, bd=1, relief="solid")
    sidebar.grid_propagate(False)

    header = tk.Frame(sidebar)
    header.pack(fill="x", padx=10, pady=(10, 6))
    title = tk.Label(header, text="Histori", font=("Segoe UI", 10, "bold"))
    title.pack(side="left")

    table_wrap = tk.Frame(sidebar)
    table_wrap.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    table = ttk.Treeview(
        table_wrap,
        columns=("expression", "result"),
        show="headings",
    )
    table.heading("expression", text="Ekspresi")
    table.heading("result", text="Hasil")
    table.column("expression", anchor="w", width=160)
    table.column("result", anchor="center", width=72)

    scroll = ttk.Scrollbar(table_wrap, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scroll.set)

    table.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    return sidebar, table


def update_history_sidebar(table: ttk.Treeview, rows: list[tuple[str, str]]) -> None:
    table.delete(*table.get_children())
    for expression, result in reversed(rows):
        table.insert("", "end", values=(expression, result))
