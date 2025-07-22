import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

class StartScreen(tk.Frame):
    def __init__(self, master, start_callback, load_callback, exit_callback, img_path="Managrid.jpg"):
        super().__init__(master)
        self.master = master
        self.start_callback = start_callback
        self.load_callback = load_callback
        self.exit_callback = exit_callback

        # Lade das Hintergrundbild
        if not os.path.exists(img_path):
            self.bg_image = None
            print("Warnung: Bild '{}' nicht gefunden.".format(img_path))
        else:
            pil_img = Image.open(img_path)
            pil_img = pil_img.resize((800, 600), Image.ANTIALIAS)
            self.bg_image = ImageTk.PhotoImage(pil_img)

        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Overlay-Elemente
        self.name_var = tk.StringVar()
        self.entry = tk.Entry(self.canvas, textvariable=self.name_var, font=("Arial", 18), width=18)
        self.entry_window = self.canvas.create_window(400, 220, window=self.entry)

        self.canvas.create_text(400, 180, text="Spielername:", font=("Arial", 18, "bold"), fill="#FFF", anchor="center")

        start_btn = tk.Button(self.canvas, text="Spiel starten", command=self.on_start, font=("Arial", 16))
        self.canvas.create_window(400, 290, window=start_btn)

        load_btn = tk.Button(self.canvas, text="Spielstand laden", command=self.on_load, font=("Arial", 16))
        self.canvas.create_window(400, 340, window=load_btn)

        exit_btn = tk.Button(self.canvas, text="Beenden", command=self.on_exit, font=("Arial", 16))
        self.canvas.create_window(400, 390, window=exit_btn)

    def on_start(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Hinweis", "Bitte gib deinen Spielernamen ein.")
            return
        self.start_callback(name)

    def on_load(self):
        filename = filedialog.askopenfilename(title="Spielstand laden", filetypes=[("Managrid Save", "*.sav"), ("Alle Dateien", "*.*")])
        if filename:
            self.load_callback(filename)

    def on_exit(self):
        self.exit_callback()