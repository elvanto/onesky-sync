#!/usr/bin/env python3
import getopt
import os
import polib
import requests
import shutil
import sys
import threading
import time

from onesky_sync.authentication import authentication_details, get_auth


class Sync(object):
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

    def get_languages(self):
        """
        Gets the list of the languages for the specified project
        :return: List
        """
        url = "https://platform.api.onesky.io/1/projects/{}/languages".format(self.project)
        data = requests.get(url, params=authentication_details(self.api_key, self.api_secret)).json()
        langs = []
        for lang in data["data"]:
            langs.append(lang["code"])
        if self.exclude:
            for lang in self.exclude:
                try:
                    langs.remove(lang)
                except ValueError:
                    pass

        return langs


class Downloader(threading.Thread):
    """
    Thread Class to perform the downloads
    Downloads the .PO file of the specified language/project and saves to the chosen filepath before converting to mo
    If set not to keep, it deletes the files.
    :lang: Language code
    :return: None
    """

    def __init__(self, lang, sync):
        threading.Thread.__init__(self)
        self.sync = sync
        self.lang = lang

    def run(self):
        if not os.path.exists(self.sync.langpath):
            os.makedirs(self.sync.langpath)

        url = "https://platform.api.onesky.io/1/projects/{}/translations".format(self.sync.project)

        auth = authentication_details(self.sync.api_key, self.sync.api_secret)
        params = {
            "source_file_name":"{}.po".format(self.sync.base),
            "locale": self.lang,
            "export_file_name": "{}.po".format(self.lang)
        }
        for key in auth.keys():
            params[key] = auth[key]

        data = requests.get(url, params=params).content.decode()

        if self.sync.rename:
            po_path = "{}/{}.po".format(self.sync.langpath, self.lang.replace("-", "_"))
            mo_path = "{}/{}.mo".format(self.sync.filepath, self.lang.replace("-","_"))
        else:
            po_path = "{}/{}.po".format(self.sync.langpath, self.lang)
            mo_path = "{}/{}.mo".format(self.sync.filepath, self.lang)

        with open(po_path, "w+") as po_file:
            po_file.write(data)

        po = polib.pofile(po_path)
        print("{}.po downloaded and saved to {}, converting to MO".format(self.lang, po_path))

        po.save_as_mofile(mo_path)
        print("{}.mo converted and saved to {}".format(self.lang, mo_path))

        if not self.sync.keep:
            print("Deleing PO files")
            shutil.rmtree(self.sync.langpath)

        return


def main(parameters):
    print("Downloading Files from OneSky")
    # Set some defaults, prevent errors
    exclude = []
    file_path = "language_files"
    base = "en_US"
    keep = False
    rename = False
    project_id = ''
    auth_file = "auth.txt"

    try:
        opts, args = getopt.getopt(parameters, "", ["path=", "project=", "exclude=", "keep=", "base=", "rename=", "auth="])
    except getopt.GetoptError:
        print(getopt.GetoptError)
        print("Usage: python sync.py --project=project_id [--path=<dir> --exclude=lang_code --base= --keep=False --rename=True")
        print("E.G. python sync.py --project=1234 --path=~/Desktop/language_files --exclude=en-US, --base=en_US")
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
        elif opt== "--auth":
            auth_file = arg

    api_key, api_secret = get_auth(auth_file)

    # Error if no project ID given
    if not project_id:
        print("Please specify a project id using --project=project_id")
        sys.exit(2)
    print("Initializing")
    tool = Sync(api_key,
                api_secret,
                file_path,
                project_id,
                base=base,
                exclude=exclude,
                keep=keep,
                rename=rename)
    print("Downloading files")
    threads = []
    for lang in tool.langs:
        thread = Downloader(lang, tool)
        thread.start()
        threads.append(thread)
        time.sleep(0.5)

    for thread in threads:
        thread.join()

    print("Language files successfully downloaded. Closing")
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
