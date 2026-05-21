# COMP5005 Robotic Warehouse Simulation

## Project Structure

```text
.
├── warehouse.py
├── warehouse_app/
│   ├── __init__.py
│   ├── config.py
│   ├── constants.py
│   ├── models.py
│   ├── simulation.py
│   ├── terrain.py
│   └── visualisation.py
├── data/
│   ├── map1.csv
│   ├── map2.csv
│   ├── map3.csv
│   ├── params1.csv
│   ├── params2.csv
│   └── params3.csv
├── REPORT_TEXT.md
└── FOP 2026 Sem 1 Assignment.pdf
```

## Requirements

- Python 3
- `matplotlib`

Install the dependency if needed:

```bash
python3 -m pip install matplotlib
```

## Run Modes

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

## Batch File Formats

Map files:

- 2D CSV grid
- supported shelf tokens: `shelf`, `s`, `1`, `#`
- supported corner tokens: `corner`, `c`
- anything else is treated as floor

Parameter files:

- `key,value` rows
- supported keys: `robots`, `goods`, `ticks`, `seed`, `pause`

## Notes

- Robots spawn only at map corners.
- Robots cannot move through shelf cells.
- Multiple goods can exist at the same shelf location.
- The sample data in `data/` is structured to keep shelf locations reachable.
