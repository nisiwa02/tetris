# tetris_app.py
import flet as ft
import numpy as np
import random

GRID_WIDTH, GRID_HEIGHT = 10, 20
CELL_SIZE = 25
COLORS = {
    0: ft.colors.WHITE,
    1: ft.colors.CYAN,
    2: ft.colors.ORANGE,
    3: ft.colors.BLUE,
    4: ft.colors.YELLOW,
    5: ft.colors.GREEN,
    6: ft.colors.RED,
    7: ft.colors.PURPLE,
}

SHAPES = [
    np.array([[1, 1, 1, 1]]),                     # I
    np.array([[1, 0, 0], [1, 1, 1]]),             # J
    np.array([[0, 0, 1], [1, 1, 1]]),             # L
    np.array([[1, 1], [1, 1]]),                   # O
    np.array([[0, 1, 1], [1, 1, 0]]),             # S
    np.array([[1, 1, 0], [0, 1, 1]]),             # Z
    np.array([[0, 1, 0], [1, 1, 1]])              # T
]

class Tetris:
    def __init__(self):
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.current_piece = self.get_new_piece()
        self.current_x, self.current_y = GRID_WIDTH // 2, 0

    def get_new_piece(self):
        return random.choice(SHAPES)

    def rotate_piece(self):
        self.current_piece = np.rot90(self.current_piece)

    def move_down(self):
        self.current_y += 1
        if self.check_collision():
            self.current_y -= 1
            self.freeze_piece()

    def move_left(self):
        self.current_x -= 1
        if self.check_collision():
            self.current_x += 1

    def move_right(self):
        self.current_x += 1
        if self.check_collision():
            self.current_x -= 1

    def check_collision(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell and (
                    x + self.current_x < 0 or
                    x + self.current_x >= GRID_WIDTH or
                    y + self.current_y >= GRID_HEIGHT or
                    self.grid[y + self.current_y, x + self.current_x]
                ):
                    return True
        return False

    def freeze_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.current_y, x + self.current_x] = 1
        self.current_piece = self.get_new_piece()
        self.current_x, self.current_y = GRID_WIDTH // 2, 0

    def get_grid_with_piece(self):
        grid = self.grid.copy()
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    grid[y + self.current_y, x + self.current_x] = 1
        return grid

def main(page: ft.Page):
    tetris = Tetris()

    def draw_grid():
        page.controls.clear()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = COLORS[tetris.get_grid_with_piece()[y, x]]
                page.add(ft.Container(width=CELL_SIZE, height=CELL_SIZE, bgcolor=color, border=ft.border.all(1)))
        page.update()

    def on_key(e: ft.KeyboardEvent):
        if e.key == "ArrowLeft":
            tetris.move_left()
        elif e.key == "ArrowRight":
            tetris.move_right()
        elif e.key == "ArrowDown":
            tetris.move_down()
        elif e.key == "Space":
            tetris.rotate_piece()
        draw_grid()

    page.title = "Flet Tetris"
    page.on_key_down = on_key
    draw_grid()

ft.app(target=main)
