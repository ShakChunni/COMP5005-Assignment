"""Domain objects for the warehouse simulation."""

import math

from warehouse_app.constants import SHELF


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
        """Return the nearest unclaimed available good, or None."""
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

    def step_change(self, goods, grid):
        """Advance this robot by one simulation timestep."""
        if self.state == Robot.IDLE:
            self.claim_good(self.find_nearest_good(goods))

        elif self.state == Robot.MOVING_TO_GOOD:
            self._move_to_good(goods, grid)

        elif self.state == Robot.COLLECTING:
            self._collect_good()

        elif self.state == Robot.RETURNING:
            self._return_home(grid)

    def _move_to_good(self, goods, grid):
        """Move toward the target good or retarget if it is unavailable."""
        target = self.target_good
        if target is None:
            self.state = Robot.IDLE
            return

        target_taken = (
            not target.available
            or (
                target.claimed_by is not None
                and target.claimed_by != self.robot_id
            )
        )

        if target_taken:
            if target.claimed_by == self.robot_id:
                target.claimed_by = None
            self.target_good = None
            self.state = Robot.IDLE
            self.claim_good(self.find_nearest_good(goods))
        else:
            self.step_toward(target.x, target.y, grid)
            if self._is_next_to_target(target):
                self.state = Robot.COLLECTING

    def _collect_good(self):
        """Collect the target good if the robot is beside it."""
        target = self.target_good
        can_collect = (
            target is not None
            and target.available
            and target.claimed_by == self.robot_id
            and self._is_next_to_target(target)
        )

        if can_collect:
            target.available = False
            target.claimed_by = None
            self.target_good = None
            self.carrying = True
            self.state = Robot.RETURNING
        else:
            if target is not None and target.claimed_by == self.robot_id:
                target.claimed_by = None
            self.target_good = None
            self.state = Robot.IDLE

    def _return_home(self, grid):
        """Move home and complete a delivery when the robot arrives."""
        self.step_toward(self.home_x, self.home_y, grid)
        if self.x == self.home_x and self.y == self.home_y:
            if self.carrying:
                self.deliveries += 1
            self.carrying = False
            self.state = Robot.IDLE

    def _is_next_to_target(self, target):
        """Return True when the robot can pick from a shelf cell."""
        dx = abs(self.x - target.x)
        dy = abs(self.y - target.y)
        return (dx + dy) <= 1

    def _is_walkable(self, x, y, grid):
        """Return True if a coordinate is inside the grid and not a shelf."""
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

        for next_x, next_y in candidates:
            if self._is_walkable(next_x, next_y, grid):
                distance = math.hypot(target_x - next_x, target_y - next_y)
                if distance < best_distance:
                    best_distance = distance
                    best_position = (next_x, next_y)

        self.x, self.y = best_position
