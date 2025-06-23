#!/bin/bash

# Memory Profiling and Visualization Script
# This script downloads the subject file, runs memory profiling on both load_ome_btf.py and load_as_zarr.py
# and then creates a comparison visualization

set -e  # Exit on any error

echo "Starting memory profiling workflow..."

# Download the subject file first
echo "Downloading subject file from DANDI if not already present..."
python download_subject_cli.py

# Generate timestamp for unique filenames
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Define output filenames
TIFF_DAT_FILE="tiff_mprofile_${TIMESTAMP}.dat"
ZARR_DAT_FILE="zarr_mprofile_${TIMESTAMP}.dat"

echo "Running memory profiling on load_ome_btf.py (TIFF)..."
mprof run -o "$TIFF_DAT_FILE" load_ome_btf.py

echo "Running memory profiling on load_as_zarr.py (Zarr)..."
mprof run -o "$ZARR_DAT_FILE" load_as_zarr.py

echo "Creating memory usage comparison plot..."
python visualization_cli.py "$TIFF_DAT_FILE" "$ZARR_DAT_FILE"

echo "Memory profiling workflow completed!"
echo "Generated files:"
echo "  - TIFF profile: $TIFF_DAT_FILE"
echo "  - Zarr profile: $ZARR_DAT_FILE"
echo "  - Comparison plot: ./compared_memory_usage.png" 
