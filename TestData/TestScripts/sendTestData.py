# Sends json files to the server and records the responses

import requests
import os
import json
from contextlib import ExitStack


def send_files(file_paths):
    url = "http://localhost:8000/process-batch"
    responses = []

    with ExitStack() as stack:
        files = []
        for file_path in file_paths:
            f = stack.enter_context(open(file_path, "rb"))
            files.append(
                ("files", (os.path.basename(file_path), f, "application/json")))

        response = requests.post(url, files=files)

    if response.status_code == 200:
        responses.append(response.json())
    else:
        responses.append({
            "error": f"Failed to process batch ({response.status_code}): {response.text}"
        })
    return responses


if __name__ == "__main__":
   # open a file dialog to select multiple json files
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    test_files = filedialog.askopenfilenames(
        title="Select JSON files", filetypes=[("JSON files", "*.json")])
    responses = []
    if test_files:
        responses = send_files(test_files)

    # save responses to a json file

    with open("test_responses.json", "w") as f:
        json.dump(responses, f)
