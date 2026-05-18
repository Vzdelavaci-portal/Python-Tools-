import tkinter as tk
from tkinter import messagebox
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageTk


def generate_barcode():
    text = barcode_entry.get().strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter text or numbers.")
        return

    filename = "barcode"

    try:
        barcode = Code128(text, writer=ImageWriter())
        saved_file = barcode.save(filename)

        # Load generated barcode image
        image = Image.open(saved_file)

        # Resize image for GUI preview
        image = image.resize((420, 180))

        photo = ImageTk.PhotoImage(image)

        barcode_preview.config(image=photo)
        barcode_preview.image = photo

        result_label.config(
            text="Barcode generated successfully ✅",
            fg="#00cc66"
        )

    except Exception as e:
        result_label.config(
            text="Error while generating barcode ❌",
            fg="#ff4d4d"
        )
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Barcode Generator")
root.geometry("540x960")
root.resizable(False, False)
root.configure(bg="#121212")

title_label = tk.Label(
    root,
    text="BARCODE\nGENERATOR",
    font=("Arial", 36, "bold"),
    fg="#ffffff",
    bg="#121212",
    justify="center"
)
title_label.pack(pady=50)

subtitle_label = tk.Label(
    root,
    text="Create a barcode from text or numbers",
    font=("Arial", 16),
    fg="#bbbbbb",
    bg="#121212"
)
subtitle_label.pack(pady=10)

barcode_entry = tk.Entry(
    root,
    width=22,
    font=("Arial", 24),
    justify="center",
    bg="#1f1f1f",
    fg="#ffffff",
    insertbackground="#ffffff",
    relief="flat"
)
barcode_entry.pack(pady=35, ipady=15)

generate_button = tk.Button(
    root,
    text="Generate Barcode",
    font=("Arial", 20, "bold"),
    bg="#00ccff",
    fg="#121212",
    activebackground="#0099cc",
    activeforeground="#ffffff",
    relief="flat",
    command=generate_barcode
)
generate_button.pack(pady=20, ipadx=25, ipady=15)

result_label = tk.Label(
    root,
    text="Enter text and click generate",
    font=("Arial", 18, "bold"),
    fg="#ffffff",
    bg="#121212"
)
result_label.pack(pady=25)

# Barcode preview area
preview_frame = tk.Frame(
    root,
    width=440,
    height=220,
    bg="#1f1f1f"
)
preview_frame.pack(pady=20)
preview_frame.pack_propagate(False)

barcode_preview = tk.Label(
    preview_frame,
    bg="#1f1f1f"
)
barcode_preview.pack(expand=True)

footer_label = tk.Label(
    root,
    text="Python Mini Automation",
    font=("Arial", 14, "bold"),
    fg="#00ccff",
    bg="#121212"
)
footer_label.pack(side="bottom", pady=40)

root.mainloop()