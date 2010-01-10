"""
:mod:`mp3details.scanners`
==========================

"""
from songdetails.mp3details import MP3Details
from songdetails.mp3details.exceptions import MP3DetailsException

def scan(filepath):
    """Scan files for MP3Details.
    
    :param filepath: Path to file.
    
    :rtype: :mod:`MP3Details`, or None
    
    """
    try:
        return MP3Details(filepath)
    except MP3DetailsException:
        return None

