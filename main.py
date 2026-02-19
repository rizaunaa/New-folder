import tkinter as tk
from pathlib import Path
import sys

from fitur.animasi.apifire import FireVisualEffect
from fitur.animasi.displayapi import DisplayFlameEffect
from fitur.animasi.keyterbakar import BurningKeyEffect
from fitur.display import create_output_display
from fitur.history import HistoryStore, show_history_table
from fitur.logikaoperasinalmtk import OPERATORS, process_input
from fitur.tombol import create_keypad


def set_windows_app_id() -> None:
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("riza.kalkulator.app")
    except Exception:
        pass


def apply_window_icon(window: tk.Tk) -> None:
    icon_path = Path(__file__).resolve().with_name("icon.ico")

    icon_candidates = [
        str(icon_path),
        sys.executable,
    ]
    for candidate in icon_candidates:
        try:
            if candidate == str(icon_path) and not icon_path.exists():
                continue
            window.iconbitmap(default=candidate)
            break
        except tk.TclError:
            continue

    # Force icon for Windows title bar/task switcher using WinAPI.
    try:
        import ctypes

        IMAGE_ICON = 1
        LR_LOADFROMFILE = 0x0010
        LR_DEFAULTSIZE = 0x0040
        WM_SETICON = 0x0080
        ICON_SMALL = 0
        ICON_BIG = 1
        GCL_HICON = -14
        GCL_HICONSM = -34

        user32 = ctypes.windll.user32
        hwnd = window.winfo_id()

        hicon = None
        if icon_path.exists():
            hicon = user32.LoadImageW(
                0,
                str(icon_path),
                IMAGE_ICON,
                0,
                0,
                LR_LOADFROMFILE | LR_DEFAULTSIZE,
            )

        if not hicon:
            small = ctypes.c_void_p()
            large = ctypes.c_void_p()
            # Extract icon embedded in executable (works for Nuitka onefile exe).
            extracted = ctypes.windll.shell32.ExtractIconExW(
                sys.executable,
                0,
                ctypes.byref(large),
                ctypes.byref(small),
                1,
            )
            if extracted > 0:
                hicon = large.value or small.value

        if hicon:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
            user32.SetClassLongPtrW(hwnd, GCL_HICON, hicon)
            user32.SetClassLongPtrW(hwnd, GCL_HICONSM, hicon)
    except Exception:
        pass


def center_window(window: tk.Tk | tk.Toplevel, width: int, height: int) -> None:
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def main() -> None:
    set_windows_app_id()
    root = tk.Tk()
    apply_window_icon(root)
    root.after(0, lambda: apply_window_icon(root))
    root.title("Kalkulator")
    center_window(root, 400, 420)
    root.minsize(320, 420)

    output_value = tk.StringVar(value="")
    history_store = HistoryStore()

    def on_history_click() -> None:
        show_history_table(root, history_store.all())

    top_row = tk.Frame(root)
    top_row.pack(fill="x", padx=20, pady=(16, 0))

    display_host = tk.Frame(top_row)
    display_host.pack(side="left", fill="x", expand=True)

    history_button = tk.Button(
        top_row,
        text="Histori",
        command=on_history_click,
        padx=10,
        pady=2,
    )
    history_button.pack(side="right", padx=(10, 0), pady=20)

    output_label = create_output_display(display_host, output_value.get())

    vfx_canvas = tk.Canvas(root, highlightthickness=0, bd=0, bg=root.cget("bg"))
    fire_vfx = FireVisualEffect(root, vfx_canvas, output_label)
    key_burn_vfx = BurningKeyEffect(root)
    display_fire_vfx = DisplayFlameEffect(root, output_label)

    last_was_equal = False

    def apply_key_logic(key: str) -> None:
        nonlocal last_was_equal
        should_start_new = last_was_equal and key not in {"=", "<"}
        previous = "" if should_start_new else output_value.get()
        next_value = process_input(previous, key)
        output_value.set(next_value)
        output_label.config(text=next_value)
        display_fire_vfx.trigger()

        if (
            key == "="
            and previous
            and previous[-1] not in OPERATORS
            and next_value != "Error"
        ):
            history_store.add(previous, next_value)

        last_was_equal = key == "="

    def on_key_press(key: str, source_button: tk.Widget) -> None:
        key_burn_vfx.trigger(source_button)
        fire_vfx.launch_fire(source_button, on_impact=lambda: apply_key_logic(key))

    create_keypad(root, on_key_press)

    root.mainloop()


if __name__ == "__main__":
    main()
