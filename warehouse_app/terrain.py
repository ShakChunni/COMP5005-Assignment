"""Warehouse terrain generation and CSV loading utilities."""

import csv
import random

from warehouse_app.constants import CORNER, FLOOR, SHELF
from warehouse_app.models import Good


def get_corner_positions(width, height):
    """Return the four valid corner coordinates for the map."""
    return [
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1),
    ]


def generate_warehouse(width, height, aisle_gap):
    """Generate a shelf-and-aisle warehouse map."""
    grid = [[FLOOR for _ in range(width)] for _ in range(height)]
    column_step = aisle_gap + 1

    for x in range(1, width - 1, column_step):
        for y in range(1, height - 1):
            grid[y][x] = SHELF

    for corner_x, corner_y in get_corner_positions(width, height):
        grid[corner_y][corner_x] = CORNER

    return grid


def load_warehouse_from_csv(path):
    """Load a warehouse terrain grid from CSV."""
    grid = []

    with open(path, "r", encoding="utf-8") as file_obj:
        reader = csv.reader(file_obj)
        for row in reader:
            if row:
                parsed_row = []
                for cell in row:
                    token = cell.strip().lower()
                    if token in ("shelf", "s", "1", "#"):
                        parsed_row.append(SHELF)
                    elif token in ("corner", "c"):
                        parsed_row.append(CORNER)
                    else:
                        parsed_row.append(FLOOR)
                grid.append(parsed_row)

    if not grid:
        raise ValueError("Map file is empty.")

    width = len(grid[0])
    for row in grid:
        if len(row) != width:
            raise ValueError("Map file has uneven row lengths.")

    height = len(grid)
    for corner_x, corner_y in get_corner_positions(width, height):
        grid[corner_y][corner_x] = CORNER

    return grid


def pick_shelf_locations(grid):
    """Return all shelf coordinates from the terrain grid."""
    shelf_cells = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == SHELF:
                shelf_cells.append((x, y))

    return shelf_cells


def generate_goods(goods_count, grid):
    """Generate goods on shelf cells; duplicates per shelf are allowed."""
    shelf_cells = pick_shelf_locations(grid)
    if not shelf_cells:
        raise ValueError("No shelf cells found. Cannot place goods.")

    return [Good(*random.choice(shelf_cells)) for _ in range(goods_count)]
