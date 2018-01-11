import codecs
import hashlib
import time


def authentication_details(api_key, api_secret):
    """
    Generates the Auth keys needed for OneSky's API

    :param str api_key: Your API Key
    :param str api_secret: Your API Secret
    :return: dict
    """
    ts = str(int(time.time()))
    dev_hash = hashlib.md5()
    dev_hash.update(ts.encode())
    dev_hash.update(api_secret.encode())
    return {"api_key": api_key, "timestamp": ts, "dev_hash": dev_hash.hexdigest()}


def base_encode(string):
    return codecs.encode(string.encode(), "base-64").decode()


def base_decode(string):
    return codecs.decode(string.encode(), "base-64").decode()


def get_auth(auth_file):
    
    if auth_file.startswith('~'):
        auth_file = os.path.expanduser(auth_file)

    try:
        with open(auth_file) as file:
            reader = file.readlines()
            api_key = base_decode(reader[0])
            api_secret = base_decode(reader[1])
    except IOError:
        api_key = input("Please enter API Key: ")
        api_secret = input("Please enter API Secret: ")
        with open(auth_file, "w+") as file:
            file.writelines([base_encode(api_key), base_encode(api_secret)])

    return api_key, api_secret
