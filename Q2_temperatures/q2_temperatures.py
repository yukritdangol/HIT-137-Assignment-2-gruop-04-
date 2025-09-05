import os
import pandas as pd
import numpy as np
import glob

# -------- Load and reshape --------
def load_all_data(folder="temperatures"):
    all_files = glob.glob(os.path.join(folder, "*.csv"))
    if not all_files:
        raise FileNotFoundError(f"No CSV files found in {folder}")

    df_list = []
    for file in all_files:
        df = pd.read_csv(file)

        # Expect columns: STATION_NAME, STN_ID, LAT, LON, January..December
        # Get year from filename (e.g., 2020.csv)
        year_str = os.path.splitext(os.path.basename(file))[0]
        try:
            year = int(year_str)
        except ValueError:
            year = np.nan

        # Keep relevant columns
        meta_cols = ["STATION_NAME", "STN_ID"]
        month_cols = [c for c in df.columns if c not in meta_cols and c not in ["LAT", "LON"]]

        # Melt into long format
        long_df = df.melt(id_vars=meta_cols, value_vars=month_cols,
                          var_name="Month", value_name="Temperature")

        # Add year
        long_df["Year"] = year

        # Map months to numbers
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        long_df["MonthNum"] = long_df["Month"].map(month_map)

        # Build Date column
        long_df["Date"] = pd.to_datetime(
            dict(year=long_df["Year"], month=long_df["MonthNum"], day=1),
            errors="coerce"
        )

        # Force Temperature numeric
        long_df["Temperature"] = pd.to_numeric(long_df["Temperature"], errors="coerce")

        # Rename Station col
        long_df = long_df.rename(columns={"STATION_NAME": "Station"})

        df_list.append(long_df)

    return pd.concat(df_list, ignore_index=True)

# -------- Analyses --------
def calculate_seasonal_averages(data):
    seasonal_temps = {
        'Summer': [],
        'Autumn': [],
        'Winter': [],
        'Spring': []
    }
    
    for record in data:
        month = record['month']
        temp = record['temperature']
        
        if month in [12, 1, 2]:
            seasonal_temps['Summer'].append(temp)
        elif month in [3, 4, 5]:
            seasonal_temps['Autumn'].append(temp)
        elif month in [6, 7, 8]:
            seasonal_temps['Winter'].append(temp)
        elif month in [9, 10, 11]:
            seasonal_temps['Spring'].append(temp)
    
    seasonal_averages = {}
    for season, temps in seasonal_temps.items():
        if temps:
            seasonal_averages[season] = sum(temps) / len(temps)
        else:
            seasonal_averages[season] = None
    
    with open("average_temp.txt", 'w') as f:
        for season, avg in seasonal_averages.items():
            if avg is not None:
                f.write(f"{season}: {avg:.1f}°C\n")
            else:
                f.write(f"{season}: No data\n")
    
    print("Seasonal averages saved to average_temp.txt")
    return seasonal_averages

def largest_temp_range(df):
    grouped = df.groupby("Station")["Temperature"]
    ranges = grouped.max() - grouped.min()
    max_range = ranges.max()
    stations = ranges[ranges == max_range]

    with open("Q2_temperatures/largest_temp_range_station.txt", "w") as f:
        for station, value in stations.items():
            max_temp = df[df["Station"] == station]["Temperature"].max()
            min_temp = df[df["Station"] == station]["Temperature"].min()
            f.write(f"{station}: Range {value:.1f}°C (Max: {max_temp:.1f}°C, Min: {min_temp:.1f}°C)\n")


def temperature_stability(df):
    stds = df.groupby("Station")["Temperature"].std()
    min_std = stds.min()
    max_std = stds.max()
    stable = stds[stds == min_std]
    variable = stds[stds == max_std]
    lines = []
    for st, val in stable.items():
        lines.append(f"Most Stable: {st}: StdDev {val:.1f}°C")
    for st, val in variable.items():
        lines.append(f"Most Variable: {st}: StdDev {val:.1f}°C")
    with open("Q2_temperatures/temperature_stability_stations.txt", "w") as f:
        f.write("\n".join(lines))

# -------- Main --------
if __name__ == "__main__":
    df = load_all_data("Q2_temperatures/temperatures")

    print("Loaded data sample:")
    print(df.head())

    calculate_seasonal_averages(df)
    largest_temp_range(df)
    temperature_stability(df)

    print("Analysis complete! Output files saved.")