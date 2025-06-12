# OME File Format Comparison

This project compares the performance characteristics (time and memory usage) of loading OME-TIFF (`.ome.btf`) files versus OME-ZARR files from the DANDI archive.

## Overview

The project provides tools to:

- Download OME-TIFF files from the DANDI archive
- Load and profile memory usage of OME-TIFF files
- Compare performance between OME-TIFF and OME-ZARR formats

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:

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
- `notebooks/comparison.ipynb`: Jupyter notebook containing detailed performance comparisons

To run the comparison:

1. Execute the Python scripts:

```bash
python load_ome_btf.py
python load_as_zarr.py
```

2. Open and run the comparison notebook:

```bash
jupyter notebook notebooks/comparison.ipynb
```

## Results

The comparison results are saved as:

- Memory profiles: `mprofile_*.dat` files
- Performance plots: `ome_btf_load.png` and `ome_zarr_load.png`

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

See `pyproject.toml` for complete dependency list and versions.
