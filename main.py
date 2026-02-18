import tkinter as tk

from fitur.display import create_output_display


def main() -> None:
    root = tk.Tk()
    root.title("Window Kosong")
    root.geometry("400x300")

    output_value = "123"
    create_output_display(root, output_value)

    root.mainloop()


if __name__ == "__main__":
    main()
