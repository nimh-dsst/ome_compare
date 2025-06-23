# OME File Format Comparison

This project compares the performance characteristics (time and memory usage) of loading OME-TIFF (`.ome.btf`) files versus OME-ZARR files from the DANDI archive.

## Overview

The project provides tools to:

- Download OME-TIFF files from the DANDI archive
- Load and profile memory usage of OME-TIFF files
- Compare performance between OME-TIFF and OME-ZARR formats

## Setup

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

### Install dependencies

Using pip:

```bash
# Install main dependencies
pip install -e .

# Install development dependencies (optional)
pip install -e ".[dev]"
```

Or using UV (recommended for faster installation):

```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install main dependencies
uv pip install -e .

# Install development dependencies (optional)
uv pip install -e ".[dev]"
```

Development dependencies include:

- ipython (≥9.3.0)
- ruff (≥0.4.4)
- types-requests (≥2.32.4.20250611)
- types-tqdm (≥4.67.0.20250516)

## Usage

The project includes several key components:

- `load_ome_btf.py`: Script to download and load OME-TIFF files from DANDI
- `load_as_zarr.py`: Script to load files in ZARR format
- `download_subject_cli.py`: CLI tool for downloading individual subject files from DANDI
- `visualization_cli.py`: CLI tool for creating memory usage comparison plots
- `run_memory_profiling.sh`: Automated bash script for memory profiling workflow
- `notebooks/comparison.ipynb`: Jupyter notebook containing detailed performance comparisons

### Downloading Subject Files

To download individual subject files from DANDI archive:

```bash
# Download with default settings (subject 45424 SPIM file)
python download_subject_cli.py

# Download with custom S3 URI and output path
python download_subject_cli.py --s3_uri "https://dandiarchive.s3.amazonaws.com/blobs/your-blob-id" --output "./my_data/subject.ome.btf"

# Download to a custom location with default S3 URI
python download_subject_cli.py --output "./custom/path/subject.ome.btf"
```

### Automated Memory Profiling Workflow

The easiest way to run the complete memory profiling comparison is using the provided bash script:

```bash
./run_memory_profiling.sh
```

This script will:

1. **Download the subject file** from DANDI archive (if not already present)
2. Run memory profiling on `load_ome_btf.py` (TIFF loading)
3. Run memory profiling on `load_as_zarr.py` (Zarr loading)
4. Generate a comparison plot saved as `./compared_memory_usage.png`

**Note**: The script automatically downloads the required OME-TIFF file from DANDI archive before running memory profiling. This ensures the data is available and prevents profiling errors due to missing files. The download step uses the default settings from `download_subject_cli.py`.

### Manual Usage

To run the comparison manually:

1. Execute the Python scripts with memory profiling:

    ```bash
    mprof run -o tiff_profile.dat load_ome_btf.py
    mprof run -o zarr_profile.dat load_as_zarr.py
    ```

2. Create the comparison visualization:

    ```bash
    python visualization_cli.py tiff_profile.dat zarr_profile.dat
    ```

3. Or specify a custom output file:

    ```bash
    python visualization_cli.py tiff_profile.dat zarr_profile.dat --output my_comparison.png
    ```

### CLI Tool Options

The `visualization_cli.py` script accepts the following arguments:

```bash
python visualization_cli.py --help
```

- `tiff_file`: Path to the TIFF mprofile .dat file (required)
- `zarr_file`: Path to the Zarr mprofile .dat file (required)
- `--output`, `-o`: Output file path for the plot (default: `./compared_memory_usage.png`)

The `download_subject_cli.py` script accepts the following arguments:

```bash
python download_subject_cli.py --help
```

- `--s3_uri`: S3 URI of the asset to download (default: subject 45424 SPIM file)
- `--output`: Output file path (default: `./catnip/sub-45424flox/micr/sub-45424flox_sample-LeftHemisphere_SPIM.ome.btf`)

### Jupyter Notebook Analysis

For detailed analysis, open and run the comparison notebook:

```bash
jupyter notebook notebooks/comparison.ipynb
```

## Results

The comparison results are saved as:

- Memory profiles: `mprofile_*.dat` files (timestamped when using the bash script)
- Performance plots: `ome_btf_load.png`, `ome_zarr_load.png`, and `compared_memory_usage.png`

## Dependencies

Main dependencies:

- tifffile
- memory_profiler
- dandi
- zarr
- fsspec
- jupyter
- matplotlib
- requests
- s3fs
- tqdm
- pandas
- seaborn

See `pyproject.toml` for complete dependency list and versions.
