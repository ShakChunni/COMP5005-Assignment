"""COMP5005 robotic warehouse simulation."""

import argparse
import csv
import math
import random
import sys

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


FLOOR = "floor"
SHELF = "shelf"
CORNER = "corner"


class Good:
    """Represents one collectable item stored on a shelf cell."""

    def __init__(self, x, y):
        """Create a good at coordinate (x, y)."""
        self.x = x
        self.y = y
        self.available = True
        self.claimed_by = None


class Robot:
    """Represents one autonomous robot in the warehouse."""

    IDLE = "idle"
    MOVING_TO_GOOD = "moving_to_good"
    COLLECTING = "collecting"
    RETURNING = "returning"

    def __init__(self, robot_id, home_x, home_y):
        """Create a robot and place it at its home corner."""
        self.robot_id = robot_id
        self.home_x = home_x
        self.home_y = home_y
        self.x = home_x
        self.y = home_y
        self.state = Robot.IDLE
        self.target_good = None
        self.carrying = False
        self.deliveries = 0

    def find_nearest_good(self, goods):
        """Return nearest unclaimed available good, or None."""
        best_good = None
        best_distance = None
        for good in goods:
            if good.available and good.claimed_by is None:
                distance = math.hypot(good.x - self.x, good.y - self.y)
                if best_distance is None or distance < best_distance:
                    best_distance = distance
                    best_good = good
        return best_good

    def claim_good(self, good):
        """Reserve a good for this robot and switch to moving state."""
        if good is not None:
            good.claimed_by = self.robot_id
            self.target_good = good
            self.state = Robot.MOVING_TO_GOOD

    def _is_walkable(self, x, y, grid):
        """Return True if a coordinate is inside grid and not a shelf."""
        height = len(grid)
        width = len(grid[0])
        if x < 0 or y < 0 or x >= width or y >= height:
            return False
        return grid[y][x] != SHELF

    def step_toward(self, target_x, target_y, grid):
        """Move one step toward target without entering shelf cells."""
        dx = target_x - self.x
        dy = target_y - self.y
        move_x = 0
        move_y = 0

        if dx > 0:
            move_x = 1
        elif dx < 0:
            move_x = -1

        if dy > 0:
            move_y = 1
        elif dy < 0:
            move_y = -1

        candidates = []
        if move_x != 0:
            candidates.append((self.x + move_x, self.y))
        if move_y != 0:
            candidates.append((self.x, self.y + move_y))

        # If direct move is blocked, try other neighbors.
        neighbors = [
            (self.x + 1, self.y),
            (self.x - 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1),
        ]
        for point in neighbors:
            if point not in candidates:
                candidates.append(point)

        best_position = (self.x, self.y)
        best_distance = math.hypot(target_x - self.x, target_y - self.y)

        for nx, ny in candidates:
            if self._is_walkable(nx, ny, grid):
                distance = math.hypot(target_x - nx, target_y - ny)
                if distance < best_distance:
                    best_distance = distance
                    best_position = (nx, ny)

        self.x, self.y = best_position


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
    grid = []
    for _ in range(height):
        row = [FLOOR] * width
        grid.append(row)

    column_step = aisle_gap + 1
    x = 1
    while x < width - 1:
        y = 1
        while y < height - 1:
            grid[y][x] = SHELF
            y += 1
        x += column_step

    for cx, cy in get_corner_positions(width, height):
        grid[cy][cx] = CORNER

    return grid


def load_warehouse_from_csv(path):
    """Load warehouse terrain from CSV."""
    grid = []
    with open(path, "r", encoding="utf-8") as file_obj:
        reader = csv.reader(file_obj)
        for row in reader:
            if len(row) > 0:
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

    if len(grid) == 0:
        raise ValueError("Map file is empty.")

    width = len(grid[0])
    for row in grid:
        if len(row) != width:
            raise ValueError("Map file has uneven row lengths.")

    height = len(grid)
    for cx, cy in get_corner_positions(width, height):
        grid[cy][cx] = CORNER

    return grid


def parse_params_file(path):
    """Parse batch parameters from a key,value CSV file."""
    params = {}
    with open(path, "r", encoding="utf-8") as file_obj:
        reader = csv.reader(file_obj)
        for row in reader:
            if len(row) >= 2:
                key = row[0].strip().lower()
                value = row[1].strip()
                params[key] = value
    return params


def prompt_int(message, minimum, maximum):
    """Prompt the user for an integer in [minimum, maximum]."""
    valid = False
    result = minimum

    while not valid:
        raw = input(message).strip()
        if raw.isdigit():
            number = int(raw)
            if minimum <= number <= maximum:
                result = number
                valid = True
            else:
                print(f"Enter a value between {minimum} and {maximum}.")
        else:
            print("Enter an integer value.")

    return result


