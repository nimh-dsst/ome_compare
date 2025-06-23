import warnings
from pathlib import Path

import tifffile
import zarr
from memory_profiler import profile  # type: ignore

from ome_compare import download_dandi_asset  # type: ignore

ome_tiff_url: str = "https://dandiarchive.s3.amazonaws.com/blobs/eac/fe0/eacfe09e-3a8a-4ca5-9a36-248693139199"

local_filepath: Path = Path(
    "./catnip/sub-45424flox/micr/sub-45424flox_sample-LeftHemisphere_SPIM.ome.btf"
)
local_filepath.parent.mkdir(exist_ok=True, parents=True)
if not local_filepath.exists():
    warnings.warn(
        f"File {local_filepath} not found. Downloading from {ome_tiff_url}"
    )
    download_dandi_asset(ome_tiff_url, local_filepath)


@profile
def main():
    tiff_store = tifffile.imread(local_filepath, aszarr=True, mode="r")
    img = zarr.open(tiff_store, mode="r")
    plane = img[0, :, :]


if __name__ == "__main__":
    main()
