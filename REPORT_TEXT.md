# Project Report: Robotic Warehouse Simulation

Name: Ashfaq
Student Number: 23472297
Date: 21 May 2026

## Overview

This project implements a robotic warehouse simulation for the COMP5005 Fundamentals of Programming assignment. The program models a warehouse as a two-dimensional grid containing walkable floor cells, blocked shelf cells, and four corner home positions. Autonomous robots begin from the warehouse corners, find goods stored at shelf coordinates, travel toward the selected shelf, collect one item, and return the item to their original home corner.

The implementation addresses the main requirements in the v2 assignment brief. Robots and goods are represented as objects, shelves are treated as obstacles, robots are allowed to overlap, goods can be generated automatically, multiple goods may exist at the same shelf location, and the program supports both interactive and batch execution. The simulation also provides a Matplotlib display using subplots: one subplot for the warehouse map and one subplot for delivery statistics over time.

The final implementation is organised into small modules. `warehouse.py` is the program entry point. The `warehouse_app` package contains configuration handling, object models, terrain generation and loading, simulation control, constants, and visualisation. The `data` directory contains reproducible CSV input files for three showcase scenarios. The `tests` directory contains functional tests for the major assignment features.

## User Guide

### Requirements

The program requires Python 3 and Matplotlib. Matplotlib is permitted under the assignment FAQ because other packages may be used to improve or extend the simulation, provided object-orientation remains central to the warehouse-level behaviour. This project uses Matplotlib only for plotting; robot and good behaviour is still implemented through Python classes.

Install Matplotlib if required:

```bash
python3 -m pip install matplotlib
```

### Interactive Mode

Run interactive mode with:

```bash
python3 warehouse.py -i
```

Interactive mode asks for warehouse width, warehouse height, number of robots, number of goods, simulation length, aisle gap between shelf columns, random seed, and display pause. It then generates a structured shelf-and-aisle warehouse and starts the simulation.

### Batch Mode

Run batch mode with a map file and parameter file:

```bash
python3 warehouse.py -f data/map1.csv -p data/params1.csv
```

Additional prepared scenarios are:

```bash
python3 warehouse.py -f data/map2.csv -p data/params2.csv
python3 warehouse.py -f data/map3.csv -p data/params3.csv
```

Batch mode is useful for repeatable testing and for report scenarios because the same inputs and seeds can be reused.

### Batch Files

Map files are CSV grids. Shelf cells may be written as `shelf`, `s`, `1`, or `#`. Corner cells may be written as `corner` or `c`. Other tokens are treated as floor cells.

Parameter files use `key,value` rows. Supported keys are `robots`, `goods`, `ticks`, `seed`, and `pause`.

### Testing

Run all functional tests with:

```bash
python3 -m unittest discover -s tests -v
```

Run a syntax check with:

```bash
python3 -m py_compile warehouse.py warehouse_app/*.py tests/*.py
```

If running without a graphical display, use the Agg backend:

```bash
MPLBACKEND=Agg python3 warehouse.py -f data/map1.csv -p data/params1.csv
```

### Submission FAQ Notes

The assignment FAQ states that the report may be submitted as DOCX or PDF. This report is prepared in DOCX format using the provided `Project_Report_StudentID.docx` template. If converted to PDF, the same PDF should also be included in the zip file and submitted to Turnitin.

The FAQ also states that additional packages may be used. This program uses Matplotlib for visualisation only. The warehouse-level behaviour remains object-oriented through the `Robot` and `Good` classes.

## Traceability Matrix

