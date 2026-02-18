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


def show_history_table(parent: tk.Widget, rows: list[tuple[str, str]]) -> None:
    window = tk.Toplevel(parent)
    window.title("Histori")
    window.geometry("420x300")

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
