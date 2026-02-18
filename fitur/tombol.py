import tkinter as tk
from typing import Callable


def create_keypad(parent: tk.Widget, on_press: Callable[[str], None]) -> tk.Frame:
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    layout = [
        (0, 0, "1", "1", 1),
        (0, 1, "2", "2", 1),
        (0, 2, "3", "3", 1),
        (0, 3, "+", "+", 1),
        (1, 0, "4", "4", 1),
        (1, 1, "5", "5", 1),
        (1, 2, "6", "6", 1),
        (1, 3, "-", "-", 1),
        (2, 0, "7", "7", 1),
        (2, 1, "8", "8", 1),
        (2, 2, "9", "9", 1),
        (2, 3, "x", "*", 1),
        (3, 1, "0", "0", 1),
        (3, 3, "/", "/", 1),
        (4, 0, "=", "=", 4),
    ]

    for row, column, label, value, span in layout:
        button = tk.Button(
            frame,
            text=label,
            height=2,
            command=lambda key_value=value: on_press(key_value),
        )
        button.grid(
            row=row,
            column=column,
            columnspan=span,
            padx=6,
            pady=6,
            sticky="nsew",
        )

    for column in range(4):
        frame.grid_columnconfigure(column, weight=1)
    for row in range(5):
        frame.grid_rowconfigure(row, weight=1)

    return frame
