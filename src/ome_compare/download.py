import json
from importlib import resources
from pathlib import Path
from typing import Any

import requests
from tqdm import tqdm


def download_dandi_asset(
    asset_url: str, local_filepath: Path, overwrite: bool = False
) -> None:
    """Download an asset from DANDI archive.

    Parameters
    ----------
    asset_url : str
        URL of the asset to download from DANDI archive.
    local_filepath : Path
        Local path where the asset will be saved.
    overwrite : bool, optional
        If True, overwrite existing file. If False,
        skip download if file exists.Default is False.

    Returns
    -------
    None

    Notes
    -----
    Downloads the asset in chunks with a progress bar showing download status.
    """
    if local_filepath.exists() and not overwrite:
        print(f"File {local_filepath} already exists. Skipping download")
        return

    response = requests.get(asset_url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    with open(local_filepath, "wb") as f:
        with tqdm(
            total=total_size,
            unit="iB",
            unit_scale=True,
            desc="Downloading",
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))


def download_subject_45424_dataset(
    root_dir: Path = Path("./catnip"), overwrite: bool = False
) -> None:
    """Download all datasets associated with subject 45424 from DANDI archive.

    This function reads a JSON file containing metadata about the datasets for
    subject 45424 and downloads each dataset to the local filesystem. The
    datasets are organized by metric and can be either single files or
    lists of files.

    Parameters
    ----------
    root_dir : Path
        Root directory where the datasets will be downloaded.
    overwrite : bool, optional
        If True, overwrite existing files. If False, skip download if
        the file exists.
        Default is False.

    Returns
    -------
    None

    Notes
    -----
    The function expects a JSON file named 'subject_45424.json' in the
    ome_compare.data package. The JSON file should contain a dictionary where
    each key is a metric name and each value is either a dictionary with
    'dandi_url' and 'dandi_filepath' keys, or a list of such dictionaries.
    """
    subject_filepath: Any = resources.files("ome_compare.data").joinpath(
        "subject_45424.json"
    )
    with open(subject_filepath, "r") as f:
        subject_45424 = json.load(f)
    for metric, values in subject_45424.items():
        print(f"Downloading {metric}...")
        if isinstance(values, dict):
            local_filepath: Path = root_dir.joinpath(values["dandi_filepath"])
            local_filepath.parent.mkdir(exist_ok=True, parents=True)
            download_dandi_asset(
                values["dandi_url"], local_filepath, overwrite=overwrite
            )
        elif isinstance(values, list):
            for value in values:
                local_filepath = root_dir.joinpath(value["dandi_filepath"])
                local_filepath.parent.mkdir(exist_ok=True, parents=True)
                download_dandi_asset(
                    value["dandi_url"], local_filepath, overwrite=overwrite
                )
    return None
