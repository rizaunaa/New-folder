import tkinter as tk

from fitur.display import create_output_display
from fitur.logikaoperasinalmtk import process_input
from fitur.tombol import create_keypad


def main() -> None:
    root = tk.Tk()
    root.title("Window Kosong")
    root.geometry("400x420")

    output_value = tk.StringVar(value="")
    output_label = create_output_display(root, output_value.get())
    last_was_equal = False

    def on_key_press(key: str) -> None:
        nonlocal last_was_equal
        current = "" if last_was_equal else output_value.get()
        output_value.set(process_input(current, key))
        output_label.config(text=output_value.get())
        last_was_equal = key == "="

    create_keypad(root, on_key_press)

    root.mainloop()


if __name__ == "__main__":
    main()
