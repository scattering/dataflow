import os
from os.path import expanduser

from django.utils.crypto import get_random_string

def get_key(keyfile):
    """
    Read the dataflow secret key from ~/.dataflow, creating a random key if
    one does not already exist.
    """
    keyfile = expanduser(keyfile)

    # Check for keyfile, creating a new one if none exists
    if not os.path.exists(keyfile):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = get_random_string(50, chars)
        with os.fdopen(os.open(keyfile, os.O_WRONLY|os.O_CREAT, 0o600), 'w') as fid:
            fid.write(key)

    # Read key file, even if it was just generated, but only when the file
    # is readable only by the user.
    stat = os.stat(keyfile)
    if stat.st_mode != (os.stat.S_IRUSR&os.stat.S_IWUSR):
        raise IOError("Keyfile %r is readable by others"%keyfile)
    with open(keyfile) as fid:
        return fid.read().strip()
