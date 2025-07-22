import tkinter as tk
import random

CELL_SIZE = 40
GRID_ROWS = 6
GRID_COLS = 6
DOT_RADIUS = 5
LINE_WIDTH = 3

class BoardGUI(tk.Frame):
    def __init__(self, master, rows=GRID_ROWS, cols=GRID_COLS, level=1):
        super().__init__(master)
        self.master = master
        self.rows = rows
        self.cols = cols
        self.level = level
        self.cell_size = CELL_SIZE
        self.dot_radius = DOT_RADIUS
        self.line_width = LINE_WIDTH
        self.canvas_width = self.cols * self.cell_size + self.cell_size
        self.canvas_height = self.rows * self.cell_size + self.cell_size

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.confirm_button = tk.Button(self, text="Zug bestätigen", command=self.confirm_turn)
        self.confirm_button.pack(pady=10)

        self.status_label = tk.Label(self, text="Spieler ist am Zug")
        self.status_label.pack()

        self.horizontal_lines = [[False for _ in range(self.cols)] for _ in range(self.rows + 1)]
        self.vertical_lines = [[False for _ in range(self.cols + 1)] for _ in range(self.rows)]
        self.pending_horizontal = [[False for _ in range(self.cols)] for _ in range(self.rows + 1)]
        self.pending_vertical = [[False for _ in range(self.cols + 1)] for _ in range(self.rows)]
        self.boxes = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        self.computer_mana = 0
        self.computer_mana_needed = 5
        self.computer_can_draw_lines = (self.level >= 3)

        self.randomize_board()

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(self.rows + 1):
            for c in range(self.cols + 1):
                x = c * self.cell_size
                y = r * self.cell_size
                self.canvas.create_oval(
                    x - self.dot_radius, y - self.dot_radius,
                    x + self.dot_radius, y + self.dot_radius,
                    fill='black'
                )
        for r in range(self.rows + 1):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = (c + 1) * self.cell_size
                y2 = r * self.cell_size
                color = "blue" if self.horizontal_lines[r][c] else "red" if self.pending_horizontal[r][c] else "lightgray"
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=self.line_width)
        for r in range(self.rows):
            for c in range(self.cols + 1):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = c * self.cell_size
                y2 = (r + 1) * self.cell_size
                color = "blue" if self.vertical_lines[r][c] else "red" if self.pending_vertical[r][c] else "lightgray"
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=self.line_width)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.boxes[r][c]:
                    x1 = c * self.cell_size + self.cell_size // 4
                    y1 = r * self.cell_size + self.cell_size // 4
                    x2 = (c + 1) * self.cell_size - self.cell_size // 4
                    y2 = (r + 1) * self.cell_size - self.cell_size // 4
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.boxes[r][c], outline='')

    def on_left_click(self, event):
        if self.status_label.cget("text") != "Spieler ist am Zug":
            return
        line = self.get_clicked_line(event.x, event.y)
        if line:
            kind, r, c = line
            if kind == 'h' and not self.horizontal_lines[r][c] and not self.pending_horizontal[r][c]:
                self.pending_horizontal[r][c] = True
                self.draw_board()
            elif kind == 'v' and not self.vertical_lines[r][c] and not self.pending_vertical[r][c]:
                self.pending_vertical[r][c] = True
                self.draw_board()

    def on_right_click(self, event):
        if self.status_label.cget("text") != "Spieler ist am Zug":
            return
        line = self.get_clicked_line(event.x, event.y)
        if line:
            kind, r, c = line
            if kind == 'h' and self.pending_horizontal[r][c]:
                self.pending_horizontal[r][c] = False
                self.draw_board()
            elif kind == 'v' and self.pending_vertical[r][c]:
                self.pending_vertical[r][c] = False
                self.draw_board()

    def get_clicked_line(self, x, y):
        for r in range(self.rows + 1):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size - self.line_width
                x2 = (c + 1) * self.cell_size
                y2 = r * self.cell_size + self.line_width
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return ('h', r, c)
        for r in range(self.rows):
            for c in range(self.cols + 1):
                x1 = c * self.cell_size - self.line_width
                y1 = r * self.cell_size
                x2 = c * self.cell_size + self.line_width
                y2 = (r + 1) * self.cell_size
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return ('v', r, c)
        return None

    def confirm_turn(self):
        any_line = False
        for r in range(self.rows + 1):
            for c in range(self.cols):
                if self.pending_horizontal[r][c]:
                    self.horizontal_lines[r][c] = True
                    self.pending_horizontal[r][c] = False
                    any_line = True
        for r in range(self.rows):
            for c in range(self.cols + 1):
                if self.pending_vertical[r][c]:
                    self.vertical_lines[r][c] = True
                    self.pending_vertical[r][c] = False
                    any_line = True
        if not any_line:
            self.status_label.config(text="Kein Zug ausgeführt!")
            return
        closed = self.check_boxes(player=True)
        self.draw_board()
        self.status_label.config(text="Computer ist am Zug...")
        self.after(700, self.computer_turn)

    def check_boxes(self, player=False):
        closed = 0
        color = "skyblue" if player else "lightgreen"
        for r in range(self.rows):
            for c in range(self.cols):
                if (self.horizontal_lines[r][c] and
                    self.horizontal_lines[r+1][c] and
                    self.vertical_lines[r][c] and
                    self.vertical_lines[r][c+1]):
                    if not self.boxes[r][c]:
                        self.boxes[r][c] = color
                        closed += 1
        return closed

    def computer_turn(self):
        self.computer_mana += 1

        if self.computer_can_draw_lines:
            possible_h = [(r, c) for r in range(self.rows + 1) for c in range(self.cols) if not self.horizontal_lines[r][c]]
            possible_v = [(r, c) for r in range(self.rows) for c in range(self.cols + 1) if not self.vertical_lines[r][c]]
        else:
            possible_h = []
            possible_v = []

        if self.computer_mana >= self.computer_mana_needed:
            if random.random() < 0.5:
                deleted = self.remove_player_box()
                if deleted:
                    self.status_label.config(text="Computer nutzt Fähigkeit!")
                    self.computer_mana = 0
                    self.draw_board()
                    self.after(1000, self.end_computer_turn)
                    return

        if self.computer_can_draw_lines:
            if possible_h and (not possible_v or random.random() < 0.5):
                r, c = random.choice(possible_h)
                self.horizontal_lines[r][c] = True
            elif possible_v:
                r, c = random.choice(possible_v)
                self.vertical_lines[r][c] = True
            self.check_boxes(player=False)
            self.draw_board()

        self.after(500, self.end_computer_turn)

    def end_computer_turn(self):
        self.status_label.config(text="Spieler ist am Zug")

    def remove_player_box(self):
        player_boxes = [(r, c) for r in range(self.rows) for c in range(self.cols) if self.boxes[r][c] == "skyblue"]
        if player_boxes:
            r, c = random.choice(player_boxes)
            self.boxes[r][c] = None
            lines = [
                ('h', r, c),
                ('h', r+1, c),
                ('v', r, c),
                ('v', r, c+1),
            ]
            kind, ri, ci = random.choice(lines)
            if kind == 'h':
                self.horizontal_lines[ri][ci] = False
            else:
                self.vertical_lines[ri][ci] = False
            return True
        return False

    def randomize_board(self):
        self.horizontal_lines = [[False for _ in range(self.cols)] for _ in range(self.rows + 1)]
        self.vertical_lines = [[False for _ in range(self.cols + 1)] for _ in range(self.rows)]
        self.pending_horizontal = [[False for _ in range(self.cols)] for _ in range(self.rows + 1)]
        self.pending_vertical = [[False for _ in range(self.cols + 1)] for _ in range(self.rows)]
        self.boxes = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.computer_mana = 0
        self.computer_can_draw_lines = (self.level >= 3)
        self.draw_board()