import argparse
from pathlib import Path

from ome_compare import download_dandi_asset


def download_subject(s3_uri: str, output_path: str) -> None:
    """
    Download a subject file from DANDI archive.

    Parameters
    ----------
    s3_uri : str
        S3 URI of the asset to download from DANDI archive.
    output_path : str
        Local path where the asset will be saved.
    """
    local_filepath = Path(output_path)

    # Create parent directories if they don't exist
    local_filepath.parent.mkdir(exist_ok=True, parents=True)

    print(f"Downloading from: {s3_uri}")
    print(f"Saving to: {local_filepath}")

    try:
        download_dandi_asset(s3_uri, local_filepath)
        print(f"Successfully downloaded to: {local_filepath}")
    except Exception as e:
        print(f"Error downloading file: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Download a subject file from DANDI archive"
    )
    parser.add_argument(
        "--s3_uri",
        default="https://dandiarchive.s3.amazonaws.com/blobs/eac/fe0/eacfe09e-3a8a-4ca5-9a36-248693139199",
        help="S3 URI of the asset to download (default: subject 45424 SPIM file)",
    )
    parser.add_argument(
        "--output",
        default="./catnip/sub-45424flox/micr/sub-45424flox_sample-LeftHemisphere_SPIM.ome.btf",
        help="Output file path (default: ./catnip/sub-45424flox/micr/sub-45424flox_sample-LeftHemisphere_SPIM.ome.btf)",
    )

    args = parser.parse_args()

    try:
        download_subject(args.s3_uri, args.output)
    except Exception as e:
        print(f"Failed to download subject: {e}")
        exit(1)


if __name__ == "__main__":
    main()
