import argparse

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


def create_memory_comparison_plot(tiff_file, zarr_file, output_file):
    """
    Creates a memory usage comparison plot from two mprofile .dat files.
    """
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
        plt.savefig(output_file, dpi=900)
        print(f"Memory comparison plot saved to: {output_file}")

    except FileNotFoundError as e:
        print(f"Error: A data file was not found. {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Create memory usage comparison plot from mprofile .dat files"
    )
    parser.add_argument(
        "tiff_file", help="Path to the TIFF mprofile .dat file"
    )
    parser.add_argument(
        "zarr_file", help="Path to the Zarr mprofile .dat file"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="./compared_memory_usage.png",
        help="Output file path for the plot (default: ./compared_memory_usage.png)",
    )

    args = parser.parse_args()

    success = create_memory_comparison_plot(
        args.tiff_file, args.zarr_file, args.output
    )
    if not success:
        exit(1)


if __name__ == "__main__":
    main()
