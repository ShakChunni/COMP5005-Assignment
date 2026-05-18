# COMP5005 Robotic Warehouse Simulation - Project Plan

This plan is structured to directly address the 7 assessed features outlined in the COMP5005 Assignment 1 specification, while strictly adhering to the unit's coding rules (no `while True`, `break`, `continue`, or `global` variables, and maintaining strict PEP 8 formatting). The goal is to build a fully functional, explainable, and exam-ready piece of software.

---

## Phase 1: Core Data Structures (Features 1 & 2)
**Objective**: Build the foundational objects representing the entities in the warehouse.

1. **`Good` Class**:
   - **Attributes**: `x`, `y`, `available` (boolean), `claimed_by` (robot_id or None).
   - **Purpose**: Represents a single item on a shelf. A reservation system ensures that once a robot targets a good, others cannot claim it.
2. **`Robot` Class**:
   - **Attributes**: `robot_id`, `home_x`, `home_y`, `x`, `y`, `state`, `target_good`, `carrying`, `deliveries`.
   - **States**: Constants for `"idle"`, `"moving_to_good"`, `"collecting"`, `"returning"`.
   - **Methods**: 
     - `find_nearest_good(goods)`: Uses `math.hypot` to calculate Euclidean distance and returns the nearest *available* good.
     - `step_toward(target_x, target_y, grid)`: Moves one square per tick toward the destination, avoiding `"shelf"` cells.

## Phase 2: Warehouse Terrain & Initialization (Feature 4)
**Objective**: Create the physical constraints of the warehouse environment.

1. **Grid Layout**:
   - A 2D list containing string markers: `"floor"`, `"shelf"`, and `"corner"`.
   - Ensure the four corners `(0,0)`, `(0, height-1)`, `(width-1, 0)`, `(width-1, height-1)` are always walkable (`"corner"`).
2. **Terrain Generation**:
   - Write a procedural generation function that places vertical columns of shelves separated by walkable aisles.
   - Write a secondary function to read terrain directly from a CSV file (for batch mode).

## Phase 3: The Simulation Workflow (Feature 3)
**Objective**: Implement the overarching task allocation and delivery lifecycle.

1. **State Machine Logic**:
   - Handled inside the main simulation loop for each robot on every tick.
   - **Idle**: Call `find_nearest_good()`. If successful, claim it and change state to `moving_to_good`.
   - **Moving to Good**: Call `step_toward()`. If at the good's location, change to `collecting`. If the good becomes unavailable, re-target immediately.
   - **Collecting**: Mark the good as picked up, set `carrying = True`, change state to `returning`.
   - **Returning**: Call `step_toward()` back to home corner. Once there, increment `deliveries` and reset to `idle`.

## Phase 4: User Interface & CLI (Feature 5)
**Objective**: Allow standard and automated execution of the program.

1. **`argparse` Implementation**:
   - Create mutually exclusive groups for interactive mode (`-i`) and batch mode (`-f` and `-p`).
2. **Interactive Mode**:
   - Use `input()` loops (with condition checks, no `while True`) to ask the user for warehouse dimensions, number of robots, and goods count.
3. **Batch Mode**:
   - Use the `csv` module to parse map layout from the map file.
   - Parse simulation variables (e.g., tick count, robots) from the parameters file.

## Phase 5: Visualisation & Statistics (Features 6 & 7)
**Objective**: Provide a live display and final summary to analyze system performance.

1. **Live Display (Matplotlib)**:
   - Create a single figure with two subplots: `1x2` layout.
   - **Left Subplot (`ax_map`)**: A visual grid of the warehouse using `imshow()` or `pcolormesh()`. Update robot and goods positions on every tick.
   - **Right Subplot (`ax_stats`)**: A line chart tracking "Total Deliveries over Time" or "Active Robots over Time".
   - Use `plt.pause()` to update the figure dynamically without blocking execution.
2. **Final Summary**:
   - At the end of the simulation loop, print a clean summary to the terminal.
   - Include: Total ticks elapsed, total goods delivered, throughput (deliveries per tick), and individual robot performance.

---

## Development Strategy
To ensure the code remains simple and easy to explain during the demonstration:
1. **Step 1**: Write `warehouse.py` with just the `Good`, `Robot`, and `generate_warehouse` functions. Print simple text logs to ensure logic works.
2. **Step 2**: Implement the CLI (`argparse`) to handle both user inputs and CSV files correctly.
3. **Step 3**: Introduce `matplotlib` for the visual rendering.
4. **Step 4**: Do a final pass to ensure strict PEP 8 compliance, full docstrings, inline comments for any complex math/logic, and removal of any forbidden constructs.
