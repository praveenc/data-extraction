import json
from argparse import ArgumentParser
from pathlib import Path

import requests


def main(file_path, api_url, file_type, coordinates):
    headers = {
        "accept": "application/json",
    }

    data = {"coordinates": coordinates}

    # Create a list of file tuples
    file_data = []
    for file in Path(file_path).glob(f"*.{file_type}"):
        file_tuple = ("files", (file.name, open(file, "rb")))
        file_data.append(file_tuple)

    # Post multipart/form-data to url using requests.post
    response = requests.post(api_url, headers=headers, files=file_data, data=data)

    # Close all the file objects
    for _, (_, file_obj) in file_data:
        file_obj.close()

    json_response = response.json()

    # Write the JSON response to a file
    with open("response.json", "w") as f:
        json.dump(json_response, f, indent=4)

    print("JSON response has been written to response.json")


if __name__ == "__main__":
    parser = ArgumentParser(description="Send PDF files as multipart/form-data.")
    parser.add_argument(
        "--file_path", required=True, help="Path to the directory containing the files."
    )
    parser.add_argument(
        "--api_url", default="http://localhost:8000/general/v0/general", help="API URL."
    )
    parser.add_argument("--file_type", default="pdf", help="File type to send.")
    parser.add_argument(
        "--coordinates", default="false", help="Whether to include coordinates or not."
    )
    args = parser.parse_args()

    headers = {
        "accept": "application/json",
    }

    data = {
        "coordinates": args.coordinates,
    }

    url = args.api_url

    file_path = Path(args.file_path)
    if file_path.exists():
        file_name = file_path.stem
        file_type = args.file_type
    else:
        print(f"File {file_path} does not exist")
        raise FileNotFoundError
        exit(1)

    OUT_FILE = Path(f"./{file_name}.json")

    print(f"Extracting text from {file_path}...\n")

    # Use 'with' to ensure the file gets closed after it's been read
    with open(file_path, "rb") as f:
        file_data = {"files": f}
        # Post multipart/form-data to url using requests.post
        response = requests.post(url, headers=headers, files=file_data, data=data)

    json_response = response.json()

    OUT_FILE.write_text(json.dumps(json_response, indent=4), encoding="utf-8")
    print(f"response written to {OUT_FILE}")
