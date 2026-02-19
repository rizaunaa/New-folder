import random
import tkinter as tk


class BurningKeyEffect:
    def __init__(self, root: tk.Misc) -> None:
        self.root = root
        self._overlay: tk.Toplevel | None = None
        self._canvas: tk.Canvas | None = None
        self._active_overlay_fx = 0
        self._tokens: dict[int, int] = {}
        self._init_overlay()

    def _init_overlay(self) -> None:
        try:
            overlay = tk.Toplevel(self.root)
            overlay.withdraw()
            overlay.overrideredirect(True)
            overlay.attributes("-topmost", True)
            overlay.configure(bg="#ff00ff")
            overlay.attributes("-transparentcolor", "#ff00ff")

            canvas = tk.Canvas(overlay, highlightthickness=0, bd=0, bg="#ff00ff")
            canvas.pack(fill="both", expand=True)

            self._overlay = overlay
            self._canvas = canvas
        except tk.TclError:
            self._overlay = None
            self._canvas = None

    def trigger(self, button: tk.Widget) -> None:
        if str(button.cget("state")) == "disabled":
            return

        widget_id = id(button)
        token = self._tokens.get(widget_id, 0) + 1
        self._tokens[widget_id] = token

        original_bg = button.cget("bg")
        original_fg = button.cget("fg")
        original_relief = button.cget("relief")
        original_bd = int(button.cget("bd"))
        original_highlight_bg = button.cget("highlightbackground")
        original_padx = int(button.grid_info().get("padx", 0))
        original_pady = int(button.grid_info().get("pady", 0))

        button.configure(
            bg="#ff7a18",
            fg="#fff3d6",
            relief="raised",
            bd=3,
            highlightbackground="#ffd166",
            activebackground="#ff8f2f",
            activeforeground="#fff3d6",
        )

        self._run_button_fx(
            button=button,
            token=token,
            original_bg=original_bg,
            original_fg=original_fg,
            original_relief=original_relief,
            original_bd=original_bd,
            original_highlight_bg=original_highlight_bg,
            original_padx=original_padx,
            original_pady=original_pady,
            frame=0,
        )
        self._spawn_overlay_fx(button)

    def _run_button_fx(
        self,
        button: tk.Widget,
        token: int,
        original_bg: str,
        original_fg: str,
        original_relief: str,
        original_bd: int,
        original_highlight_bg: str,
        original_padx: int,
        original_pady: int,
        frame: int,
    ) -> None:
        if self._tokens.get(id(button)) != token:
            return

        frames = [
            ("#ff9b2f", "#fff3d6", 4),
            ("#ff6a00", "#ffe6b3", 2),
            ("#ffb347", "#fff8e1", 4),
            ("#ff5e00", "#ffe0a3", 2),
            ("#ff8a1f", "#fff3d6", 3),
        ]

        if frame >= len(frames):
            button.configure(
                bg=original_bg,
                fg=original_fg,
                relief=original_relief,
                bd=original_bd,
                highlightbackground=original_highlight_bg,
                activebackground=original_bg,
                activeforeground=original_fg,
            )
            button.grid_configure(padx=original_padx, pady=original_pady)
            return

        bg, fg, bd = frames[frame]
        button.configure(bg=bg, fg=fg, bd=bd)

        # Shake ringan via perubahan padding grid.
        shake = 1 if frame % 2 == 0 else -1
        button.grid_configure(padx=max(original_padx + shake, 0), pady=max(original_pady - shake, 0))

        self.root.after(
            52,
            lambda: self._run_button_fx(
                button=button,
                token=token,
                original_bg=original_bg,
                original_fg=original_fg,
                original_relief=original_relief,
                original_bd=original_bd,
                original_highlight_bg=original_highlight_bg,
                original_padx=original_padx,
                original_pady=original_pady,
                frame=frame + 1,
            ),
        )

    def _spawn_overlay_fx(self, button: tk.Widget) -> None:
        if self._overlay is None or self._canvas is None:
            return

        self.root.update_idletasks()
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_w = max(self.root.winfo_width(), 1)
        root_h = max(self.root.winfo_height(), 1)

        self._overlay.geometry(f"{root_w}x{root_h}+{root_x}+{root_y}")
        self._overlay.deiconify()
        self._overlay.lift()
        self._active_overlay_fx += 1

        x = button.winfo_rootx() - root_x + button.winfo_width() / 2
        y = button.winfo_rooty() - root_y + button.winfo_height() / 2

        ring = self._canvas.create_oval(x - 8, y - 8, x + 8, y + 8, outline="#ffd166", width=2)
        self._expand_ring(ring, 0)

        for _ in range(8):
            ember_size = random.uniform(1.6, 3.0)
            ember = self._canvas.create_oval(
                x - ember_size,
                y - ember_size,
                x + ember_size,
                y + ember_size,
                fill=random.choice(("#ffe3ad", "#ffb347", "#ff8c00")),
                outline="",
            )
            dx = random.uniform(-16, 16)
            dy = random.uniform(-14, 8)
            self._drift_ember(ember, dx, dy, 0)

        self.root.after(360, self._finish_overlay_fx)

    def _expand_ring(self, ring: int, frame: int) -> None:
        if self._canvas is None:
            return
        if frame >= 8:
            self._canvas.delete(ring)
            return
        coords = self._canvas.coords(ring)
        if len(coords) != 4:
            return
        x1, y1, x2, y2 = coords
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        radius = ((x2 - x1) / 2) + 2.2
        self._canvas.coords(ring, cx - radius, cy - radius, cx + radius, cy + radius)
        self._canvas.itemconfig(ring, outline=("#ffd166", "#ffb347", "#ff8c00")[min(frame // 3, 2)])
        self.root.after(26, lambda: self._expand_ring(ring, frame + 1))

    def _drift_ember(self, ember: int, dx: float, dy: float, frame: int) -> None:
        if self._canvas is None:
            return
        colors = ("#ffe3ad", "#ffbf66", "#ff9e3d", "#ff7f2a", "#e96a1e")
        total = len(colors)
        if frame >= total:
            self._canvas.delete(ember)
            return
        if not self._canvas.coords(ember):
            return
        self._canvas.move(ember, dx / total, dy / total)
        self._canvas.itemconfig(ember, fill=colors[frame])
        self.root.after(24, lambda: self._drift_ember(ember, dx, dy, frame + 1))

    def _finish_overlay_fx(self) -> None:
        if self._overlay is None or self._canvas is None:
            return
        self._active_overlay_fx = max(self._active_overlay_fx - 1, 0)
        if self._active_overlay_fx == 0:
            self._canvas.delete("all")
            self._overlay.withdraw()
