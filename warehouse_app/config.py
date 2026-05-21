"""Command-line parsing and simulation configuration builders."""

import argparse
import csv

from warehouse_app.terrain import load_warehouse_from_csv


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
    """Prompt the user for an integer within the allowed range."""
    valid = False
    result = minimum

    while not valid:
        raw_value = input(message).strip()
        if raw_value.isdigit():
            number = int(raw_value)
            if minimum <= number <= maximum:
                result = number
                valid = True
            else:
                print(f"Enter a value between {minimum} and {maximum}.")
        else:
            print("Enter an integer value.")

    return result


def build_config_interactive():
    """Read simulation settings from interactive prompts."""
    print("Interactive mode")
    width = prompt_int("Warehouse width (6-50): ", 6, 50)
    height = prompt_int("Warehouse height (6-50): ", 6, 50)
    robot_count = prompt_int("Number of robots (1-20): ", 1, 20)
    goods_count = prompt_int("Number of goods (1-500): ", 1, 500)
    ticks = prompt_int("Simulation ticks (10-5000): ", 10, 5000)
    aisle_gap = prompt_int("Aisle gap between shelf columns (1-4): ", 1, 4)
    seed = prompt_int("Random seed (0-999999): ", 0, 999999)
    pause_ms = prompt_int("Display pause per tick in ms (0-300): ", 0, 300)

    return {
        "width": width,
        "height": height,
        "robot_count": robot_count,
        "goods_count": goods_count,
        "ticks": ticks,
        "aisle_gap": aisle_gap,
        "seed": seed,
        "pause": pause_ms / 1000.0,
    }


def build_config_batch(map_path, params_path):
    """Read simulation settings from CSV files."""
    grid = load_warehouse_from_csv(map_path)
    params = parse_params_file(params_path)

    robot_count = int(params.get("robots", "4"))
    goods_count = int(params.get("goods", "30"))
    ticks = int(params.get("ticks", "300"))
    seed = int(params.get("seed", "123"))
    pause = float(params.get("pause", "0.03"))

    return {
        "width": len(grid[0]),
        "height": len(grid),
        "robot_count": robot_count,
        "goods_count": goods_count,
        "ticks": ticks,
        "seed": seed,
        "pause": pause,
        "grid": grid,
    }


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
        help="Path to a map CSV file for batch mode.",
    )
    parser.add_argument(
        "-p",
        "--params-file",
        type=str,
        help="Path to a parameter CSV file for batch mode.",
    )
    return parser.parse_args()


def validate_args(args):
    """Validate the allowed command-line mode combinations."""
    if args.interactive:
        if args.map_file is not None or args.params_file is not None:
            raise ValueError("Use -i alone, or use -f and -p together.")
    elif args.map_file is None or args.params_file is None:
        raise ValueError("Batch mode requires both -f and -p.")