def build_config_interactive():
    """Read simulation settings from user prompts."""
    print("Interactive mode")
    width = prompt_int("Warehouse width (6-50): ", 6, 50)
    height = prompt_int("Warehouse height (6-50): ", 6, 50)
    robot_count = prompt_int("Number of robots (1-20): ", 1, 20)
    goods_count = prompt_int("Number of goods (1-500): ", 1, 500)
    ticks = prompt_int("Simulation ticks (10-5000): ", 10, 5000)
    aisle_gap = prompt_int("Aisle gap between shelf columns (1-4): ", 1, 4)
    seed = prompt_int("Random seed (0-999999): ", 0, 999999)
    pause_ms = prompt_int("Display pause per tick in ms (0-300): ", 0, 300)

    config = {
        "width": width,
        "height": height,
        "robot_count": robot_count,
        "goods_count": goods_count,
        "ticks": ticks,
        "aisle_gap": aisle_gap,
        "seed": seed,
        "pause": pause_ms / 1000.0,
    }
    return config


def build_config_batch(map_path, params_path):
    """Read simulation settings from CSV files."""
    grid = load_warehouse_from_csv(map_path)
    params = parse_params_file(params_path)

    robot_count = int(params.get("robots", "4"))
    goods_count = int(params.get("goods", "30"))
    ticks = int(params.get("ticks", "300"))
    seed = int(params.get("seed", "123"))
    pause = float(params.get("pause", "0.03"))

    config = {
        "width": len(grid[0]),
        "height": len(grid),
        "robot_count": robot_count,
        "goods_count": goods_count,
        "ticks": ticks,
        "aisle_gap": 2,
        "seed": seed,
        "pause": pause,
        "grid": grid,
    }
    return config


def pick_shelf_locations(grid):
    """Return all shelf coordinates from the terrain grid."""
    shelf_cells = []
    y = 0
    while y < len(grid):
        x = 0
        while x < len(grid[0]):
            if grid[y][x] == SHELF:
                shelf_cells.append((x, y))
            x += 1
        y += 1
    return shelf_cells


def generate_goods(goods_count, grid):
    """Generate goods on shelf cells; duplicates per shelf are allowed."""
    shelf_cells = pick_shelf_locations(grid)
    if len(shelf_cells) == 0:
        raise ValueError("No shelf cells found. Cannot place goods.")

    goods = []
    for _ in range(goods_count):
        x, y = random.choice(shelf_cells)
        goods.append(Good(x, y))
    return goods


def build_robots(robot_count, width, height):
    """Create robots and place each one on a valid corner."""
    corners = get_corner_positions(width, height)
    robots = []
    for robot_id in range(robot_count):
        home_x, home_y = corners[robot_id % len(corners)]
        robots.append(Robot(robot_id + 1, home_x, home_y))
    return robots


def try_assign_target(robot, goods):
    """Assign nearest available good to a robot if possible."""
    nearest = robot.find_nearest_good(goods)
    if nearest is not None:
        robot.claim_good(nearest)


def process_robot_tick(robot, goods, grid):
    """Advance one robot by one simulation tick."""
    if robot.state == Robot.IDLE:
        try_assign_target(robot, goods)

    elif robot.state == Robot.MOVING_TO_GOOD:
        target = robot.target_good
        if target is None:
            robot.state = Robot.IDLE
        else:
            target_taken = (
                (not target.available)
                or (
                    target.claimed_by is not None
                    and target.claimed_by != robot.robot_id
                )
            )
            if target_taken:
                if target.claimed_by == robot.robot_id:
                    target.claimed_by = None
                robot.target_good = None
                robot.state = Robot.IDLE
                try_assign_target(robot, goods)
            else:
                robot.step_toward(target.x, target.y, grid)
                dx = abs(robot.x - target.x)
                dy = abs(robot.y - target.y)
                # Goods are on shelf cells, so collect from adjacent tile.
                can_reach_shelf = (dx + dy) <= 1
                if can_reach_shelf:
                    robot.state = Robot.COLLECTING

    elif robot.state == Robot.COLLECTING:
        target = robot.target_good
        dx = 0
        dy = 0
        if target is not None:
            dx = abs(robot.x - target.x)
            dy = abs(robot.y - target.y)

        can_collect = (
            target is not None
            and target.available
            and target.claimed_by == robot.robot_id
            and (dx + dy) <= 1
        )
        if can_collect:
            target.available = False
            target.claimed_by = None
            robot.target_good = None
            robot.carrying = True
            robot.state = Robot.RETURNING
        else:
            # Lost the target before pickup, reset and retarget next tick.
            if target is not None and target.claimed_by == robot.robot_id:
                target.claimed_by = None
            robot.target_good = None
            robot.state = Robot.IDLE

    elif robot.state == Robot.RETURNING:
        robot.step_toward(robot.home_x, robot.home_y, grid)
        if robot.x == robot.home_x and robot.y == robot.home_y:
            if robot.carrying:
                robot.deliveries += 1
            robot.carrying = False
            robot.state = Robot.IDLE


def count_available_goods(goods):
    """Count goods that have not yet been collected."""
    count = 0
    for good in goods:
        if good.available:
            count += 1
    return count


