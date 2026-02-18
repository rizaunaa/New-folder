import tkinter as tk


def _blend_border_color(parent: tk.Widget, bg_color: str, opacity: float = 0.18) -> str:
    r16, g16, b16 = parent.winfo_rgb(bg_color)
    r = r16 // 256
    g = g16 // 256
    b = b16 // 256
    border_r = int(r * (1 - opacity))
    border_g = int(g * (1 - opacity))
    border_b = int(b * (1 - opacity))
    return f"#{border_r:02x}{border_g:02x}{border_b:02x}"


def create_output_display(parent: tk.Widget, value: str) -> tk.Label:
    bg_color = parent.cget("bg")
    border_color = _blend_border_color(parent, bg_color)
    label = tk.Label(
        parent,
        text=f"{value}",
        font=("Segoe UI", 12),
        pady=8,
        bd=0,
        relief="flat",
        highlightthickness=1,
        highlightbackground=border_color,
        highlightcolor=border_color,
    )

    parent.update_idletasks()
    width = max(parent.winfo_width(), 1)
    horizontal_pad = max(int(width * 0.05), 8)
    label.pack(fill="x", padx=horizontal_pad, pady=20)

    def _on_resize(event: tk.Event) -> None:
        new_pad = max(int(event.width * 0.05), 8)
        label.pack_configure(padx=new_pad)

    parent.bind("<Configure>", _on_resize, add="+")
    return label
