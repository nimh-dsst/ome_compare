import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_mprofile_dat(filepath):
    """
    Parses a memory-profiler .dat file and returns a pandas DataFrame.
    """
    timestamps = []
    memory_usage = []
    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("MEM"):
                parts = line.split()
                timestamps.append(float(parts[2]))
                memory_usage.append(float(parts[1]) / 1024)

    df = pd.DataFrame({"timestamp": timestamps, "memory_gb": memory_usage})

    # Convert timestamps to elapsed time in seconds
    df["elapsed_time_s"] = df["timestamp"] - df["timestamp"].min()
    return df


if __name__ == "__main__":
    tiff_file = "tiff_mprofile_20250616163143.dat"
    zarr_file = "zarr_mprofile_20250616163103.dat"

    # Load the data
    try:
        # Load both datasets
        tiff_df = load_mprofile_dat(tiff_file)
        zarr_df = load_mprofile_dat(zarr_file)

        # Create the plot using seaborn
        plt.figure(figsize=(10, 6), tight_layout=True)
        sns.lineplot(
            x="elapsed_time_s",
            y="memory_gb",
            data=tiff_df,
            label="Numpy",
            color="#f4b26b",
            linewidth=6,
        )
        sns.lineplot(
            x="elapsed_time_s",
            y="memory_gb",
            data=zarr_df,
            label="Zarr",
            color="#e06666",
            linewidth=6,
        )

        # Customize the plot
        plt.rcParams.update({"font.size": 24})
        plt.title("Loading Single Plane of OME-TIFF")
        plt.xlabel("Elapsed Time (s)", fontsize=16)
        plt.ylabel("Memory Usage (GB)", fontsize=16)
        plt.grid(True)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.legend()
        plt.savefig("memory_usage.png", dpi=900)

    except FileNotFoundError as e:
        print(f"Error: A data file was not found. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
