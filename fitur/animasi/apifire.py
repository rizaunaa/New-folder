import math
import random
import tkinter as tk
from collections.abc import Callable


class FireVisualEffect:
    def __init__(self, root: tk.Misc, canvas: tk.Canvas, display: tk.Widget) -> None:
        self.root = root
        self.display = display
        self.fire_color = "#FF4500"

        self._fallback_canvas = canvas
        self._canvas = canvas
        self._overlay: tk.Toplevel | None = None
        self._use_overlay = False
        self._active_particles = 0
        self._canvas_x = 0
        self._canvas_y = 0

        self._init_overlay()

    def _init_overlay(self) -> None:
        try:
            overlay = tk.Toplevel(self.root)
            overlay.withdraw()
            overlay.overrideredirect(True)
            overlay.attributes("-topmost", True)
            overlay.configure(bg="#ff00ff")
            overlay.attributes("-transparentcolor", "#ff00ff")

            canvas = tk.Canvas(
                overlay,
                highlightthickness=0,
                bd=0,
                bg="#ff00ff",
            )
            canvas.pack(fill="both", expand=True)

            self._overlay = overlay
            self._canvas = canvas
            self._use_overlay = True
        except tk.TclError:
            self._overlay = None
            self._canvas = self._fallback_canvas
            self._use_overlay = False

    def launch_fire(
        self,
        source_widget: tk.Widget,
        on_impact: Callable[[], None] | None = None,
    ) -> None:
        self.root.update_idletasks()
        self._prepare_layer(source_widget)

        x_start, y_start = self._center_in_layer(source_widget)
        x_end, y_end = self._center_in_layer(self.display)

        glow = self._canvas.create_oval(
            x_start - 22,
            y_start - 22,
            x_start + 22,
            y_start + 22,
            fill="#ffd9a3",
            outline="",
        )
        particle = self._canvas.create_oval(
            x_start - 14,
            y_start - 14,
            x_start + 14,
            y_start + 14,
            fill=self.fire_color,
            outline="#FFD700",
            width=2,
        )
        self._canvas.tag_lower(glow, particle)
        self._active_particles += 1

        self._animate_path(
            particle=particle,
            glow=glow,
            x_start=x_start,
            y_start=y_start,
            x_end=x_end,
            y_end=y_end,
            step=0,
            on_impact=on_impact,
        )

    def _prepare_layer(self, source_widget: tk.Widget) -> None:
        if self._use_overlay and self._overlay is not None:
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            width = max(self.root.winfo_width(), 1)
            height = max(self.root.winfo_height(), 1)
            self._overlay.geometry(f"{width}x{height}+{x}+{y}")
            self._overlay.deiconify()
            self._overlay.lift()
            self._canvas_x = 0
            self._canvas_y = 0
            return

        x_start, y_start = self._center_in_root(source_widget)
        x_end, y_end = self._center_in_root(self.display)
        margin = 70
        min_x = int(min(x_start, x_end) - margin)
        min_y = int(min(y_start, y_end) - margin)
        max_x = int(max(x_start, x_end) + margin)
        max_y = int(max(y_start, y_end) + margin)
        width = max(max_x - min_x, 1)
        height = max(max_y - min_y, 1)

        self._canvas_x = min_x
        self._canvas_y = min_y
        self._canvas.place(x=min_x, y=min_y, width=width, height=height)
        self._canvas.tk.call("raise", self._canvas._w)

    def _center_in_root(self, widget: tk.Widget) -> tuple[float, float]:
        x = widget.winfo_rootx() - self.root.winfo_rootx() + (widget.winfo_width() / 2)
        y = widget.winfo_rooty() - self.root.winfo_rooty() + (widget.winfo_height() / 2)
        return x, y

    def _center_in_layer(self, widget: tk.Widget) -> tuple[float, float]:
        if self._use_overlay:
            x = widget.winfo_rootx() - self.root.winfo_rootx() + (widget.winfo_width() / 2)
            y = widget.winfo_rooty() - self.root.winfo_rooty() + (widget.winfo_height() / 2)
            return x, y

        x, y = self._center_in_root(widget)
        return x - self._canvas_x, y - self._canvas_y

    def _animate_path(
        self,
        particle: int,
        glow: int,
        x_start: float,
        y_start: float,
        x_end: float,
        y_end: float,
        step: int,
        on_impact: Callable[[], None] | None,
    ) -> None:
        total_steps = 28

        if step <= total_steps:
            t = step / total_steps
            eased = 1 - pow(1 - t, 3)
            next_x = x_start + (x_end - x_start) * eased
            arc = math.sin(t * math.pi) * 58
            next_y = y_start + (y_end - y_start) * eased - arc
            next_x += random.uniform(-0.7, 0.7)
            next_y += random.uniform(-0.6, 0.6)

            radius = 14 - (4 * t)
            self._canvas.coords(
                particle,
                next_x - radius,
                next_y - radius,
                next_x + radius,
                next_y + radius,
            )
            self._canvas.itemconfig(particle, fill=("#FFB347", "#FF8C00", "#FF4500")[step % 3])

            glow_radius = 22 - (6 * t)
            self._canvas.coords(
                glow,
                next_x - glow_radius,
                next_y - glow_radius,
                next_x + glow_radius,
                next_y + glow_radius,
            )
            self._canvas.itemconfig(glow, fill=("#ffd9a3", "#ffc777")[step % 2])
            self._spawn_trail(next_x, next_y)

            self.root.after(
                12,
                lambda: self._animate_path(
                    particle,
                    glow,
                    x_start,
                    y_start,
                    x_end,
                    y_end,
                    step + 1,
                    on_impact,
                ),
            )
            return

        self._canvas.delete(particle)
        self._canvas.delete(glow)
        self._impact_burst(x_end, y_end)
        self.flash_display()
        if on_impact is not None:
            on_impact()

        self._active_particles = max(self._active_particles - 1, 0)
        if self._active_particles == 0:
            self.root.after(120, self._hide_layer)

    def _spawn_trail(self, x: float, y: float) -> None:
        trail_radius = random.uniform(3.0, 6.0)
        trail = self._canvas.create_oval(
            x - trail_radius,
            y - trail_radius,
            x + trail_radius,
            y + trail_radius,
            fill=random.choice(("#FFB347", "#FF8C00", "#FF6A00")),
            outline="",
        )
        self._fade_particle(trail, 0)

    def _impact_burst(self, x: float, y: float) -> None:
        ring = self._canvas.create_oval(x - 8, y - 8, x + 8, y + 8, outline="#FFD700", width=2)
        self._expand_ring(ring, 0)
        for _ in range(10):
            radius = random.uniform(2.0, 4.0)
            ember = self._canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=random.choice(("#ffe3ad", "#ffb347", "#ff8c00")),
                outline="",
            )
            self._drift_particle(
                ember,
                random.uniform(-20, 20),
                random.uniform(-16, 10),
                0,
            )

    def _expand_ring(self, ring: int, frame: int) -> None:
        if frame >= 10:
            self._canvas.delete(ring)
            return
        coords = self._canvas.coords(ring)
        if len(coords) != 4:
            return
        x1, y1, x2, y2 = coords
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        radius = ((x2 - x1) / 2) + 2.5
        self._canvas.coords(ring, cx - radius, cy - radius, cx + radius, cy + radius)
        self._canvas.itemconfig(ring, outline=("#FFD700", "#FFB347", "#FF8C00")[min(frame // 4, 2)])
        self.root.after(16, lambda: self._expand_ring(ring, frame + 1))

    def _fade_particle(self, particle: int, frame: int) -> None:
        colors = ("#ff8c00", "#ff6a00", "#f25c05", "#d9480f", "#b53b12")
        if frame >= len(colors):
            self._canvas.delete(particle)
            return
        if not self._canvas.coords(particle):
            return
        self._canvas.itemconfig(particle, fill=colors[frame])
        self.root.after(14, lambda: self._fade_particle(particle, frame + 1))

    def _drift_particle(self, particle: int, dx: float, dy: float, frame: int) -> None:
        colors = ("#ffe3ad", "#ffbf66", "#ff9e3d", "#ff7f2a", "#e96a1e", "#cf5716")
        total = len(colors)
        if frame >= total:
            self._canvas.delete(particle)
            return
        if not self._canvas.coords(particle):
            return
        self._canvas.move(particle, dx / total, dy / total)
        self._canvas.itemconfig(particle, fill=colors[frame])
        self.root.after(14, lambda: self._drift_particle(particle, dx, dy, frame + 1))

    def flash_display(self) -> None:
        try:
            original = self.display.cget("fg_color")
            self.display.configure(fg_color="#4a4a4a")
            self.root.after(100, lambda: self.display.configure(fg_color=original))
            return
        except tk.TclError:
            pass

        original_bg = self.display.cget("bg")
        self.display.configure(bg="#4a4a4a")
        self.root.after(100, lambda: self.display.configure(bg=original_bg))

    def _hide_layer(self) -> None:
        if self._use_overlay and self._overlay is not None:
            self._canvas.delete("all")
            self._overlay.withdraw()
            return

        self._canvas.tk.call("lower", self._canvas._w)
        self._canvas.place_forget()
