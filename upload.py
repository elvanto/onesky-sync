#!/usr/bin/env python3
import codecs
import getopt
import hashlib
import os
import requests
import sys
import time

import json

def base_encode(string):
    return codecs.encode(string.encode(), "base-64").decode()


def base_decode(string):
    return codecs.decode(string.encode(), "base-64").decode()


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

    def authentication_details(self):
        """
        Generates the Authentication details that onesky uses
        :return: Dict
        """
        ts = str(int(time.time()))
        dev_hash = hashlib.md5()
        dev_hash.update(ts.encode())
        dev_hash.update(self.api_secret.encode())
        return {"api_key":self.api_key,"timestamp":ts,"dev_hash":dev_hash.hexdigest()}

    def upload(self):
        print("Compiling data to upload")
        url = "https://platform.api.onesky.io/1/projects/{0}/files".format(self.project)
        files = {'file': open(file_path, 'rb')}
        payload = self.authentication_details()
        payload['file_format'] = self.file_type
        payload['locale'] = base
        payload["is_keeping_all_strings"] = self.keep
        payload["is_keeping_all_strings"] = "false"

        """res = {
            "url": url,
            "file": file_path,
            "params": payload
        }"""
        print("Data compiled... uploading!")
        res = requests.post(url, files=files, params=payload)
        if res['meta']['status'] == 201:
            print("Succesfully uploaded!")
        else:
            print("Something went wrong...")
            print(json.dumps(res.json(), indent=4))

        return


if __name__ == "__main__":
    print("Starting up")
    # Set some defaults, prevent errors
    exclude = []
    file_path = "language_files"
    base = "en-US"
    keep = "false"
    file_type = "GNU_PO"

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
