"""Functional tests for the robotic warehouse assignment."""

import os
import subprocess
import sys
import tempfile
import unittest

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

from warehouse_app.config import build_config_batch, validate_args
from warehouse_app.constants import CORNER, SHELF
from warehouse_app.models import Good, Robot
from warehouse_app.simulation import build_robots, count_available_goods
from warehouse_app.terrain import (
    generate_goods,
    generate_warehouse,
    get_corner_positions,
    load_warehouse_from_csv,
)


class WarehouseModelTests(unittest.TestCase):
    """Tests for goods, robots, and robot workflow."""

    def test_good_stores_location_and_availability(self):
        good = Good(3, 4)

        self.assertEqual((good.x, good.y), (3, 4))
        self.assertTrue(good.available)
        self.assertIsNone(good.claimed_by)

    def test_robot_selects_nearest_unclaimed_good(self):
        robot = Robot(1, 0, 0)
        far_good = Good(8, 8)
        near_good = Good(1, 2)
        claimed_good = Good(0, 1)
        claimed_good.claimed_by = 2

        selected = robot.find_nearest_good(
            [far_good, near_good, claimed_good]
        )

        self.assertIs(selected, near_good)

    def test_robot_claims_and_delivers_one_good(self):
        grid = generate_warehouse(8, 8, 2)
        robot = Robot(1, 0, 0)
        goods = [Good(1, 5)]

        for _ in range(40):
            robot.step_change(goods, grid)

        self.assertEqual(robot.deliveries, 1)
        self.assertFalse(goods[0].available)
        self.assertEqual(robot.state, Robot.IDLE)
        self.assertEqual((robot.x, robot.y), (0, 0))

    def test_robot_retargets_when_target_is_taken(self):
        grid = generate_warehouse(8, 8, 2)
        robot = Robot(1, 0, 0)
        first_good = Good(1, 5)
        second_good = Good(1, 1)
        robot.claim_good(first_good)

        first_good.available = False
        robot.step_change([first_good, second_good], grid)

        self.assertIs(robot.target_good, second_good)
        self.assertEqual(second_good.claimed_by, robot.robot_id)

    def test_robot_does_not_enter_shelf_cell(self):
        grid = generate_warehouse(8, 8, 2)
        robot = Robot(1, 0, 0)

        robot.step_toward(1, 1, grid)

        self.assertNotEqual(grid[robot.y][robot.x], SHELF)


class WarehouseTerrainTests(unittest.TestCase):
    """Tests for generated and CSV-loaded warehouse terrain."""

    def test_generated_warehouse_has_corner_homes_and_shelves(self):
        grid = generate_warehouse(10, 8, 2)
        corners = get_corner_positions(10, 8)

        for x, y in corners:
            self.assertEqual(grid[y][x], CORNER)
        self.assertEqual(grid[1][1], SHELF)

    def test_csv_loader_reads_shelves_and_corners(self):
        grid = load_warehouse_from_csv("data/map1.csv")

        self.assertEqual(grid[0][0], CORNER)
        self.assertEqual(grid[1][1], SHELF)

    def test_goods_are_generated_only_on_shelves(self):
        grid = generate_warehouse(10, 8, 2)
        goods = generate_goods(20, grid)

        self.assertEqual(len(goods), 20)
        for good in goods:
            self.assertEqual(grid[good.y][good.x], SHELF)


class WarehouseConfigAndCliTests(unittest.TestCase):
    """Tests for configuration, robot spawning, and CLI behaviour."""

    def test_build_robots_cycles_through_four_corners(self):
        robots = build_robots(6, 10, 8)
        homes = [(robot.home_x, robot.home_y) for robot in robots]

        self.assertEqual(
            homes,
            [(0, 0), (9, 0), (0, 7), (9, 7), (0, 0), (9, 0)],
        )

    def test_batch_config_reads_map_and_parameters(self):
        config = build_config_batch("data/map1.csv", "data/params1.csv")

        self.assertEqual(config["width"], 10)
        self.assertEqual(config["height"], 8)
        self.assertEqual(config["robot_count"], 4)
        self.assertEqual(config["goods_count"], 20)

    def test_validate_args_rejects_missing_batch_files(self):
        class Args:
            interactive = False
            map_file = None
            params_file = None

        with self.assertRaises(ValueError):
            validate_args(Args())

    def test_cli_batch_run_prints_summary(self):
        env = os.environ.copy()
        env["MPLBACKEND"] = "Agg"
        env.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

        result = subprocess.run(
            [
                sys.executable,
                "warehouse.py",
                "-f",
                "data/map1.csv",
                "-p",
                "data/params1.csv",
            ],
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )

        self.assertIn("Simulation Summary", result.stdout)
        self.assertIn("Total deliveries: 20", result.stdout)
        self.assertEqual(count_available_goods([]), 0)


if __name__ == "__main__":
    unittest.main()
