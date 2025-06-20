from onesky_sync.sync import main as sync
from onesky_sync.json_sync import main as json_download
from onesky_sync.authentication import get_auth, authentication_details
import sys
import requests
from onesky_sync.upload import main as upload


def check_auth_status(auth_file):
    """Check if authentication with OneSky is working.
    
    Returns:
        tuple: (bool, str) - (is_success, message)
    """
    try:
        api_key, api_secret = get_auth(auth_file)
        auth_params = authentication_details(api_key, api_secret)
        response = requests.get(
            "https://platform.api.onesky.io/1/projects",
            params=auth_params,
            timeout=10
        )
        response.raise_for_status()
        return True, "✅ Authentication successful!"
    except Exception as e:
        return False, f"❌ Authentication failed: {str(e)}"


def print_help():
    """Print help information for the CLI."""
    print("""OneSky Sync CLI

Commands:
  upload       Upload translation files to OneSky
  download     Download translations from OneSky
  status       Check authentication status
  help         Show this help message

Common options:
  --auth=FILE  Path to auth file (default: auth.txt in current directory)

Use 'onesky-sync COMMAND --help' for command-specific help.
""")


def main():
    commands = ['upload', 'download', 'help', 'status', 'json_download']
    initial_error = f'Please enter a valid command: {commands}'
    
    try:
        command = sys.argv[1].lower()
        if command not in commands:
            print(initial_error)
            sys.exit(2)
    except IndexError:
        print_help()
        sys.exit(2)

    if command == 'help':
        print_help()
    elif command == 'upload':
        upload(sys.argv[2:])
    elif command == 'json_download':
        json_download(sys.argv[2:])
    elif command == 'status':
        # Extract --auth parameter if provided
        auth_file = 'auth.txt'
        for arg in sys.argv[2:]:
            if arg.startswith('--auth='):
                auth_file = arg.split('=', 1)[1]
                break
                
        success, message = check_auth_status(auth_file)
        print(message)
        sys.exit(0 if success else 1)
    else:
        sync(sys.argv[2:])
