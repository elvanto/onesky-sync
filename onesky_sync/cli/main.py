from onesky_sync.sync import main as sync
from onesky_sync.json_sync import main as json_download
import sys
from onesky_sync.upload import main as upload


def main():
    initial_error = 'Please enter a valid command:\n\t- upload\n\t- download\n\nUse "help" for more information'
    try:
        command = sys.argv[1].lower()
        if command not in ['upload', 'download', 'help', 'json_download']:
            print(initial_error)
            sys.exit(2)
    except IndexError:
        print(initial_error)
        sys.exit(2)

    if command == 'help':
        pass
        # TODO: Add Help Text!
    elif command == 'upload':
        upload(sys.argv[2:])
    elif command == 'json_download':
        json_download(sys.argv[2:])
    else:
        sync(sys.argv[2:])
