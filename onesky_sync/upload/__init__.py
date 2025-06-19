#!/usr/bin/env python3
import getopt
import json
import os
import requests
import sys

from onesky_sync.authentication import authentication_details, get_auth


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
        print("Attempting to upload file located at {0}".format(self.filepath))
        try:
            files = {'file': open(self.filepath, 'rb')}
            payload = authentication_details(self.api_key, self.api_secret)
            payload['file_format'] = self.file_type
            payload['locale'] = self.base
            payload["is_keeping_all_strings"] = self.keep
            payload["is_keeping_all_strings"] = "false"

            print("Data compiled... uploading!")
            res = requests.post(url, files=files, params=payload)
            response_json = res.json()
            print("OneSky API Response:")
            print(json.dumps(response_json, indent=4))
            
            if res.status_code == 201 and response_json.get('meta', {}).get('status') == 201:
                print("Successfully uploaded!")
            else:
                print("Upload failed with status code:", res.status_code)

            return
        except FileNotFoundError:
            print("No file located at {0} - Please give a valid file path".format(self.filepath))
            sys.exit(2)


def main(parameters):
    file_path = "language_files"
    base = "en_US"
    keep = "false"
    file_type = "GNU_PO"
    project_id = ''
    auth_file = "auth.txt"

    try:
        opts, args = getopt.getopt(parameters, "", ["path=", "project=", "format=", "keep=", "base=", "auth="])
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
        elif opt== "--auth":
            auth_file = arg

    api_key, api_secret = get_auth(auth_file)

    # Error if no project ID given
    if not project_id:
        print("Please specify a project id using --project=project_id")
        sys.exit(2)

    tool = Uploader(api_key, api_secret, file_path, project_id, file_type, base, keep)
    tool.upload()
    print("Successfully uploaded file to OneSky!")
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
