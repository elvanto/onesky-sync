#!/usr/bin/env python3
import getopt
import hashlib
import os
import polib
import requests
import shutil
import sys
import time


class sync(object):
    """
    The object to store important stuff.
    """
    def __init__(self, api_key, api_secret, filepath, project, rename=False, base="en-US", exclude=[], keep=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.filepath = filepath
        self.project = project
        self.base = base
        self.exclude = exclude
        self.langs = self.get_languages()
        if self.filepath[-1] == "/":
            self.filepath = self.filepath[:-1]
        self.langpath = self.filepath + "/po"
        self.keep = keep
        self.rename = rename

    def authentication_details(self):
        """
        Generates the messed up Authentication details that onesky uses
        :return: Dict
        """
        ts = str(int(time.time()))
        dev_hash = hashlib.md5()
        dev_hash.update(ts.encode())
        dev_hash.update(self.api_secret.encode())
        return {"api_key":self.api_key,"timestamp":ts,"dev_hash":dev_hash.hexdigest()}

    def get_languages(self):
        """
        Gets the list of the languages for the specified project
        :return: List
        """
        url = "https://platform.api.onesky.io/1/projects/{}/languages".format(self.project)
        data = requests.get(url, params=self.authentication_details()).json()
        langs = []
        for lang in data["data"]:
            langs.append(lang["code"])
        if self.exclude:
            for lang in self.exclude:
                langs.remove(lang)

        return langs

    def download_files(self):
        """
        Downloads the .PO file of the specified language/project and saves to the chosen filepath before converting to mo
        If set not to keep, it deletes the files.
        :lang: Language code
        :return: None
        """
        if not os.path.exists(self.langpath):
            os.makedirs(self.langpath)

        url = "https://platform.api.onesky.io/1/projects/{}/translations".format(self.project)
        for lang in self.langs:
            print("Downloading {}. {} of {}".format(lang, self.langs.index(lang) + 1, len(self.langs)))
            auth = self.authentication_details()
            params = {
                "source_file_name":"{}.po".format(self.base),
                "locale": lang,
                "export_file_name": "{}.po".format(lang)
            }
            for key in auth.keys():
                params[key] = auth[key]

            data = requests.get(url, params=params).content.decode()
            if self.rename:
                po_path = "{}/{}.po".format(self.langpath, lang.replace("-", "_"))
                mo_path = "{}/{}.mo".format(self.filepath, lang.replace("-","_"))
            else:
                po_path = "{}/{}.po".format(self.langpath, lang)
                mo_path = "{}/{}.mo".format(self.filepath, lang)
            with open(po_path, "w+") as file:
                file.write(data)

            po = polib.pofile(po_path)
            print("{}.po downloaded and saved to {}, converting to MO".format(lang, po_path))
            po.save_as_mofile(mo_path)
            print("{}.mo converted and saved to {}".format(lang, mo_path))
        if not self.keep:
            print("Deleing PO files")
            shutil.rmtree(self.langpath)

        return

if __name__ == "__main__":
    """

    """
    print("Starting up!")
    # Set some defaults, prevent errors
    exclude = []
    file_path = "language_files"
    base = "en_US"
    keep = False
    rename = False
    try:
        opts, args = getopt.getopt(sys.argv[3:], "", ["path=", "project=", "exclude=", "keep=", "base=", "rename="])
        api_key = sys.argv[1]
        api_secret = sys.argv[2]
    except getopt.GetoptError:
        print(getopt.GetoptError)
        print("Usage: python sync.py api_key api_secret --project=project_id [--path=<dir> --exclude=lang_code --base= --keep=False --rename=True")
        print("E.G. python sync.py public_key secret_key --project=1234 --path=~/Desktop/language_files --exclude=en-US, --base=en_US")
        sys.exit(2)


    for opt, arg in opts:
        if opt == "--project":
            project_id = arg
        elif opt == "--path":
            file_path = arg
            if file_path[0] == "~":
                file_path = os.path.expanduser(file_path)
        elif opt == "--exclude":
            exclude.append(arg)
        elif opt == "--keep":
            keep = arg
        elif opt == "--base":
            base = arg
        elif opt == "--rename":
            rename = arg

    # TODO: Get Auth details from auth.txt
    """
    try:
        with open("auth.txt") as file:
            reader = file.readlines()
            api_key = reader[0]
            api_secret = reader[1]
    except IOError:
        api_key = input("Please enter API Key: ")
        api_secret = input("Please enter API Secret: ")
        with open("auth.txt", "w+") as file:
            file.writelines([api_key, api_secret])
    """

    # TODO: Use 2 way encryption on the auth details
    """
    https://gist.github.com/sekondus/4322469#gistcomment-1314672
    Crypto library?
    https://www.dlitz.net/software/pycrypto/
    """

    # Error if no project ID given
    if not project_id:
        print("Please specify a project id using --project=project_id")
        sys.exit(2)

    tool = sync(api_key,
                api_secret,
                file_path,
                project_id,
                base=base,
                exclude=exclude,
                keep=keep,
                rename=rename)
    tool.download_files()
