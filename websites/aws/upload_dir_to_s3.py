# Function to upload files recursively under a directory to s3
import os
from argparse import ArgumentParser

import boto3
from tqdm import tqdm


def upload_files_to_s3(bucket, local_directory, prefix):
    s3 = boto3.client("s3")
    for root, _, files in os.walk(local_directory):
        for file in tqdm(
            files,
            total=len(files),
            desc=f"Uploading {os.path.basename(root)} to s3://{bucket}/{prefix}",
            unit="file",
        ):
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, local_directory)
            key = f"{prefix}{relative_path}"
            print(f"Uploading {full_path} to s3://{bucket}/{key}")
            s3.upload_file(full_path, bucket, key)
            # print(f"Uploaded: {key}")
            # print()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--target-bucket", type=str, required=True, help="target s3 bucket full path"
    )
    parser.add_argument("--local-dir", type=str, required=True, help="local directory")

    args = parser.parse_args()

    target_bucket = args.target_bucket
    # if target_bucket file scheme doesn't start with s3:// throw error
    if not target_bucket.startswith("s3://"):
        raise ValueError("Target bucket must start with s3://")
    else:
        target_bucket = target_bucket[5:]
        bucket = target_bucket.split("/")[0]
        prefix = "".join(target_bucket.split("/")[1:])

    local_dir = args.local_dir

    upload_files_to_s3(
        bucket=bucket,
        local_directory=local_dir,
        prefix=f"{prefix}/html/aws/",
    )