| Feature | Code Reference | Test Reference | Status | Date Completed |
|---|---|---|---|---|
| 1.0 Robots are objects with position, home corner, state, and target good | `warehouse_app/models.py`, `Robot`, lines 19-191 | `tests/test_warehouse.py`, `test_robot_claims_and_delivers_one_good`; batch scenario runs | P | 21/05/2026 |
| 1.1 Robot states are represented clearly | `warehouse_app/models.py`, lines 22-25 | `test_robot_claims_and_delivers_one_good`; final summaries show final states | P | 21/05/2026 |
| 1.2 Robots spawn at the four corners | `warehouse_app/simulation.py`, `build_robots`, lines 10-19; `terrain.py`, `get_corner_positions`, lines 10-17 | `test_build_robots_cycles_through_four_corners` | P | 21/05/2026 |
| 2.0 Goods store location, availability, and reservation state | `warehouse_app/models.py`, `Good`, lines 8-16 | `test_good_stores_location_and_availability` | P | 21/05/2026 |
| 2.1 Multiple goods may exist at the same shelf location | `warehouse_app/terrain.py`, `generate_goods`, lines 81-87 | `test_goods_are_generated_only_on_shelves`; duplicate positions are allowed because goods are individual objects | P | 21/05/2026 |
| 2.2 Robots select the nearest available unclaimed good | `warehouse_app/models.py`, `find_nearest_good`, lines 39-51 | `test_robot_selects_nearest_unclaimed_good` | P | 21/05/2026 |
| 3.0 Pickup-return workflow is implemented | `warehouse_app/models.py`, `step_change`, lines 60-72; `_collect_good`, lines 100-120; `_return_home`, lines 122-129 | `test_robot_claims_and_delivers_one_good` | P | 21/05/2026 |
| 3.1 Robot retargets if target becomes unavailable | `warehouse_app/models.py`, `_move_to_good`, lines 74-99 | `test_robot_retargets_when_target_is_taken` | P | 21/05/2026 |
| 4.0 Warehouse terrain contains shelves and walkable aisles | `warehouse_app/terrain.py`, `generate_warehouse`, lines 20-32; `load_warehouse_from_csv`, lines 35-66 | `test_generated_warehouse_has_corner_homes_and_shelves`; `test_csv_loader_reads_shelves_and_corners` | P | 21/05/2026 |
| 4.1 Robots cannot move through shelves | `warehouse_app/models.py`, `_is_walkable`, lines 137-145; `step_toward`, lines 147-191 | `test_robot_does_not_enter_shelf_cell` | P | 21/05/2026 |
| 5.0 Interactive mode is supported | `warehouse_app/config.py`, `build_config_interactive`, lines 44-65; `warehouse.py`, lines 23-27 | Manual run: `python3 warehouse.py -i` | P | 21/05/2026 |
| 5.1 Batch mode is supported | `warehouse_app/config.py`, `build_config_batch`, lines 68-88; `validate_args`, lines 117-123 | `test_batch_config_reads_map_and_parameters`; `test_cli_batch_run_prints_summary` | P | 21/05/2026 |
| 6.0 Simulation updates each timestep using object methods | `warehouse_app/models.py`, `step_change`, lines 60-72; `simulation.py`, `process_robot_tick`, lines 22-24 | `test_robot_claims_and_delivers_one_good`; batch scenario runs | P | 21/05/2026 |
| 7.0 Realtime display and statistics are provided with subplots | `warehouse_app/visualisation.py`, `draw_scene`, lines 8-75; `simulation.py`, `run_simulation`, lines 52-79 | Manual visual run; batch runs using Agg backend for summary verification | P | 21/05/2026 |
| 7.1 Final summary statistics are printed | `warehouse_app/simulation.py`, `print_summary`, lines 32-49 | `test_cli_batch_run_prints_summary` | P | 21/05/2026 |

## Discussion

### Object Model

The simulation uses two main domain classes: `Good` and `Robot`. A `Good` stores its shelf coordinates, whether it is still available, and which robot has claimed it. A `Robot` stores its ID, home corner, current position, current state, target good, carrying flag, and delivery count. This matches the assignment requirement that robots should know their position, home corner, state, and target.

