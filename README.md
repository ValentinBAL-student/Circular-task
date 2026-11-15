# Circular Task Analysis

A Python-based analysis of the MouseReMoCo circular steering task, as described in [Fauviaux et al. (2021)]https://hal.science/hal-03834500.

## Overview

This project reproduces the graphical outputs and statistical table from a circular task recording, then runs the same analysis on a new recording made by a team member. The analysis covers:

- Reading and parsing MouseReMoCo `.csv` and `.marker.csv` files
- Splitting raw data into individual records using marker timestamps
- Computing polar-coordinate statistics (radius, angle, effective tolerance)
- Calculating Fitts' Law metrics: effective index of difficulty (IDe), movement time per lap (MT/lap), and information throughput (IPe)
- Producing time-series and trajectory plots for each record
- Comparison of the values provided in the marker files
- Analysis of own recorded movement data

## Repository Structure

```
Circular-task/
├── data/
│   ├── 001MoDe_R1.csv              # Provided reference recording 
│   ├── 001MoDe_R1.marker.csv        
│   ├── tub_data.csv               # Team member's own recording
│   └── tub_marker.csv             
├── src/
│   └── circular.py              # contains reuseable functions
├── Circular_Task_MainNotebook.ipynb  # Main analysis notebook
├── Comparative_analysis.ipynb        # Comparison of provided and recorded data
└── README.md
```

## Requirements

No external packages are required beyond the Python standard scientific stack:

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import os
```

> **Note:** The notebook uses `%matplotlib widget` for interactive zooming. Install `ipympl` if needed:  
> conda install -c conda-forge ipympl

## How to Run

1. Clone this repository.
git clone https://github.com/ValentinBAL-student/Circular-task.git 
2. Open `Circular_Task_MainNotebook.ipynb` in Jupyter.
3. Run all cells in order.

The notebook will:
- Reproduce the expected plots and statistics table for `001MoDe_R1.csv`
- Run the full analysis on `tub_data.csv` (team member's own recording)

## Key Concepts

| Symbol | Meaning |
|--------|---------|
| R, T | Nominal task radius and tolerance (from header) |
| Re | Effective radius — mean distance from centre |
| Te | Effective width — `4.133 × SD(radius)` |
| IDe | Effective index of difficulty — `2π × Re / Te` (bits/lap) |
| MT/lap | Movement time per lap |
| IPe | Information throughput — `IDe / MT` (bits/s) |
| Be | Accuracy ratio — `Te / T` |

## Team

- Tuba
- Valentin Balbine

This project was completed collaboratively by the members of the group.
The repository uses GitHub branches and commits to organise and track contributions made during the development of the project.


## Branching Structure

The project was developed using a branch-based workflow to organise the work of the different contributors and to avoid directly modifying the `main` branch.

| Branch Name | Description |
|---|---|
| `main` | Contains the final integrated version of the project after merging completed work from the other branches. |
| `1.-Data-processing-and-graph` | Contains the initial data processing, trajectory analysis, and graph/visualisation work. |
| `Recomputed_summarytable` | Contains the recomputation of movement statistics, the summary statistics table, and comparison with the marker file values. |
| `Tuba_data_analysis` | Contains the analysis of the MouseReMoCo data recorded for the project. |
| `Final-analysis` | Contains the final integrated analysis and modifications before merging the completed work into `main`. |
| `README` | Contains README file with brief project description. |

