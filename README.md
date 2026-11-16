# Circular Task Analysis

## Introduction: What is this Experiment & Why Does It Matter?

### The Task: A Continuous Steering Challenge
Imagine driving a car at high speed inside a narrow circular racetrack:
- Participants use a standard computer mouse to steer a circular cursor around a track bounded by two concentric circles.
- The goal is simple yet challenging: **rotate as fast as possible while keeping the cursor strictly within the track boundaries to avoid errors**.
- The experiment is structured into alternating timed blocks (e.g., 20 seconds of continuous steering followed by 20 seconds of rest), repeated over multiple cycles.

### What is Being Tested Scientifically?
In Human Movement Science (HMS), this paradigm evaluates several fundamental principles of motor control:

1. **Continuous Sensorimotor Integration (The Visual-Motor Loop)**:
   Unlike discrete pointing tasks (like clicking an icon), circular steering demands continuous, real-time control. The eyes track the cursor's deviation, the brain computes trajectory corrections, and the hand makes musculoskeletal adjustments multiple times per second.

2. **Speed-Accuracy Trade-off (The Steering Law)**:
   An extension of Fitts' Law, the Accot-Zhai Steering Law posits that moving faster naturally increases trajectory dispersion (variability). Participants must dynamically locate their optimal operating threshold between rotational speed and boundary avoidance.

3. **Neural Information Throughput ($IPe$)**:
   By measuring both spatial precision (effective tolerance $Te$) and rotational time ($MT$), the task models the human motor system as an information channel. The ultimate metric, **$IPe$ (bits/second)**, quantifies the brain's information processing bandwidth during continuous manual control.

### Why Does It Matter?
Originally investigated by [Fauviaux et al. (2021)](https://hal.science/hal-03834500), this task is primarily used in **neurorehabilitation** (e.g., assessing motor impairment and functional recovery in stroke patients) and **Human-Computer Interaction (HCI)** to benchmark input devices and human tracking limits.

## Overview

This project reproduces the graphical outputs and statistical table from a circular task recording, then runs the same analysis on a new recording made by a team member. The analysis covers:

- Reading and parsing MouseReMoCo `.csv` and `.marker.csv` files without external data manipulation libraries (pure Python & NumPy)
- Splitting raw data into individual records using marker timestamps
- Computing polar-coordinate statistics (radius, angle, effective tolerance)
- Calculating Fitts' Law metrics: effective index of difficulty (IDe), movement time per lap (MT/lap), and information throughput (IPe)
- Producing time-series and trajectory plots for each record
- Comparison of recomputed values with reference values provided in marker files
- Normalized cross-session comparison between reference and newly recorded movement data
- Extended kinematic analysis (empirical radius distribution vs. Gaussian fit, and directional tangential speed profiles)

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
3. Run `Circular_Task_MainNotebook.ipynb` to inspect the base reproduction and verification against the reference table.
4. Run `Comparative_analysis.ipynb` to view:
   - The normalized cross-subject comparison (Prof vs. Tub)
   - The longitudinal evolution of throughput (IPe)
   - The extended kinematic exploration (radius normality check and angular speed profiles)

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
- Jiangbin Long

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
| `feat/kinematics-analysis` | Contains the extended kinematic analysis (radius normality fit and tangential speed modulation across sectors). |
| `README` | Contains README file with brief project description. |