The robot has four states: `idle`, `moving_to_good`, `collecting`, and `returning`. These states make the workflow explicit and easy to explain. The normal cycle is: idle robot selects a target, moves toward the target, collects the good, returns home, records the delivery, and becomes idle again.

### Goods and Targeting

Goods are created as separate objects. This means multiple goods can exist at the same shelf coordinate because each item is still a separate `Good` instance. Availability is tracked with the `available` attribute. Reservation is tracked with the `claimed_by` attribute. A robot only chooses goods where `available` is true and `claimed_by` is `None`.

The nearest-target decision uses Euclidean distance through `math.hypot()`. This is simple and consistent. When a robot chooses a good, it claims the good immediately. This reduces duplicate targeting by different robots. If a target becomes unavailable before pickup, the robot releases the old target, returns to the idle logic, and selects another available good.

### Timestep Simulation Logic

The v2 assignment brief says that each timestep should move robots, collect goods, return goods, or retarget depending on state, and that this behaviour should be driven by methods such as `step_change()`. To match that wording, the `Robot` class includes a `step_change(goods, grid)` method. The simulation loop calls this method once per robot per tick through `process_robot_tick()`.

This design keeps the robot behaviour inside the robot object. The simulation loop remains responsible for ordering updates, collecting statistics, and drawing the scene. This separation makes the code easier to explain because object behaviour and global simulation control are not mixed together.

### Warehouse Terrain

The warehouse is a 2D list of terrain strings. The possible terrain values are floor, shelf, and corner. Shelves are blocked cells. Corners and floor cells are walkable. Interactive mode generates structured shelf columns with aisle gaps. Batch mode loads terrain from CSV files.

Robots are spawned only at the four corner positions. If there are more than four robots, the code cycles through the four corners. This follows the assignment rule that robots are initialised only at the four corners, while still allowing the number of robots to vary.

### Movement Logic

The movement algorithm is a simple greedy approach. Each tick, a robot considers neighbouring cells and moves to a walkable cell that reduces the straight-line distance to the target. It never moves into a shelf cell because `_is_walkable()` rejects shelf coordinates.

This approach is suitable for the structured aisle maps used in the showcase, but it is not a full pathfinding algorithm. A more advanced solution would use breadth-first search or A* to guarantee a path in more complex maps. I kept greedy movement because it is short, understandable, and appropriate for the designed input maps. This limitation is discussed again in Future Work.

### User Interface and Configuration

The program has the two required modes. Interactive mode prompts for parameters and generates a warehouse. Batch mode uses `-f` and `-p` to load a map and parameter file. The command-line validation prevents invalid mode combinations, such as using `-i` with batch files or running batch mode without both required files.

### Visualisation and Statistics

The Matplotlib display uses two subplots. The first subplot shows the warehouse map, shelf cells, corner cells, available goods, and robot positions. The second subplot shows total deliveries over time. At the end of the simulation, the program prints ticks elapsed, total deliveries, remaining goods, throughput, and per-robot delivery counts and final states.

### UML Class Diagram

```text
+------------------+            targets / claims            +------------------+
|      Robot       | --------------------------------------> |       Good       |
+------------------+                                         +------------------+
| robot_id         |                                         | x                |
| home_x, home_y   |                                         | y                |
| x, y             |                                         | available        |
| state            |                                         | claimed_by       |
| target_good      |                                         +------------------+
| carrying         |
| deliveries       |
+------------------+
| find_nearest_good|
| claim_good       |
| step_change      |
| step_toward      |
+------------------+
```

The `Robot` class depends on `Good` because each robot may target one good. The terrain is not a class in this version; it is represented by a 2D list handled by terrain utility functions.

## Showcase

### Introduction

The showcase uses three batch-mode scenarios. They vary warehouse size, shelf layout, number of robots, number of goods, and simulation length. All scenarios are reproducible because the map files, parameter files, and random seeds are fixed.

The scenarios are designed to compare how workload and layout affect completion and throughput:

