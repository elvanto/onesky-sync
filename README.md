This library can download .PO files from a Onesky Project and convert them to .MO files, as well as uploading a new base .PO file for your chosen project



## Installation

Download the library and place in a folder on your computer. Install the requirements using pip.

```
pip3 install -r requirements.txt
```

## Usage

### Downloading .PO Files

#### Downloading the .PO Files

```
python3 sync.py --project=project_id
```

This will then download all the PO files and convert to MO for the specified project.

#### Optional arguments

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

### Uploading .PO Files

```
python3 upload.py --project=project_id --path=/path/to/file.po
```

This will upload the specified PO file to your project. Onesky will then process the file as-per-normal

#### Optional arguments

`--keep` - Specify if you wish to keep phrases that had been uploaded previously but aren't in the new file. Defaults to false.

EG: `--keep=true` if you want to keep phrases from previous PO file uploads

`--base` - Specify the locale for this file. If this is the same as the base language of the web-app it will upload a new base translation. If it's different it will upload translations for the specified language. Defaults to en-US

EG: `--base=en-AU` if you want the language of the chosen file to be English (Australia)

`--format` - The format of the file you're uploading. This is required by Onesky. Defaults to GNU_PO.

EG: `--format=GNU_POT` if you're uploading a new .POT file. 
