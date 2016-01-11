This library will download .PO files from a Onesky Project and convert them to .MO files.

## Installation

Download the library and place in a folder on your computer. Install the requirements using pip.

```
pip3 install -r requirements.txt
```

## Usage

### Downloading the .PO Files

```
python3 sync.py api_key api_secret --project=project_id
```

This will then download all the PO files and convert to MO for the specified project.

### Optional arguments

`--path` - This specifies the path to download the PO and MO files to. Defaults to a new folder called "language_files"

EG: `--path=~/Desktop/Languages` will save the file to the current users desktop


`--keep` - Specify if you wish to keep the PO files. Defaults to delete them

EG: `--keep=True` if you want to keep the PO files.


`--base` - Specify the base file name imported to Onesky. Defaults to en_US

EG: `--base=en_AU`


`--rename` - Specifies if you want to rename the files from Hyphens to Underscores.

EG: `--rename=True` will cause the script to rename the files from en-AU.mo to en_AU.mo


`--exclude` - Specify language codes that you don't want to download. If you don't want to download multiple languages, use this twice.

EG: `--exclude=en-UK --exclude=ne-BL` will not download the en-UK or ne-BL language files.
