import random
import math
import tkinter as tk


class DisplayFlameEffect:
    def __init__(self, root: tk.Misc, display: tk.Widget) -> None:
        self.root = root
        self.display = display
        self._overlay: tk.Toplevel | None = None
        self._canvas: tk.Canvas | None = None
        self._active = 0
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

    def trigger(self) -> None:
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

        left = self.display.winfo_rootx() - root_x
        top = self.display.winfo_rooty() - root_y
        width = self.display.winfo_width()
        height = self.display.winfo_height()
        right = left + width
        bottom = top + height
        center_x = left + (width / 2)
        center_y = top + (height / 2)

        self._active += 1
        self._radial_spread(center_x, center_y, left + 4, right - 4, top + 4, bottom - 4)
        self._ring(center_x, center_y, 0)
        self._edge_embers(left, right, top, bottom)
        self.root.after(380, self._finish)

    def _radial_spread(
        self,
        center_x: float,
        center_y: float,
        left: float,
        right: float,
        top: float,
        bottom: float,
    ) -> None:
        if self._canvas is None:
            return
        rays = 24
        angle_step = (2 * math.pi) / rays
        for i in range(rays):
            angle = i * angle_step
            dx = math.cos(angle)
            dy = math.sin(angle)
            distance = self._distance_to_edge(center_x, center_y, dx, dy, left, right, top, bottom)
            if distance <= 0:
                continue
            target_x = center_x + (dx * distance)
            target_y = center_y + (dy * distance)
            self._launch_streak(center_x, center_y, target_x, target_y, 0)

    def _distance_to_edge(
        self,
        cx: float,
        cy: float,
        dx: float,
        dy: float,
        left: float,
        right: float,
        top: float,
        bottom: float,
    ) -> float:
        distances: list[float] = []
        if dx > 0:
            distances.append((right - cx) / dx)
        elif dx < 0:
            distances.append((left - cx) / dx)
        if dy > 0:
            distances.append((bottom - cy) / dy)
        elif dy < 0:
            distances.append((top - cy) / dy)
        positives = [d for d in distances if d > 0]
        return min(positives) if positives else 0.0

    def _launch_streak(self, sx: float, sy: float, tx: float, ty: float, frame: int) -> None:
        if self._canvas is None:
            return
        total_frames = 12
        if frame > total_frames:
            return
        t = frame / total_frames
        eased = 1 - pow(1 - t, 3)
        x = sx + (tx - sx) * eased
        y = sy + (ty - sy) * eased
        size = max(4 - (2 * t), 1.6)
        blob = self._canvas.create_oval(
            x - size,
            y - size,
            x + size,
            y + size,
            fill=("#ffd166", "#ffb347", "#ff8c00", "#ff6a00")[min(frame // 3, 3)],
            outline="",
        )
        self._fade_blob(blob, 0)
        self.root.after(16, lambda: self._launch_streak(sx, sy, tx, ty, frame + 1))

    def _ring(self, x: float, y: float, frame: int) -> None:
        if self._canvas is None:
            return
        if frame >= 7:
            return
        r = 8 + (frame * 4)
        ring = self._canvas.create_oval(x - r, y - r, x + r, y + r, outline="#ffd166", width=2)
        self._canvas.itemconfig(ring, outline=("#ffd166", "#ffb347", "#ff8c00")[min(frame // 3, 2)])
        self.root.after(40, lambda: self._canvas.delete(ring) if self._canvas is not None else None)
        self.root.after(22, lambda: self._ring(x, y, frame + 1))

    def _edge_embers(self, left: float, right: float, top: float, bottom: float) -> None:
        if self._canvas is None:
            return
        for _ in range(20):
            side = random.choice(("top", "right", "bottom", "left"))
            if side == "top":
                x = random.uniform(left, right)
                y = top
            elif side == "right":
                x = right
                y = random.uniform(top, bottom)
            elif side == "bottom":
                x = random.uniform(left, right)
                y = bottom
            else:
                x = left
                y = random.uniform(top, bottom)
            size = random.uniform(1.6, 3.2)
            ember = self._canvas.create_oval(x - size, y - size, x + size, y + size, fill="#ffb347", outline="")
            dx = random.uniform(-12, 12)
            dy = random.uniform(-10, 10)
            self._drift_ember(ember, dx, dy, 0)

    def _fade_blob(self, blob: int, frame: int) -> None:
        if self._canvas is None:
            return
        colors = ("#ffd166", "#ffb347", "#ff8c00", "#ff6a00", "#d9480f")
        if frame >= len(colors):
            self._canvas.delete(blob)
            return
        if not self._canvas.coords(blob):
            return
        self._canvas.itemconfig(blob, fill=colors[frame])
        self.root.after(18, lambda: self._fade_blob(blob, frame + 1))

    def _drift_ember(self, ember: int, dx: float, dy: float, frame: int) -> None:
        if self._canvas is None:
            return
        colors = ("#ffd166", "#ffb347", "#ff8c00", "#ff6a00", "#e85d04")
        total = len(colors)
        if frame >= total:
            self._canvas.delete(ember)
            return
        if not self._canvas.coords(ember):
            return
        self._canvas.move(ember, dx / total, dy / total)
        self._canvas.itemconfig(ember, fill=colors[frame])
        self.root.after(18, lambda: self._drift_ember(ember, dx, dy, frame + 1))

    def _finish(self) -> None:
        if self._overlay is None or self._canvas is None:
            return
        self._active = max(self._active - 1, 0)
        if self._active == 0:
            self._canvas.delete("all")
            self._overlay.withdraw()
