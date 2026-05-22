import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


ASCII_CHARS = "@%#*+=-:. "


def resize_image(image, new_width=120):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.55)

    return image.resize((new_width, new_height))


def grayscale(image):
    return image.convert("L")


def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""

    for pixel in pixels:
        index = pixel * (len(ASCII_CHARS) - 1) // 255
        ascii_str += ASCII_CHARS[index]

    return ascii_str


def convert_to_ascii():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Images", "*.png *.jpg *.jpeg *.bmp")
        ]
    )

    if not file_path:
        return

    try:
        image = Image.open(file_path)

        # Preview image
        preview = image.copy()
        preview.thumbnail((300, 300))

        photo = ImageTk.PhotoImage(preview)

        image_preview.config(image=photo)
        image_preview.image = photo

        # ASCII conversion
        image = resize_image(image)
        image = grayscale(image)

        ascii_str = pixels_to_ascii(image)

        pixel_count = len(ascii_str)
        ascii_image = "\n".join(
            ascii_str[i:i + image.width]
            for i in range(0, pixel_count, image.width)
        )

        ascii_text.delete("1.0", tk.END)
        ascii_text.insert(tk.END, ascii_image)

        with open("ascii_art.txt", "w") as f:
            f.write(ascii_image)

        result_label.config(
            text="ASCII art generated successfully ✅",
            fg="#00cc66"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def save_ascii():
    content = ascii_text.get("1.0", tk.END)

    if not content.strip():
        messagebox.showwarning("Warning", "No ASCII art to save.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt")]
    )

    if save_path:
        with open(save_path, "w") as f:
            f.write(content)

        messagebox.showinfo("Saved", "ASCII art saved successfully.")


root = tk.Tk()
root.title("ASCII Art Generator")
root.geometry("1500x900")
root.configure(bg="#08111f")

main_frame = tk.Frame(root, bg="#08111f")
main_frame.pack(fill="both", expand=True, padx=30, pady=30)

left_frame = tk.Frame(main_frame, bg="#08111f", width=420)
left_frame.pack(side="left", fill="y", padx=(0, 20))

right_frame = tk.Frame(main_frame, bg="#08111f")
right_frame.pack(side="right", fill="both", expand=True)


title_label = tk.Label(
    left_frame,
    text="ASCII ART\nGENERATOR",
    font=("Arial", 34, "bold"),
    fg="#ffffff",
    bg="#08111f",
    justify="left"
)
title_label.pack(anchor="w", pady=(10, 15))

subtitle_label = tk.Label(
    left_frame,
    text="Convert images into ASCII art with Python",
    font=("Arial", 15),
    fg="#cccccc",
    bg="#08111f"
)
subtitle_label.pack(anchor="w", pady=(0, 30))

convert_button = tk.Button(
    left_frame,
    text="Select Image",
    font=("Arial", 18, "bold"),
    bg="#00bfff",
    fg="#08111f",
    activebackground="#0099cc",
    activeforeground="#ffffff",
    relief="flat",
    command=convert_to_ascii
)
convert_button.pack(anchor="w", pady=15, ipadx=45, ipady=14)

save_button = tk.Button(
    left_frame,
    text="Save ASCII Art",
    font=("Arial", 16, "bold"),
    bg="#111827",
    fg="#ffffff",
    activebackground="#00bfff",
    activeforeground="#08111f",
    relief="solid",
    borderwidth=1,
    command=save_ascii
)
save_button.pack(anchor="w", pady=10, ipadx=35, ipady=12)

result_label = tk.Label(
    left_frame,
    text="Select an image to begin",
    font=("Arial", 15, "bold"),
    fg="#ffffff",
    bg="#08111f"
)
result_label.pack(anchor="w", pady=25)

preview_title = tk.Label(
    left_frame,
    text="🖼 IMAGE PREVIEW",
    font=("Arial", 18, "bold"),
    fg="#00bfff",
    bg="#08111f"
)
preview_title.pack(anchor="w", pady=(10, 15))

preview_frame = tk.Frame(
    left_frame,
    width=320,
    height=320,
    bg="#111827",
    highlightbackground="#00bfff",
    highlightthickness=2
)
preview_frame.pack(anchor="w")
preview_frame.pack_propagate(False)

image_preview = tk.Label(
    preview_frame,
    bg="#111827"
)
image_preview.pack(expand=True)

footer_label = tk.Label(
    left_frame,
    text="🐍 Python Mini Automation",
    font=("Arial", 14, "bold"),
    fg="#00bfff",
    bg="#08111f"
)
footer_label.pack(side="bottom", anchor="w", pady=20)

ascii_title = tk.Label(
    right_frame,
    text="💻 ASCII OUTPUT",
    font=("Arial", 24, "bold"),
    fg="#00bfff",
    bg="#08111f"
)
ascii_title.pack(anchor="w", pady=(10, 20))

text_frame = tk.Frame(
    right_frame,
    bg="#111827",
    highlightbackground="#00bfff",
    highlightthickness=2
)
text_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

ascii_text = tk.Text(
    text_frame,
    wrap="none",
    bg="#111827",
    fg="#00ff99",
    insertbackground="#ffffff",
    font=("Courier New", 6),
    yscrollcommand=scrollbar.set,
    relief="flat"
)

ascii_text.pack(fill="both", expand=True)

scrollbar.config(command=ascii_text.yview)

root.mainloop()