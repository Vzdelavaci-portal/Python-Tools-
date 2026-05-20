import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter


OUTPUT_FILE = "business_card.png"


def load_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()


def create_business_card_image():
    name = name_entry.get().strip()
    job = job_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    website = website_entry.get().strip()

    if not name:
        messagebox.showwarning("Warning", "Please enter your name.")
        return None

    width, height = 1000, 600

    image = Image.new("RGBA", (width, height), "#0b1220")
    draw = ImageDraw.Draw(image)

    title_font = load_font(58, bold=True)
    job_font = load_font(34)
    text_font = load_font(28, bold=True)
    normal_font = load_font(28)
    logo_font = load_font(34, bold=True)
    slogan_font = load_font(20)

    cyan = "#00bfff"
    dark = "#0b1220"
    blue = "#0077cc"
    white = "#f7f7f7"

    # Rounded card mask
    card_mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(card_mask)
    mask_draw.rounded_rectangle(
        (15, 15, width - 15, height - 15),
        radius=32,
        fill=255
    )

    # Card base
    card_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_layer)
    card_draw.rounded_rectangle(
        (15, 15, width - 15, height - 15),
        radius=32,
        fill=dark,
        outline="#dddddd",
        width=2
    )

    # White left part clipped into rounded card
    white_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    white_draw = ImageDraw.Draw(white_layer)

    white_draw.polygon(
        [
            (15, 15),
            (645, 15),
            (520, 300),
            (720, height - 15),
            (15, height - 15),
        ],
        fill=white
    )

    white_layer.putalpha(card_mask)
    card_layer.alpha_composite(white_layer)

    # Blue accent shape
    accent_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    accent_draw = ImageDraw.Draw(accent_layer)

    accent_draw.polygon(
        [
            (620, 80),
            (700, 80),
            (520, 300),
            (720, 520),
            (640, 520),
            (460, 300),
        ],
        fill=cyan
    )

    accent_layer = accent_layer.filter(ImageFilter.GaussianBlur(0.4))
    card_layer.alpha_composite(accent_layer)

    image.alpha_composite(card_layer)
    draw = ImageDraw.Draw(image)

    # Name accent line
    draw.rounded_rectangle(
        (70, 120, 82, 250),
        radius=6,
        fill=blue
    )

    # Name and job
    draw.text((110, 135), name, fill=dark, font=title_font)
    draw.text((110, 210), job, fill=blue, font=job_font)

    # Divider
    draw.line((70, 290, 430, 290), fill=cyan, width=4)

    # Contact rows
    y = 350
    rows = [
        ("✉", "Email:", email),
        ("☎", "Phone:", phone),
        ("🌐", "Web:", website),
    ]

    for icon, label, value in rows:
        draw.ellipse((70, y - 10, 120, y + 40), fill=blue)

        try:
            icon_font = ImageFont.truetype("seguisym.ttf", 24)
        except:
            icon_font = normal_font

        draw.text((84, y - 2), icon, fill="white", font=icon_font)
        draw.text((145, y), label, fill=dark, font=text_font)
        draw.text((245, y), value, fill=dark, font=normal_font)

        y += 80

    # Logo placeholder
    draw.regular_polygon(
        (820, 260, 60),
        n_sides=6,
        outline=cyan,
        width=6
    )

    draw.text((755, 340), "YOUR LOGO", fill="white", font=logo_font)
    draw.text((770, 382), "SLOGAN HERE", fill="#aaaaaa", font=slogan_font)

    return image.convert("RGB")


def generate_business_card():
    image = create_business_card_image()

    if image is None:
        return

    image.save(OUTPUT_FILE)

    preview = image.resize((700, 420))
    photo = ImageTk.PhotoImage(preview)

    card_preview.config(image=photo)
    card_preview.image = photo

    result_label.config(
        text="Business card generated successfully! ✅",
        fg="#00cc66"
    )


def print_business_card():
    if not os.path.exists(OUTPUT_FILE):
        messagebox.showwarning("Warning", "Please generate the business card first.")
        return

    try:
        os.startfile(OUTPUT_FILE, "print")
    except Exception as e:
        messagebox.showerror("Print Error", str(e))


def clear_all():
    for entry in [name_entry, job_entry, email_entry, phone_entry, website_entry]:
        entry.delete(0, tk.END)

    card_preview.config(image="")
    card_preview.image = None

    result_label.config(
        text="Fill in the details and generate",
        fg="#ffffff"
    )


root = tk.Tk()
root.title("Business Card Generator")
root.geometry("1400x850")
root.resizable(False, False)
root.configure(bg="#08111f")


