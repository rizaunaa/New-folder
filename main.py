import tkinter as tk

from fitur.display import create_output_display
from fitur.history import HistoryStore, show_history_table
from fitur.logikaoperasinalmtk import OPERATORS, process_input
from fitur.tombol import create_keypad


def main() -> None:
    root = tk.Tk()
    root.title("Kalkulator")
    root.geometry("400x420")
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
    last_was_equal = False

    def on_key_press(key: str) -> None:
        nonlocal last_was_equal
        previous = "" if last_was_equal else output_value.get()
        next_value = process_input(previous, key)
        output_value.set(next_value)
        output_label.config(text=next_value)

        if (
            key == "="
            and previous
            and previous[-1] not in OPERATORS
            and next_value != "Error"
        ):
            history_store.add(previous, next_value)

        last_was_equal = key == "="

    create_keypad(root, on_key_press)

    root.mainloop()


if __name__ == "__main__":
    main()
