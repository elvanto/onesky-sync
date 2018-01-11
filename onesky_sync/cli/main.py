from onesky_sync.sync import main as sync
import sys
from onesky_sync.upload import main as upload


def main():
    initial_error = 'Please enter a valid command:\n\t- upload\n\t- download\n\nUse "help" for more information'
    try:
        command = sys.argv[1].lower()
        if command not in ['upload', 'download', 'help']:
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
    else:
        sync(sys.argv[2:])
