#!/usr/bin/env python3
import getopt
import json
import os
import requests
import sys

from authentication import authentication_details, base_encode, base_decode


class Uploader(object):
    """
    Object for uploading files
    """
    def __init__(self, api_key, api_secret, filepath, project, file_type, base, keep):
        self.api_key = api_key
        self.api_secret = api_secret
        self.filepath = filepath
        self.project = project
        self.base = base
        self.keep = keep
        self.file_type = file_type

    def upload(self):
        print("Compiling data to upload")
        url = "https://platform.api.onesky.io/1/projects/{0}/files".format(self.project)
        print("Attempting to upload file located at {0}".format(file_path))
        try:
            files = {'file': open(file_path, 'rb')}
            payload = authentication_details(api_key, api_secret)
            payload['file_format'] = self.file_type
            payload['locale'] = base
            payload["is_keeping_all_strings"] = self.keep
            payload["is_keeping_all_strings"] = "false"

            print("Data compiled... uploading!")
            res = requests.post(url, files=files, params=payload)
            if res.json()['meta']['status'] == 201:
                print("Succesfully uploaded!")
            else:
                print("Something went wrong...")
                print(json.dumps(res.json(), indent=4))

            return
        except FileNotFoundError:
            print("No file located at {0} - Please give a valid file path".format(file_path))
            sys.exit(2)


if __name__ == "__main__":
    print("Starting up")
    # Set some defaults, prevent errors
    file_path = "language_files"
    base = "en_US"
    keep = "false"
    file_type = "GNU_PO"
    project_id = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["path=", "project=", "format=", "keep=", "base="])
    except getopt.GetoptError:
        print(getopt.GetoptError)
        print("Usage: python upload.py --project=project_id --path=<dir>[--format= --base= --keep=False]")
        print("E.G. python upload.py --project=1234 --path=~/Desktop/language_files, --base=en_US")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--project":
            project_id = arg
        elif opt == "--path":
            file_path = arg
            if file_path[0] == "~":
                file_path = os.path.expanduser(file_path)
        elif opt == "--keep":
            keep = arg
        elif opt == "--base":
            base = arg
        elif opt == "--format":
            file_type = arg

    try:
        with open("auth.txt") as file:
            reader = file.readlines()
            api_key = base_decode(reader[0])
            api_secret = base_decode(reader[1])
    except IOError:
        api_key = input("Please enter API Key: ")
        api_secret = input("Please enter API Secret: ")
        with open("auth.txt", "w+") as file:
            file.writelines([base_encode(api_key), base_encode(api_secret)])

    # Error if no project ID given
    if not project_id:
        print("Please specify a project id using --project=project_id")
        sys.exit(2)

    tool = Uploader(api_key, api_secret, file_path, project_id, file_type, base, keep)
    tool.upload()
    print("Done!")
    sys.exit()
