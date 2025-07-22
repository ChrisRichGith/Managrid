import tkinter as tk
from gui.startscreen import StartScreen
from gui.board import BoardGUI

def start_game(player_name):
    startscreen.pack_forget()
    board_gui = BoardGUI(root, level=1)
    board_gui.pack()

def load_game(filename):
    tk.messagebox.showinfo("Laden", f"Lade Spielstand aus: {filename}")

def exit_game():
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Managrid")
    startscreen = StartScreen(
        root,
        start_callback=start_game,
        load_callback=load_game,
        exit_callback=exit_game,
        img_path="Managrid.jpg"
    )
    startscreen.pack(fill="both", expand=True)
    root.mainloop()