def draw_scene(ax_map, ax_stats, grid, robots, goods, tick, history):
    """Render map and statistics subplots for the current tick."""
    color_values = {FLOOR: 0, SHELF: 1, CORNER: 2}
    numeric_grid = []
    for row in grid:
        numeric_row = []
        for cell in row:
            numeric_row.append(color_values.get(cell, 0))
        numeric_grid.append(numeric_row)

    cmap = ListedColormap(["#f5f3ef", "#4f5d75", "#95d5b2"])

    ax_map.clear()
    ax_map.imshow(numeric_grid, cmap=cmap, origin="upper")
    ax_map.set_title("Warehouse Map")
    ax_map.set_xlabel("X")
    ax_map.set_ylabel("Y")
    ax_map.set_xticks([])
    ax_map.set_yticks([])

    good_x = []
    good_y = []
    for good in goods:
        if good.available:
            good_x.append(good.x)
            good_y.append(good.y)

    if len(good_x) > 0:
        ax_map.scatter(
            good_x,
            good_y,
            c="#ffbe0b",
            marker="o",
            s=45,
            edgecolors="black",
            linewidths=0.4,
            label="Available goods",
        )

    robot_x = []
    robot_y = []
    for robot in robots:
        robot_x.append(robot.x)
        robot_y.append(robot.y)
        ax_map.text(
            robot.x,
            robot.y,
            str(robot.robot_id),
            color="white",
            fontsize=8,
            ha="center",
            va="center",
        )

    ax_map.scatter(
        robot_x,
        robot_y,
        c="#ef476f",
        marker="s",
        s=65,
        edgecolors="black",
        linewidths=0.5,
        label="Robots",
    )
    ax_map.legend(loc="upper right", fontsize=7)

    ax_stats.clear()
    x_axis = list(range(1, len(history) + 1))
    ax_stats.plot(x_axis, history, color="#118ab2", linewidth=2)
    ax_stats.set_title("Total Deliveries Over Time")
    ax_stats.set_xlabel("Tick")
    ax_stats.set_ylabel("Deliveries")
    ax_stats.grid(True, alpha=0.3)
    ax_stats.set_xlim(1, max(2, tick + 1))
    upper = max(1, history[-1] + 1)
    ax_stats.set_ylim(0, upper)


def run_simulation(grid, robots, goods, ticks, pause):
    """Run the simulation and show realtime plots plus final summary."""
    plt.ion()
    figure, (ax_map, ax_stats) = plt.subplots(1, 2, figsize=(12, 5))
    history = []

    tick = 0
    while tick < ticks:
        for robot in robots:
            process_robot_tick(robot, goods, grid)

        total_deliveries = sum(robot.deliveries for robot in robots)
        history.append(total_deliveries)
        draw_scene(ax_map, ax_stats, grid, robots, goods, tick, history)
        plt.tight_layout()
        plt.pause(pause)
        tick += 1

    plt.ioff()
    plt.show()
    print_summary(ticks, robots, goods)


def print_summary(ticks, robots, goods):
    """Print end-of-run simulation statistics."""
    total_deliveries = sum(robot.deliveries for robot in robots)
    remaining_goods = count_available_goods(goods)
    throughput = 0.0
    if ticks > 0:
        throughput = total_deliveries / ticks

    print("\nSimulation Summary")
    print("-" * 40)
    print(f"Ticks elapsed: {ticks}")
    print(f"Total deliveries: {total_deliveries}")
    print(f"Remaining goods: {remaining_goods}")
    print(f"Throughput (deliveries/tick): {throughput:.3f}")
    print("\nRobot performance:")
    for robot in robots:
        print(
            f"Robot {robot.robot_id}: deliveries={robot.deliveries}, "
            f"final_state={robot.state}, position=({robot.x}, {robot.y})"
        )


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="COMP5005 robotic warehouse simulation"
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Run in interactive prompt mode.",
    )
    parser.add_argument(
        "-f",
        "--map-file",
        type=str,
        help="Path to map CSV file for batch mode.",
    )
    parser.add_argument(
        "-p",
        "--params-file",
        type=str,
        help="Path to params CSV file for batch mode.",
    )
    return parser.parse_args()


def validate_args(args):
    """Validate mode combination for CLI arguments."""
    if args.interactive:
        if args.map_file is not None or args.params_file is not None:
            raise ValueError("Use -i alone, or use -f and -p together.")
    else:
        if args.map_file is None or args.params_file is None:
            raise ValueError("Batch mode requires both -f and -p.")


def main():
    """Program entry point."""
    args = parse_args()
    try:
        validate_args(args)
    except ValueError as error:
        print(f"Argument error: {error}")
        sys.exit(1)

    if args.interactive:
        config = build_config_interactive()
        grid = generate_warehouse(
            config["width"], config["height"], config["aisle_gap"]
        )
    else:
        config = build_config_batch(args.map_file, args.params_file)
        grid = config["grid"]

    random.seed(config["seed"])
    robots = build_robots(
        config["robot_count"], config["width"], config["height"]
    )
    goods = generate_goods(config["goods_count"], grid)
    run_simulation(grid, robots, goods, config["ticks"], config["pause"])


if __name__ == "__main__":
    main()
