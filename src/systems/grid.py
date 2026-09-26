"""
Lawn grid management system.
Handles cell coordinates, plant placement validation, shovel digging, and grid overlays.
"""

from typing import TYPE_CHECKING
import pygame
from config import (
    CELL_HEIGHT,
    CELL_WIDTH,
    COLOR_HIGHLIGHT_INVALID,
    COLOR_HIGHLIGHT_VALID,
    GRID_COLS,
    GRID_ROWS,
    GRID_START_X,
    GRID_START_Y,
)

if TYPE_CHECKING:
    from entities.plant import Plant


class LawnGrid:
    def __init__(self, active_rows: list[int] | None = None):
        self.rows = GRID_ROWS
        self.cols = GRID_COLS
        self.active_rows = active_rows if active_rows is not None else list(range(GRID_ROWS))
        # 2D matrix of plants [row][col]
        self.cells: list[list[Plant | None]] = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def get_cell_coords(self, row: int, col: int) -> tuple[int, int]:
        """Returns top-left pixel (x, y) for a cell."""
        x = GRID_START_X + col * CELL_WIDTH
        y = GRID_START_Y + row * CELL_HEIGHT
        return x, y

    def get_cell_center(self, row: int, col: int) -> tuple[int, int]:
        """Returns center pixel (x, y) for a cell."""
        x, y = self.get_cell_coords(row, col)
        return x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2

    def mouse_to_cell(self, mouse_x: int, mouse_y: int) -> tuple[int, int] | None:
        """Converts mouse screen coordinates to (row, col) or None if outside lawn."""
        rel_x = mouse_x - GRID_START_X
        rel_y = mouse_y - GRID_START_Y

        if rel_x < 0 or rel_y < 0:
            return None

        col = rel_x // CELL_WIDTH
        row = rel_y // CELL_HEIGHT

        if 0 <= row < self.rows and 0 <= col < self.cols:
            if row in self.active_rows:
                return int(row), int(col)

        return None

    def is_cell_empty(self, row: int, col: int) -> bool:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            plant = self.cells[row][col]
            return plant is None or not plant.is_alive
        return False

    def can_place_plant(self, row: int, col: int) -> bool:
        if row not in self.active_rows:
            return False
        return self.is_cell_empty(row, col)

    def place_plant(self, plant: "Plant") -> bool:
        if self.can_place_plant(plant.row, plant.col):
            self.cells[plant.row][plant.col] = plant
            return True
        return False

    def remove_plant(self, row: int, col: int) -> "Plant | None":
        if 0 <= row < self.rows and 0 <= col < self.cols:
            plant = self.cells[row][col]
            self.cells[row][col] = None
            if plant:
                plant.is_alive = False
            return plant
        return None

    def get_plant(self, row: int, col: int) -> "Plant | None":
        if 0 <= row < self.rows and 0 <= col < self.cols:
            plant = self.cells[row][col]
            if plant and plant.is_alive:
                return plant
        return None

    def get_plants_in_row(self, row: int) -> list["Plant"]:
        if 0 <= row < self.rows:
            return [p for p in self.cells[row] if p is not None and p.is_alive]
        return []

    def get_all_plants(self) -> list["Plant"]:
        plants = []
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.cells[r][c]
                if p is not None and p.is_alive:
                    plants.append(p)
        return plants

    def update(self):
        # Clean up dead plants from cells
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.cells[r][c]
                if p is not None and not p.is_alive:
                    self.cells[r][c] = None

    def render_overlay(self, surface: pygame.Surface, hovered_cell: tuple[int, int] | None, is_valid: bool):
        # Draw inactive rows dark overlay if any rows are locked
        if len(self.active_rows) < self.rows:
            inactive_surf = pygame.Surface((CELL_WIDTH * self.cols, CELL_HEIGHT), pygame.SRCALPHA)
            inactive_surf.fill((0, 0, 0, 140))
            for r in range(self.rows):
                if r not in self.active_rows:
                    y = GRID_START_Y + r * CELL_HEIGHT
                    surface.blit(inactive_surf, (GRID_START_X, y))

        # Render hovered cell highlight if active
        if hovered_cell:
            r, c = hovered_cell
            x, y = self.get_cell_coords(r, c)
            highlight_color = COLOR_HIGHLIGHT_VALID if is_valid else COLOR_HIGHLIGHT_INVALID

            cell_surf = pygame.Surface((CELL_WIDTH, CELL_HEIGHT), pygame.SRCALPHA)
            cell_surf.fill(highlight_color)
            pygame.draw.rect(cell_surf, (255, 255, 255, 180), cell_surf.get_rect(), 3)
            surface.blit(cell_surf, (x, y))
