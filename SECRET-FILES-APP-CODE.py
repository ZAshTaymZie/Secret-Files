import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk


app = ttk.Window(themename="darkly")

app.title("Secret Files")
app.geometry("1100x700")
app.minsize(900, 600)


BG_COLOR = "#000000"
CARD_COLOR = "#272727"
ACCENT_COLOR = "#C4FE76"
TEXT_COLOR = "#FDFDFD"
MUTED_COLOR = "#A0A0A0"


posts = []


def update_post_count():
    post_count.config(text=f"{len(posts)} Secret(s)")


def clear_empty_message():
    if empty_message.winfo_exists():
        empty_message.pack_forget()


def show_empty_message():
    if len(posts) == 0:
        empty_message.pack(pady=80)


def publish_secret():

    codename = user_input.get().strip()
    secret = secret_input.get("1.0", "end").strip()

    if not codename or not secret:
        error_label.config(
            text="Please enter both a codename and a secret."
        )
        return

    error_label.config(text="")

    confirmation = ttk.Toplevel(app)
    confirmation.title("Confirm Publication")
    confirmation.geometry("400x220")
    confirmation.resizable(False, False)
    confirmation.configure(bg=BG_COLOR)
    confirmation.transient(app)
    confirmation.grab_set()

    confirmation.update_idletasks()

    x = app.winfo_x() + (app.winfo_width() // 2) - 200
    y = app.winfo_y() + (app.winfo_height() // 2) - 110

    confirmation.geometry(f"+{x}+{y}")

    tk.Label(
        confirmation,
        text="Publish Secret?",
        font=("Segoe UI", 18, "bold"),
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=(25, 8))

    tk.Label(
        confirmation,
        text="Are you sure you want to publish this secret?",
        font=("Segoe UI", 10),
        fg=MUTED_COLOR,
        bg=BG_COLOR
    ).pack(pady=5)

    button_frame = tk.Frame(
        confirmation,
        bg=BG_COLOR
    )

    button_frame.pack(pady=25)

    tk.Button(
        button_frame,
        text="CANCEL",
        font=("Segoe UI", 9, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        activebackground="#333333",
        activeforeground=TEXT_COLOR,
        relief="flat",
        width=12,
        command=confirmation.destroy
    ).pack(side=LEFT, padx=8)

    tk.Button(
        button_frame,
        text="PUBLISH",
        font=("Segoe UI", 9, "bold"),
        bg=ACCENT_COLOR,
        fg=BG_COLOR,
        activebackground=ACCENT_COLOR,
        activeforeground=BG_COLOR,
        relief="flat",
        width=12,
        command=lambda: complete_publish(
            codename,
            secret,
            confirmation
        )
    ).pack(side=LEFT, padx=8)


def complete_publish(codename, secret, confirmation):

    post = {
        "codename": codename,
        "secret": secret
    }

    posts.append(post)

    create_post_card(post)

    user_input.delete(0, END)
    secret_input.delete("1.0", END)

    update_post_count()
    clear_empty_message()

    confirmation.destroy()


def create_post_card(post):

    card = tk.Frame(
        posts_container,
        bg=CARD_COLOR,
        padx=20,
        pady=18
    )

    card.pack(
        fill=X,
        pady=8,
        padx=5
    )

    top_frame = tk.Frame(
        card,
        bg=CARD_COLOR
    )

    top_frame.pack(fill=X)

    tk.Label(
        top_frame,
        text=f"@{post['codename']}",
        font=("Segoe UI", 13, "bold"),
        fg=ACCENT_COLOR,
        bg=CARD_COLOR
    ).pack(side=LEFT)

    tk.Label(
        top_frame,
        text="● PUBLISHED",
        font=("Segoe UI", 8, "bold"),
        fg=ACCENT_COLOR,
        bg=CARD_COLOR
    ).pack(side=RIGHT)

    tk.Label(
        card,
        text=post["secret"],
        font=("Segoe UI", 11),
        fg=TEXT_COLOR,
        bg=CARD_COLOR,
        wraplength=450,
        justify=LEFT
    ).pack(
        fill=X,
        pady=(15, 15)
    )

    bottom_frame = tk.Frame(
        card,
        bg=CARD_COLOR
    )

    bottom_frame.pack(fill=X)

    tk.Button(
        bottom_frame,
        text="DELETE",
        font=("Segoe UI", 8, "bold"),
        bg="#000000",
        fg=TEXT_COLOR,
        activebackground="#111111",
        activeforeground=ACCENT_COLOR,
        relief="flat",
        width=10,
        command=lambda: delete_post(card, post)
    ).pack(side=RIGHT)


def delete_post(card, post):

    confirmation = ttk.Toplevel(app)

    confirmation.title("Delete Secret")
    confirmation.geometry("380x210")
    confirmation.resizable(False, False)
    confirmation.configure(bg=BG_COLOR)
    confirmation.transient(app)
    confirmation.grab_set()

    tk.Label(
        confirmation,
        text="Delete Secret?",
        font=("Segoe UI", 18, "bold"),
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=(25, 8))

    tk.Label(
        confirmation,
        text="This action cannot be undone.",
        font=("Segoe UI", 10),
        fg=MUTED_COLOR,
        bg=BG_COLOR
    ).pack()

    button_frame = tk.Frame(
        confirmation,
        bg=BG_COLOR
    )

    button_frame.pack(pady=30)

    tk.Button(
        button_frame,
        text="CANCEL",
        font=("Segoe UI", 9, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        activebackground="#333333",
        activeforeground=TEXT_COLOR,
        relief="flat",
        width=12,
        command=confirmation.destroy
    ).pack(side=LEFT, padx=8)

    tk.Button(
        button_frame,
        text="DELETE",
        font=("Segoe UI", 9, "bold"),
        bg=ACCENT_COLOR,
        fg=BG_COLOR,
        activebackground=ACCENT_COLOR,
        activeforeground=BG_COLOR,
        relief="flat",
        width=12,
        command=lambda: complete_delete(
            card,
            post,
            confirmation
        )
    ).pack(side=LEFT, padx=8)


def complete_delete(card, post, confirmation):

    if post in posts:
        posts.remove(post)

    card.destroy()

    update_post_count()
    show_empty_message()

    confirmation.destroy()


main_container = tk.Frame(
    app,
    bg=BG_COLOR
)

main_container.pack(
    fill=BOTH,
    expand=True
)


left_panel = tk.Frame(
    main_container,
    bg=BG_COLOR,
    padx=45,
    pady=35
)

left_panel.pack(
    side=LEFT,
    fill=BOTH,
    expand=True
)


logo_image = Image.open("sf logo.png")
logo_image = logo_image.resize(
    (300, 140),
    Image.Resampling.LANCZOS
)

logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(
    left_panel,
    image=logo_photo,
    bg=BG_COLOR
)

logo_label.pack(
    anchor=W,
    pady=(0, 5)
)


tk.Label(
    left_panel,
    text="Say it. Share it. Stay anonymous.",
    font=("Segoe UI", 11),
    fg=MUTED_COLOR,
    bg=BG_COLOR
).pack(
    anchor=W,
    pady=(0, 35)
)


form_card = tk.Frame(
    left_panel,
    bg=CARD_COLOR,
    padx=25,
    pady=25
)

form_card.pack(
    fill=X
)


tk.Label(
    form_card,
    text="CODENAME",
    font=("Segoe UI", 9, "bold"),
    fg=MUTED_COLOR,
    bg=CARD_COLOR
).pack(anchor=W)


user_input = tk.Entry(
    form_card,
    font=("Segoe UI", 11),
    bg="#000000",
    fg=TEXT_COLOR,
    insertbackground=ACCENT_COLOR,
    relief="flat"
)

user_input.pack(
    fill=X,
    ipady=9,
    pady=(7, 20)
)


tk.Label(
    form_card,
    text="YOUR SECRET",
    font=("Segoe UI", 9, "bold"),
    fg=MUTED_COLOR,
    bg=CARD_COLOR
).pack(anchor=W)


secret_input = tk.Text(
    form_card,
    height=7,
    font=("Segoe UI", 11),
    bg="#000000",
    fg=TEXT_COLOR,
    insertbackground=ACCENT_COLOR,
    relief="flat",
    padx=12,
    pady=12,
    wrap="word"
)

secret_input.pack(
    fill=X,
    pady=(7, 20)
)


error_label = tk.Label(
    form_card,
    text="",
    font=("Segoe UI", 9),
    fg="#FF7070",
    bg=CARD_COLOR
)

error_label.pack(anchor=W)


publish_button = tk.Button(
    form_card,
    text="PUBLISH SECRET",
    font=("Segoe UI", 10, "bold"),
    bg=ACCENT_COLOR,
    fg=BG_COLOR,
    activebackground=ACCENT_COLOR,
    activeforeground=BG_COLOR,
    relief="flat",
    cursor="hand2",
    width=25,
    command=publish_secret
)

publish_button.pack(
    pady=(15, 5),
    ipady=8
)


tk.Label(
    form_card,
    text="Your identity stays hidden behind your codename.",
    font=("Segoe UI", 8),
    fg=MUTED_COLOR,
    bg=CARD_COLOR
).pack(
    pady=(8, 0)
)


right_panel = tk.Frame(
    main_container,
    bg=BG_COLOR,
    padx=25,
    pady=30
)

right_panel.pack(
    side=RIGHT,
    fill=BOTH,
    expand=True
)


header_frame = tk.Frame(
    right_panel,
    bg=BG_COLOR
)

header_frame.pack(fill=X)


tk.Label(
    header_frame,
    text="PUBLIC SECRETS",
    font=("Segoe UI", 22, "bold"),
    fg=TEXT_COLOR,
    bg=BG_COLOR
).pack(side=LEFT)


post_count = tk.Label(
    header_frame,
    text="0 Secret(s)",
    font=("Segoe UI", 9, "bold"),
    fg=ACCENT_COLOR,
    bg=BG_COLOR
)

post_count.pack(side=RIGHT)


tk.Frame(
    right_panel,
    height=2,
    bg=CARD_COLOR
).pack(
    fill=X,
    pady=15
)


canvas = tk.Canvas(
    right_panel,
    bg=BG_COLOR,
    highlightthickness=0
)


scrollbar = tk.Scrollbar(
    right_panel,
    orient=VERTICAL,
    command=canvas.yview,
    bg=CARD_COLOR,
    troughcolor=BG_COLOR,
    activebackground=ACCENT_COLOR
)


posts_container = tk.Frame(
    canvas,
    bg=BG_COLOR
)


posts_container.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)


canvas_window = canvas.create_window(
    (0, 0),
    window=posts_container,
    anchor="nw"
)


canvas.configure(
    yscrollcommand=scrollbar.set
)


def resize_posts(event):
    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


canvas.bind(
    "<Configure>",
    resize_posts
)


canvas.pack(
    side=LEFT,
    fill=BOTH,
    expand=True
)


scrollbar.pack(
    side=RIGHT,
    fill=Y
)


empty_message = tk.Label(
    posts_container,
    text="NO SECRETS YET\n\nBe the first to share something.",
    font=("Segoe UI", 11),
    fg=MUTED_COLOR,
    bg=BG_COLOR,
    justify=CENTER
)

empty_message.pack(
    pady=80
)


app.mainloop()