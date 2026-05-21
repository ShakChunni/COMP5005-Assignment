"""Plotting helpers for the warehouse simulation."""

from matplotlib.colors import ListedColormap

from warehouse_app.constants import CORNER, FLOOR, SHELF


def draw_scene(ax_map, ax_stats, grid, robots, goods, tick, history):
    """Render the map and delivery statistics for the current tick."""
    color_values = {FLOOR: 0, SHELF: 1, CORNER: 2}
    numeric_grid = [
        [color_values.get(cell, 0) for cell in row]
        for row in grid
    ]

    cmap = ListedColormap(["#f5f3ef", "#4f5d75", "#95d5b2"])

    ax_map.clear()
    ax_map.imshow(numeric_grid, cmap=cmap, origin="upper")
    ax_map.set_title("Warehouse Map")
    ax_map.set_xlabel("X")
    ax_map.set_ylabel("Y")
    ax_map.set_xticks([])
    ax_map.set_yticks([])

    good_x = [good.x for good in goods if good.available]
    good_y = [good.y for good in goods if good.available]
    if good_x:
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
    ax_stats.set_ylim(0, max(1, history[-1] + 1))
