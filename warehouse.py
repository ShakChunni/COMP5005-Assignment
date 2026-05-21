"""Entry point for the COMP5005 robotic warehouse simulation."""

import random
import sys

from warehouse_app.config import (
    build_config_batch,
    build_config_interactive,
    parse_args,
    validate_args,
)
from warehouse_app.simulation import build_robots, run_simulation
from warehouse_app.terrain import generate_goods, generate_warehouse


def main():
    """Parse configuration, build the scenario, and run the simulation."""
    args = parse_args()

    try:
        validate_args(args)

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
    except (OSError, ValueError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