main_frame = tk.Frame(root, bg="#08111f")
main_frame.pack(fill="both", expand=True, padx=40, pady=35)

left_frame = tk.Frame(main_frame, bg="#08111f", width=520)
left_frame.pack(side="left", fill="y", padx=(0, 35))

divider = tk.Frame(main_frame, bg="#00bfff", width=2)
divider.pack(side="left", fill="y", padx=10)

right_frame = tk.Frame(main_frame, bg="#08111f")
right_frame.pack(side="right", fill="both", expand=True, padx=(35, 0))


title_label = tk.Label(
    left_frame,
    text="BUSINESS CARD\nGENERATOR",
    font=("Arial", 32, "bold"),
    fg="#ffffff",
    bg="#08111f",
    justify="left"
)
title_label.pack(anchor="w", pady=(20, 15))

subtitle_label = tk.Label(
    left_frame,
    text="Create your own professional business card with Python",
    font=("Arial", 15),
    fg="#cccccc",
    bg="#08111f",
    justify="left"
)
subtitle_label.pack(anchor="w", pady=(0, 30))


def create_input(label_text):
    label = tk.Label(
        left_frame,
        text=label_text,
        font=("Arial", 14, "bold"),
        fg="#00bfff",
        bg="#08111f"
    )
    label.pack(anchor="w", pady=(10, 4))

    entry = tk.Entry(
        left_frame,
        width=34,
        font=("Arial", 18),
        bg="#111827",
        fg="#ffffff",
        insertbackground="#ffffff",
        relief="flat"
    )
    entry.pack(anchor="w", ipady=10)

    return entry


name_entry = create_input("Name")
job_entry = create_input("Job Title")
email_entry = create_input("Email")
phone_entry = create_input("Phone")
website_entry = create_input("Website")


generate_button = tk.Button(
    left_frame,
    text="Generate Card",
    font=("Arial", 18, "bold"),
    bg="#00bfff",
    fg="#08111f",
    activebackground="#0099cc",
    activeforeground="#ffffff",
    relief="flat",
    command=generate_business_card
)
generate_button.pack(anchor="w", pady=30, ipadx=60, ipady=14)

result_label = tk.Label(
    left_frame,
    text="Fill in the details and generate",
    font=("Arial", 15, "bold"),
    fg="#ffffff",
    bg="#08111f"
)
result_label.pack(anchor="w", pady=10)

footer_label = tk.Label(
    left_frame,
    text="🐍 Python Mini Automation",
    font=("Arial", 15, "bold"),
    fg="#00bfff",
    bg="#08111f"
)
footer_label.pack(side="bottom", anchor="w", pady=25)


preview_title = tk.Label(
    right_frame,
    text="👁 PREVIEW",
    font=("Arial", 22, "bold"),
    fg="#00bfff",
    bg="#08111f"
)
preview_title.pack(pady=(40, 25))

preview_frame = tk.Frame(
    right_frame,
    width=740,
    height=460,
    bg="#111827",
    highlightbackground="#00bfff",
    highlightthickness=2
)
preview_frame.pack()
preview_frame.pack_propagate(False)

card_preview = tk.Label(
    preview_frame,
    bg="#111827"
)
card_preview.pack(expand=True)

actions_label = tk.Label(
    right_frame,
    text="⚙ ACTIONS",
    font=("Arial", 20, "bold"),
    fg="#00bfff",
    bg="#08111f"
)
actions_label.pack(pady=(35, 20))

buttons_frame = tk.Frame(right_frame, bg="#08111f")
buttons_frame.pack()

print_button = tk.Button(
    buttons_frame,
    text="Print Card",
    font=("Arial", 15, "bold"),
    bg="#111827",
    fg="#ffffff",
    activebackground="#00bfff",
    activeforeground="#08111f",
    relief="solid",
    borderwidth=1,
    command=print_business_card
)
print_button.grid(row=0, column=0, padx=15, ipadx=45, ipady=12)

clear_button = tk.Button(
    buttons_frame,
    text="Clear All",
    font=("Arial", 15, "bold"),
    bg="#111827",
    fg="#ffffff",
    activebackground="#ff4d4d",
    activeforeground="#ffffff",
    relief="solid",
    borderwidth=1,
    command=clear_all
)
clear_button.grid(row=0, column=1, padx=15, ipadx=45, ipady=12)

note_label = tk.Label(
    right_frame,
    text="Note: The business card is saved as business_card.png in the current directory.",
    font=("Arial", 13),
    fg="#cccccc",
    bg="#08111f"
)
note_label.pack(pady=35)

root.mainloop()