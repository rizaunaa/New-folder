import tkinter as tk
from typing import Callable


def create_keypad(parent: tk.Widget, on_press: Callable[[str], None]) -> tk.Frame:
    frame = tk.Frame(parent)
    frame.pack(fill="x", padx=20, pady=(0, 20))

    keys = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "+",
        "-",
        "*",
        "/",
        "=",
    ]

    for index, key in enumerate(keys):
        row = index // 3
        column = index % 3
        button = tk.Button(
            frame,
            text=key,
            width=8,
            height=2,
            command=lambda value=key: on_press(value),
        )
        button.grid(row=row, column=column, padx=6, pady=6, sticky="nsew")

    for column in range(3):
        frame.grid_columnconfigure(column, weight=1)

    return frame
