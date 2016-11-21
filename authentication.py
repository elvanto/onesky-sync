import time
import hashlib

def authentication_details(api_key, api_secret):
    """
    Generates the messed up Authentication details that onesky uses
    :return: Dict
    """
    ts = str(int(time.time()))
    dev_hash = hashlib.md5()
    dev_hash.update(ts.encode())
    dev_hash.update(api_secret.encode())
    return {"api_key": api_key, "timestamp": ts, "dev_hash": dev_hash.hexdigest()}
