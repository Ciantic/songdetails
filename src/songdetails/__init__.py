"""
:mod:`songdetails`
==================
 
Usage example:
--------------

    >>> import songdetails
    >>> song = songdetails.scan("data/song.mp3")
    >>> if song is not None:
    ...     print song.duration
    0:03:12

Members
-------

"""
from songdetails import scanners
from songdetails.scanners import scan, scan_files
import re

__all__ = ['scanners', 'scan', 'scan_files', 'SongDetails', 'SongFileDetails']

# Pylint disable settings --------------------
#
# ToDos, DocStrings:
# pylint: disable-msg=W0511,W0105 
#
# Protected member access: 
# pylint: disable-msg=W0212
#
# Too many instance attributes, Too few public methods, Too many init arguments:
# pylint: disable-msg=R0902,R0903,R0913

class SongDetails(object):
    """Song details.
    
    Basically this represents single song, without mentioning anything about
    file type, like MP3, FLAC...
    
    .. todo::
     
        This is only fast sketch, and thus may contain too I{many or few} 
        attributes.
        
    """
    def __init__(self):
        
        self.title = None
        """Title
        
        :type: string, or None"""
        
        self.artist = None
        """Artist
        
        :type: string, or None"""
        
        self.track = None
        """Track number
        
        :type: int, or None"""
        
        self.album = None
        """Album
        
        :type: string, or None"""
        
        self.year = None
        """Year
        
        :type: int, or None"""
        
        self.published = None
        """Date of publish
        
        :type: datetime.datetime, or None"""
        
        self.recorded = None
        """Date of recording
        
        :type: datetime.datetime, or None"""
        
        self.genre = None
        """Genre
        
        :type: string, or None"""
        
        self.composer = None
        """Composer
        
        :type: string, or None"""
        
        self.comment = None
        """Comment
        
        :type: string, or None"""
        
        self.duration = None
        """Duration
        
        :type: datetime.timedelta, or None"""
        
        self.language = None
        """Language
        
        :type: string, or None""" 


class SongFileDetails(SongDetails):
    """Song File details"""
    def __init__(self, filepath):
        """
        :param filepath: File path to MP3.
        :type filepath: string
        
        """
        super(SongFileDetails, self).__init__()
        
        self.filepath = filepath
        """Path to the song file.
        
        :type: string"""
