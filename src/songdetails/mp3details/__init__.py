"""
MP3 Details subpackage for :mod:`songdetails`, you should not need to use this
directly since there exists :func:`songdetails.scan`.

Dependencies
------------

 * :mod:`mpeg1audio` - http://github.com/Ciantic/mpeg1audio/
 * :mod:`pytagger` - http://github.com/scy/pytagger/
    
"""

# Pylint disable settings:
# ------------------------
# ToDos, DocStrings:
# pylint: disable-msg=W0511,W0105 
#
# Protected member access: 
# pylint: disable-msg=W0212
#
# Too many instance attributes, Too few public methods, Too many init arguments:
# pylint: disable-msg=R0902,R0903,R0913

from songdetails import SongFileDetails
from songdetails.mp3details import audio
from songdetails.mp3details import id3
from songdetails.mp3details import exceptions
from songdetails.mp3details.audio import MPEGAudioDescriptor 
from songdetails.mp3details.id3 import ID3TagDescriptor, _track_convert, \
    _genre_convert
from songdetails.mp3details.exceptions import MP3DetailsException

__all__ = ["audio", "scanners", "id3", 'scan', "MP3Details", "MP3DetailsException"]

class MP3Details(SongFileDetails):
    """MP3 details"""
    title = ID3TagDescriptor("TIT2", "TIT2", "TT2", "title")
    artist = ID3TagDescriptor("TPE1", "TPE1", "TP1", "artist")
    album = ID3TagDescriptor("TALB", "TALB", "TAL", "album")
    year = ID3TagDescriptor("TYER", "TYER", "TYE", "album", int)
    track = ID3TagDescriptor("TRCK", "TRCK", "TRK", "track", _track_convert)
    genre = ID3TagDescriptor("TCON", "TCON", "TCO", "genre", _genre_convert)
    composer = ID3TagDescriptor("TCOM", "TCOM", "TCM")
    comment = ID3TagDescriptor("COMM", "COMM", "COM")
    duration = MPEGAudioDescriptor("duration")
    
    def __init__(self, filepath):
        """__init__:
        
        :param filepath: File path to MP3.
        :type filepath: string, unicode
        
        :raise MP3DetailsException: Raised if the file is not MP3.
        
        """
        super(MP3Details, self).__init__(filepath)
        ID3TagDescriptor.initialize_owner(self, filepath)
        MPEGAudioDescriptor.initialize_owner(self, filepath)
        
    def save(self):
        """Save changes to the MP3"""
        ID3TagDescriptor.save(self)

def scan(filepath):
    """Scan files for MP3Details.
    
    :param filepath: Path to file.
    
    :rtype: :mod:`MP3Details`, or None
    
    """
    try:
        return MP3Details(filepath)
    except MP3DetailsException:
        return None