"""Simulation workflow and summary statistics."""

import matplotlib.pyplot as plt

from warehouse_app.models import Robot
from warehouse_app.terrain import get_corner_positions
from warehouse_app.visualisation import draw_scene


def build_robots(robot_count, width, height):
    """Create robots and place each one on a valid corner."""
    corners = get_corner_positions(width, height)
    robots = []

    for robot_id in range(robot_count):
        home_x, home_y = corners[robot_id % len(corners)]
        robots.append(Robot(robot_id + 1, home_x, home_y))

    return robots


def process_robot_tick(robot, goods, grid):
    """Advance one robot by one simulation tick."""
    robot.step_change(goods, grid)


def count_available_goods(goods):
    """Count how many goods have not yet been collected."""
    return sum(1 for good in goods if good.available)


def print_summary(ticks, robots, goods):
    """Print end-of-run simulation statistics."""
    total_deliveries = sum(robot.deliveries for robot in robots)
    remaining_goods = count_available_goods(goods)
    throughput = total_deliveries / ticks if ticks > 0 else 0.0

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


def run_simulation(grid, robots, goods, ticks, pause):
    """Run the simulation and show realtime plots plus a final summary."""
    interactive_display = plt.get_backend().lower() != "agg"
    if interactive_display:
        plt.ion()

    figure, (ax_map, ax_stats) = plt.subplots(1, 2, figsize=(12, 5))
    history = []

    for tick in range(ticks):
        for robot in robots:
            process_robot_tick(robot, goods, grid)

        total_deliveries = sum(robot.deliveries for robot in robots)
        history.append(total_deliveries)
        draw_scene(ax_map, ax_stats, grid, robots, goods, tick, history)

        if interactive_display:
            plt.tight_layout()
            plt.pause(max(pause, 0.001))

    if interactive_display:
        plt.ioff()
        plt.show()
    else:
        plt.close(figure)

    print_summary(ticks, robots, goods)