1. Scenario 1 checks a small warehouse with a moderate workload.
2. Scenario 2 checks a larger workload where some goods remain after the time limit.
3. Scenario 3 checks a larger warehouse and workload with enough time for full completion.

### Scenario 1

Command:

```bash
python3 warehouse.py -f data/map1.csv -p data/params1.csv
```

Configuration:

- Map size: 10 x 8
- Robots: 4
- Goods: 20
- Ticks: 150
- Seed: 123

Observed summary:

```text
Ticks elapsed: 150
Total deliveries: 20
Remaining goods: 0
Throughput (deliveries/tick): 0.133
```

Scenario 1 clears all goods. This confirms that the basic workflow is working: robots can find goods, move beside shelves, collect items, return home, and repeat until all goods are delivered.

### Scenario 2

Command:

```bash
python3 warehouse.py -f data/map2.csv -p data/params2.csv
```

Configuration:

- Map size: 12 x 9
- Robots: 6
- Goods: 40
- Ticks: 220
- Seed: 456

Observed summary:

```text
Ticks elapsed: 220
Total deliveries: 36
Remaining goods: 4
Throughput (deliveries/tick): 0.164
```

Scenario 2 leaves four goods undelivered. This is useful for comparison because it shows that changing workload and time limit changes the outcome. The simulation does not automatically guarantee completion; it depends on the selected parameters.

### Scenario 3

Command:

```bash
python3 warehouse.py -f data/map3.csv -p data/params3.csv
```

Configuration:

- Map size: 14 x 10
- Robots: 6
- Goods: 60
- Ticks: 250
- Seed: 321

Observed summary:

```text
Ticks elapsed: 250
Total deliveries: 60
Remaining goods: 0
Throughput (deliveries/tick): 0.240
```

Scenario 3 completes all deliveries and has the highest throughput. This demonstrates that the relationship between map size, robot count, goods count, and time limit is not linear. The wider aisle layout and available time allow the robots to process more goods overall.

### Showcase Comparison

Scenario 1 proves the baseline functionality. Scenario 2 shows that a larger workload can exceed the available simulation time. Scenario 3 shows that a larger scenario can still complete successfully when the parameters are balanced. Together, the three scenarios demonstrate that the simulation responds meaningfully to input changes.

## Conclusion

The final program provides a complete implementation of the main robotic warehouse requirements. It uses object-oriented design for robots and goods, supports multiple goods at shelf locations, implements task progression through robot states, blocks movement through shelves, provides both interactive and batch run modes, and displays realtime and summary statistics.

The v2 specification emphasises timestep behaviour driven by object methods. This is addressed through `Robot.step_change()`, which updates the robot according to its current state on each simulation tick. The functional test suite also improves confidence that the main behaviours work as intended.

The main limitation is the greedy movement algorithm. It is appropriate for the structured showcase maps, but it is not a general pathfinding solution for all possible warehouse layouts.

## Future Work

Future improvements could include:

1. Replace greedy movement with BFS or A* pathfinding.
2. Add saved output files for plots and summary statistics.
3. Add parameter sweep automation for larger experiments.
4. Add more task allocation strategies, such as assigning goods based on robot workload.
5. Add stronger validation for unreachable shelf locations.
6. Add optional collision avoidance if robot overlap is disallowed in a future version.

## References

Curtin University. 2026. "COMP5005 Assignment Robotic Warehouse Semester 1, 2026 v1.0." Assignment brief, Discipline of AI and Data Science, Curtin University.

Curtin University. 2026. "COMP1005/5005 Assignment FAQ." Blackboard FAQ notes for Fundamentals of Programming.

Matplotlib Development Team. 2026. "Matplotlib Documentation." Accessed May 21, 2026. https://matplotlib.org/stable/contents.html.

Python Software Foundation. 2026. "Python 3 Documentation." Accessed May 21, 2026. https://docs.python.org/3/.
