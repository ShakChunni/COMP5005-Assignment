# COMP5005 Robotic Warehouse Simulation

## Requirements
- Python 3
- `matplotlib`

Install matplotlib if needed:

```bash
python3 -m pip install matplotlib
```

## Run Modes

Interactive mode:

```bash
python3 warehouse.py -i
```

Batch mode (sample files included):

```bash
python3 warehouse.py -f map1.csv -p params1.csv
```

## Batch File Formats

`map1.csv`
- 2D grid
- Supported cell values:
  - `shelf`, `s`, `1`, `#` -> shelf cell (blocked)
  - `corner`, `c` -> corner cell
  - anything else -> floor cell

`params1.csv`
- `key,value` rows, for example:
  - `robots,6`
  - `goods,40`
  - `ticks,250`
  - `seed,123`
  - `pause,0.02`

## Notes
- Robots spawn only at map corners.
- Robots cannot move through shelf cells.
- Multiple goods can exist at the same shelf location.
