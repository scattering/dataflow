import os
from os.path import expanduser
import stat

from django.utils.crypto import get_random_string

def get_key(keyfile, keylen=50):
    """
    Read the dataflow secret key from ~/.dataflow, creating a random key if
    one does not already exist.
    """
    keyfile = expanduser(keyfile)

    # Check for keyfile, creating a new one if none exists
    if not os.path.exists(keyfile):
        if not os.path.exists(os.path.dirname(keyfile)):
            os.makedirs(os.path.dirname(keyfile),0o700)
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = get_random_string(keylen, chars)
        with os.fdopen(os.open(keyfile, os.O_WRONLY|os.O_CREAT, 0o600), 'w') as fid:
            fid.write(key)

    # Read key file, even if it was just generated, but only when the file
    # is readable only by the user.
    mode = os.stat(keyfile).st_mode
    if mode == stat.S_IRUSR|stat.S_IWUSR:
        raise IOError("Keyfile %r is readable by others"%keyfile)
    with open(keyfile) as fid:
        return fid.read().strip()
