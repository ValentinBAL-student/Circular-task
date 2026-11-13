"""Circular task analysis (MouseReMoCo): reusable functions.

Extracted from the main notebook so that other notebooks can do
`from src.circular import full_analysis` instead of copying the code.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import os


def read_header(filename):
    # Return the task parameters of the first line as a dictionary
    with open(filename) as f:
        first_line = f.readline().strip() # Read the first line and strip whitespace
    header = {}
    for item in first_line.split(";"): # Split the line by semicolon to get key-value combinations
        key, value = item.split(" ", 1)# Split each combination into key and value (only at the first space)
        # Try to convert the value to a float, if it fails, keep it as a string
        try:
            value = float(value)
        except ValueError:
            pass  # keep text values (colors, software name...) as strings
        header[key] = value
    return header


def read_markers(filename):
    # Return the list of timestamp_ms, message and the list of the summary table lines
    with open(filename) as f:
        lines = f.read().splitlines()
    markers, table_lines = [], []
    for line in lines[3:]:  # skip header, date and empty line
        parts = line.split(",", 2)# Split the line into parts (timestamp, message, and the rest)
        if len(parts) == 3 and parts[1].strip().isdigit():#if it's a marker line, append the timestamp and message to the markers list otherwise, if it's a summary table line, append it to the table_lines list
            markers.append((int(parts[1]), parts[2]))
        elif line.strip() != "":
            table_lines.append(line)
    return markers, table_lines


def get_record_times(markers):
    # Return an array (n_records, 2) with [start, end] timestamps (ms) of each record
    times = []
    for i, (ts, msg) in enumerate(markers): # enumerate over the markers to get the index and the (timestamp, message) 
        if "DoRecord" in msg and i + 1 < len(markers): # check if the message contains "DoRecord" and if there is a next marker then stock the start timestamp and the next marker's timestamp as the end timestamp to isolate a record
            times.append([ts, markers[i + 1][0]])
    return np.array(times, dtype=np.int64)


def read_data(filename,header):
        # Return t (s), x, y (pixels, centred, y up), inside (bool), timestamps (ms)
        
    with open(filename) as f:
        lines = f.read().splitlines() # read all lines of the file
    i_names = next(i for i, line in enumerate(lines) if line.startswith("timestamp")) # find the index of the line that starts with "timestamp" (the column names)
    names = lines[i_names].split(",") #then split the line by comma to get the column names in the timestamp line 
    data = np.loadtxt(filename, delimiter=",", skiprows=i_names + 1) # load the data as a numpy array, skipping the header lines
    data = data[data[:, names.index("timestamp")] > 0]  # remove the "0,0,0,0" separator lines by keeping only the rows where the timestamp is greater than 0
    timestamps = data[:, names.index("timestamp")].astype(np.int64) #as time stamps can be very large, we need to use int64 to avoid overflow

# get x and y coordinates relative to the center of the target (pixels)
    x = data[:, names.index("mouseX")] - header["centerX"] # compute the mouse x coordinate relative to the center of the target by doing mouseX - centerX
    y = header["centerY"] - data[:, names.index("mouseY")] #same for Y
    inside = data[:, names.index("mouseInTarget")] == 1 # As defined in documentation, 1 mean inside the target, 0 means outside. So we can create a boolean array where True means inside and False means outside by checking if mouseInTarget is equal to 1
    t = (timestamps - timestamps[0]) / 1000 #define the time vector in seconds, relative to the first timestamp
    return t, x, y, inside, timestamps


def plot_raw_timeseries(t, x, y, record_times, t0):
    fig, ax = plt.subplots(figsize=(20, 6))#def the figure size
    ax.plot(t, x, ".", label="x position")# plot the x(mouse) position by time 
    ax.plot(t, y, ".", label="y position")# plot the y(mouse) position by time + name

    # we set a line for each record start and end, with a different color and a label for the first one
    for i, (start, end) in enumerate(record_times): 
        ax.axvline((start - t0) / 1000, color="k", linestyle="--", label="record start" if i == 0 else None) #at start time(DoRecord in data file) add a vertical line 
        ax.axvline((end - t0) / 1000, color="r", linestyle="--", label="record end" if i == 0 else None) #at start time(DoRecord in data file) add a vertical line 
     # set the labels and title of the plot   
    ax.set_xlabel("Time(seconds)")
    ax.set_ylabel("Value")
    ax.set_title("Raw time series data")
    ax.legend()
    plt.show()


def plot_raw_trajectory(t, x, y, inside, header):
    #Call the function with the x and y coordinates,array indicating if  mouse is inside the target, and the task parameters 
    #return a plot of the trajectory with the target area and the points inside the target highlighted
    # Input:
    #   x: array of x coordinates
    #   y: array of y coordinates
    #   inside: boolean array indicating if the mouse is inside the target
    #   header: dictionary containing the task parameters
    # Output:
    #   None (displays the plot)
    R, T = header["taskRadius"], header["taskTolerance"]
    fig, ax = plt.subplots(figsize=(8, 6))
    # plot the trajectory as a line plot, with the points inside the target highlighted in green
    #adding pause between each record to visualize the trajectory better
    pause = np.where(np.diff(t) > 1.0)[0] + 1
    x_nan = np.insert(x.astype(float), pause, np.nan)
    y_nan = np.insert(y.astype(float), pause, np.nan)
    ax.plot(x_nan, y_nan, label="trajectory")
    ax.plot(x[inside], y[inside], "go", label="inside target")
    #use the Circle patch to draw the target area, with a radius of R + T/2, centered at (0,0)
    ax.add_patch(Circle((0, 0), R + T / 2, fill=False, edgecolor="r", label="target"))
    # draw the inner circle, with a radius of R - T/2, centered at (0,0)
    ax.add_patch(Circle((0, 0), R - T / 2, fill=False, edgecolor="r"))
    ax.set_xlabel("x position")
    ax.set_ylabel("y position")
    ax.set_title("Raw trajectory data")
    ax.legend()
    plt.show()


def split_records(t, x, y, inside, timestamps, record_times):
    # Return a list of records, each record is a dictionary with keys "t", "x", "y", "inside"
    records = [] #list to store the records
    for start, end in record_times: 
        #By using the record times, isolate the data for each record by creating a boolean mask that selects the samples within the start and end timestamps.
        #We then append a dictionary containing the time, x, y, and inside arrays for each record to the records list.
        m = (timestamps >= start) & (timestamps <= end)
        records.append({"t": t[m], "x": x[m], "y": y[m], "inside": inside[m]})
    return records


def compute_stats(r, header):
    R, T = header["taskRadius"], header["taskTolerance"]  # get nominal radius R and tolerance T from header
    first_in = np.argmax(r["inside"])  # find index of first sample where cursor is inside the target

    # trim all arrays to start from first inside sample (skip the approach movement)
    t, x, y, inside = r["t"][first_in:], r["x"][first_in:], r["y"][first_in:], r["inside"][first_in:]
    radius = np.sqrt(x**2 + y**2)  # compute polar radius: distance from centre for each sample
    theta = np.unwrap(np.arctan2(y, x))  # continuous angle — unwrap removes ±π jumps so laps are counted correctly
    d_theta = np.abs(np.diff(theta))  # angular step between consecutive samples (used for error and nLaps)
    n_laps = (theta[-1] - theta[0]) / (2 * np.pi)  # total angle divided by 2π (negative = clockwise)
    Re = np.mean(radius)  # effective radius: mean distance from centre over the whole record
    Te = 4.133 * np.std(radius)  # effective tolerance: 4.133 × SD of radius (target of this width is missed 3.88% of the time)
    error = 100 * np.sum(d_theta[~inside[1:]]) / np.sum(d_theta)  # % of angular travel where cursor was outside target
    MT = (t[-1] - t[0]) / abs(n_laps)  # movement time per lap: total duration divided by number of laps
    IDe = 2 * np.pi * Re / Te  # effective index of difficulty per lap (bits) using Fitts' law
    return {"nLaps": n_laps, "Re": Re, "Te": Te, "error": error,
            "MT/lap": MT, "IDe/lap": IDe, "Be": Te / T, "IPe": IDe / MT}


def theory_error():
    z = np.linspace(-4.133 / 2, 4.133 / 2, 200001)  # 200001 points between -2.066 and +2.066 SD
    pdf = np.exp(-z**2 / 2) / np.sqrt(2 * np.pi)  # standard normal distribution value at each point
    return 100 * (1 - np.sum(pdf) * (z[1] - z[0]))


def print_stats_table(all_stats, header):
    print("   Var , nLaps ,      Re ,      Te ,   error ,  MT/lap , IDe/lap ,      Be ,     IPe ,")  # column names
    print("  unit ,   lap ,   pixel ,   pixel ,       % ,   s/lap , bit/lap ,  double ,   bit/s ,")  # units row
    print(f"Theory , {1:5.2f} , {header['taskRadius']:7.2f} , {header['taskTolerance']:7.2f} , "
          f"{theory_error():7.2f} ,         ,         , {1:7.2f} ,         ,")  # theory line using nominal R and T
    for i, s in enumerate(all_stats):  # one row per record
        print(f"Rec{i + 1:03d} , {s['nLaps']:5.2f} , {s['Re']:7.2f} , {s['Te']:7.2f} , {s['error']:7.2f} , "
              f"{s['MT/lap']:7.2f} , {s['IDe/lap']:7.2f} , {s['Be']:7.2f} , {s['IPe']:7.2f} ,")


def compare_with_file(all_stats, table_lines):
    keys = ["nLaps", "Re", "Te", "error", "MT/lap", "IDe/lap", "Be", "IPe"]  # list of metric names to compare
    print("difference (ours - MouseReMoCo):")
    print("   Var ," + ",".join(f"{k:>8} " for k in keys))  # print column headers
    rec_lines = [line for line in table_lines if line.strip().startswith("Rec")]  # keep only Rec001, Rec002... lines
    for i, s in enumerate(all_stats):  # loop over each record
        values = [float(v) for v in rec_lines[i].split(",")[1:9]]  # extract the 8 numeric values from the Rec line
        print(f"Rec{i + 1:03d} ," + ",".join(f"{s[k] - v:8.2f} " for k, v in zip(keys, values)))


def plot_record_trajectory(r, header, title):
    R, T = header["taskRadius"], header["taskTolerance"]  # get nominal radius and tolerance from header
    left, top = -header["centerX"], header["centerY"]  # compute screen corner position in centred coordinates
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.add_patch(Rectangle((left, top - header["screenHeight"]), header["screenWidth"], header["screenHeight"],
                           fill=False, edgecolor="magenta", label="screen"))  # draw the screen boundary in magenta
    ax.add_patch(Circle((0, 0), R + T / 2, color="yellow", label="target"))  # draw outer circle of target in yellow
    ax.add_patch(Circle((0, 0), R - T / 2, color="white"))  # cover inner part with white to create the ring shape
    ins = r["inside"]
    ax.plot(r["x"][ins], r["y"][ins], ".", color="green", markersize=2, label="inside")  # plot points inside target in green
    ax.plot(r["x"][~ins], r["y"][~ins], ".", color="red", markersize=4, label="outside")  # plot points outside target in red
    ax.set_aspect("equal")  # equal aspect ratio so the ring appears as a circle not an ellipse
    ax.set_xlabel("X (pixels)")
    ax.set_ylabel("Y (pixels)")
    ax.set_title(title)
    ax.legend(loc="upper right")
    plt.show()


def plot_record_timeseries(r):
    fig, axes = plt.subplots(3, 1, figsize=(8, 6), sharex=True)  # 3 subplots sharing the same x axis
    axes[0].plot(r["t"], r["x"], ".-", color="blue", linewidth=0.2, label="x")  # plot x position over time
    axes[0].set_ylabel("X position")
    axes[1].plot(r["t"], r["y"], ".-", color="orange", linewidth=0.2, label="y")  # plot y position over time
    axes[1].set_ylabel("Y position")
    axes[2].plot(r["t"], r["inside"].astype(int), ".-", color="green", linewidth=0.2, label="is_inside")  # plot inside/outside as 0 or 1
    axes[2].set_ylabel("Is Inside")
    axes[2].set_xlabel("Time (s)")
    for ax in axes:
        ax.grid(True)  # add grid to each subplot for readability
        ax.legend()
    plt.tight_layout()
    plt.show()


def full_analysis(data_file, marker_file, show_plots=True):
    header = read_header(data_file)  # read task parameters from header
    markers, table_lines = read_markers(marker_file)  # read markers and summary table
    record_times = get_record_times(markers)  # get start and end time of each record
    t, x, y, inside, timestamps = read_data(data_file, header)  # read and process raw data
    records = split_records(t, x, y, inside, timestamps, record_times)  # cut data into records
    print(f"{data_file}: {len(records)} records")
    if show_plots:
        plot_raw_timeseries(t, x, y, record_times, timestamps[0])  # plot raw time series
        plot_raw_trajectory(t, x, y, inside, header)  # plot raw trajectory
    all_stats = [compute_stats(r, header) for r in records]  # compute stats for each record
    print("recomputed statistics:")
    print_stats_table(all_stats, header)  # print the stats table
    if show_plots:
        for i, r in enumerate(records):  # plot trajectory and timeseries for each record
            plot_record_trajectory(r, header, f"record {i}")
            plot_record_timeseries(r)
    return all_stats  # lets another notebook reuse the results
