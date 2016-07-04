#!/usr/bin/env python3
import codecs
import getopt
import hashlib
import os
import polib
import requests
import shutil
import sys
import threading
import time


def base_encode(string):
    return codecs.encode(string.encode(), "base-64").decode()


def base_decode(string):
    return codecs.decode(string.encode(), "base-64").decode()


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
                try:
                    langs.remove(lang)
                except ValueError:
                    pass

        return langs


class downloader(threading.Thread):
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

        auth = self.sync.authentication_details()
        params = {
            "source_file_name":"{}.po".format(self.sync.base),
            "locale": lang,
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

if __name__ == "__main__":
    print("Starting up")
    # Set some defaults, prevent errors
    exclude = []
    file_path = "language_files"
    base = "en_US"
    keep = False
    rename = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["path=", "project=", "exclude=", "keep=", "base=", "rename="])
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
    print("Initializing")
    tool = sync(api_key,
                api_secret,
                file_path,
                project_id,
                base=base,
                exclude=exclude,
                keep=keep,
                rename=rename)
    print("Downloading files")
    threads = []
    print(tool.langs)
    for lang in tool.langs:
        thread = downloader(lang, tool)
        thread.start()
        threads.append(thread)
        time.sleep(0.5)

    for thread in threads:
        thread.join()

    print("Language files downloaded. Quitting app")
    sys.exit()
