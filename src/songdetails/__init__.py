"""
:mod:`songdetails`
==================

Dependencies
------------

 * :mod:`mpeg1audio` - http://github.com/Ciantic/mpeg1audio/
 * :mod:`pytagger` - http://github.com/scy/pytagger/

Members
-------

"""
from mpeg1audio import MPEGAudio, MPEGAudioHeaderException
import re

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

SCANNERS = []
"""Scanners registered."""

MULTI_SCANNERS = []
"""Multi scanners registered."""

def register_file_scan(scan_function, extension_matches=None, 
                       custom_matcher=None):
    """Register single file scanner.
    
    :param scan_function: Scan function returning SongDetails.
    :param extension_matches: Match files by extension, for example 
        ``("mp3", "mp2", "mp1")``.
    :param custom_matcher: Match files by custom function.
    
    """
    def extension_matcher(filepath): #IGNROE:C0111
        for ext in extension_matches:
            if filepath.endswith(ext):
                return True
        return False
    
    filepath_matcher = custom_matcher or extension_matcher
    SCANNERS.append((scan_function, filepath_matcher))

def register_multifile_scan(multiscan_function, files_matcher):
    """Register multi file scanner.
    
    :param scan_function: Scan function returning SongDetails from list of 
        files.
    :param files_matcher: Function returning True for list of files that match
        or False for files that doesn't match.
        
    """
    MULTI_SCANNERS.append((multiscan_function, files_matcher))

def scan(files):
    """Scan files for SongDetails.
    
    :param files: List of files to be scanned.
    :type files: [string, ...]
    
    :rtype: [:mod:`SongDetails`, ...]
    :return: List of SongDetails found, list maybe empty if nothing is found.
    
    """
    import mp3details
    
    songdetails = []
    for multiscan_function, files_matcher in MULTI_SCANNERS:
        if files_matcher(files):
            songdetails.append(multiscan_function(files))
            
    for file in files:
        for scan_function, filepath_matcher in SCANNERS:
            if filepath_matcher(file):
                song = scan_function(file)
                if song is not None:
                    songdetails.append(song)
    return songdetails
    

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
        """Path to the MP3 file.
        
        :type: string"""

