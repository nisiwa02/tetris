# streamlit_tetris.py
import streamlit as st
import numpy as np
import random

GRID_WIDTH, GRID_HEIGHT = 10, 20
COLORS = {
    0: (240, 240, 240),   # 空白
    1: (0, 255, 255),     # ピースの色
}

# テトリスのピース定義
SHAPES = [
    np.array([[1, 1, 1, 1]]),                     # I
    np.array([[1, 0, 0], [1, 1, 1]]),             # J
    np.array([[0, 0, 1], [1, 1, 1]]),             # L
    np.array([[1, 1], [1, 1]]),                   # O
    np.array([[0, 1, 1], [1, 1, 0]]),             # S
    np.array([[1, 1, 0], [0, 1, 1]]),             # Z
    np.array([[0, 1, 0], [1, 1, 1]])              # T
]

# テトリスのグリッドとピース管理
class Tetris:
    def __init__(self):
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.current_piece = self.get_new_piece()
        self.current_x, self.current_y = GRID_WIDTH // 2, 0

    def get_new_piece(self):
        return random.choice(SHAPES)

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

# 描画関数
def draw_grid(grid):
    canvas = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3), dtype=int)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = COLORS[cell]
            canvas[y, x] = color
    return canvas

# Streamlitアプリケーション
st.title("Streamlit Tetris")

tetris = Tetris()

# コントロールボタン
if st.button("⬇ Move Down"):
    tetris.move_down()
if st.button("⬅ Move Left"):
    tetris.move_left()
if st.button("➡ Move Right"):
    tetris.move_right()

# グリッドの描画
grid_with_piece = tetris.get_grid_with_piece()
st.image(draw_grid(grid_with_piece), caption="Tetris", use_column_width=True)

