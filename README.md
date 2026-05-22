Fundamentals of Programming COMP1005/5005

## Description of warehouse.py
This directory contains the COMP5005 Robotic Warehouse assignment. The program simulates autonomous warehouse robots collecting goods from shelf locations and returning them to their home corners in a grid-based warehouse.

The implementation includes:
- `warehouse.py`, the main program entry point.
- `warehouse_app/`, the package containing configuration, terrain, model, simulation, and visualisation code.
- `data/`, sample CSV maps and parameter files for batch-mode scenarios.
- `tests/`, functional tests for the main assignment requirements.

Robots are represented as objects with their own position, home corner, state, target good, carrying status, and delivery count. Goods are represented as objects with shelf coordinates, availability, and reservation state. Shelves are blocked terrain cells, while floor and corner cells are walkable.

# Dependencies
- Python 3
- matplotlib

Install matplotlib if it is not already available:

```bash
python3 -m pip install matplotlib
```

The tests use Python's built-in `unittest` module and do not require pytest.

## How to Run
Interactive mode:

```bash
python3 warehouse.py -i
```

Batch mode:

```bash
python3 warehouse.py -f data/map1.csv -p data/params1.csv
```

Additional showcase scenarios:

```bash
python3 warehouse.py -f data/map2.csv -p data/params2.csv
python3 warehouse.py -f data/map3.csv -p data/params3.csv
```

If running in a terminal without a graphical display, use:

```bash
MPLBACKEND=Agg python3 warehouse.py -f data/map1.csv -p data/params1.csv
```

## How to Test
Run all functional tests:

```bash
python3 -m unittest discover -s tests -v
```

Run a syntax check:

```bash
python3 -m py_compile warehouse.py warehouse_app/*.py tests/*.py
```

## Batch File Format
Map files are 2D CSV grids. Supported shelf tokens are `shelf`, `s`, `1`, and `#`. Supported corner tokens are `corner` and `c`. Any other value is treated as floor.

Parameter files use `key,value` rows. Supported keys are `robots`, `goods`, `ticks`, `seed`, and `pause`.

## FAQ Notes
Reports may be submitted as either DOCX or PDF. This project includes a Word report template file for the final report.

The assignment FAQ allows other packages. This implementation uses matplotlib for plotting while keeping the warehouse-level behaviour object-oriented through the `Robot` and `Good` classes.

## Version Information
21st May, 2026 - Updated version for COMP5005 Robotic Warehouse assignment using the v2 assignment brief, functional tests, and revised report structure.
