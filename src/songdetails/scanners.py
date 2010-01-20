"""
Song detail scanner system.
"""
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

_SCANNERS = []
"""Scanners registered."""

_MULTI_SCANNERS = []
"""Multi scanners registered."""

_HAS_DEFAULTS = False
"""Has default scanners set already?"""

def register_file_scan(scan_function, extension_matches=None, 
                       custom_matcher=None):
    """Register single file scanner.
    
    :param scan_function: Scan function returning SongDetails.
    :param extension_matches: Match files by extension, for example 
        ``("mp3", "mp2", "mp1")``.
    :param custom_matcher: Match files by custom function, custom function gets
        only filepaths or urls as argument and should return :const:`True` or
        :const:`False`.
        
        .. note::
            
            Custom matcher should never assume that it can open the file given
            in argument, it should only try to roughly match using the string
            only!
            
            Reason is that custom_matcher may be given URL's, for instance when
            registered scanner handles file objects retrieved behind URL.
    
    """
    def extension_matcher(filepath):
        """Match by given extensions"""
        for ext in extension_matches:
            if filepath.endswith(ext):
                return True
        return False
    
    file_path_matcher = custom_matcher or extension_matcher
    _SCANNERS.append((scan_function, file_path_matcher))


def register_files_scan(scan_files_function, files_matcher):
    """Register files scanner.
    
    :param scan_files_function: Scan function returning SongDetails from list of 
        files.
    :param files_matcher: Function returning True for list of files that match
        or False for files that doesn't match.
        
    """
    _MULTI_SCANNERS.append((scan_files_function, files_matcher))


def scan_files(files):
    """Scan several files for SongDetails.
    
    :param files: List of files to be scanned, you can also give this single 
        file.
    :type files: [string, ...]
    
    :rtype: [:class:`SongDetails`, ...]
    :return: List of SongDetails found, list maybe empty if nothing is found.
    
    """
    
    # If the given files are not iterable, such as string. Make it iterable.
    if not hasattr(files, "__iter__"):
        files = [files]
    
    # Register default scanners
    _register_default_scanners()
    
    # Search from all m
    songs = []
    for scan_files_, files_matcher in _MULTI_SCANNERS:
        if files_matcher(files):
            songs.append(scan_files_(files))
            
    for file_path in files:
        song = scan(file_path)
        if song is not None:
            songs.append(song)
            
    return songs


def scan(file_path):
    """Scan single file
    
    :param file_path: Path to the file.
    
    :return: Returns the SongDetails matching the given file path.
    :rtype: :class:`SongDetails`, or :const:`None`
    
    """
    
    # Registers default scanners
    _register_default_scanners()
    
    # Tries all registered scanners
    for scan_function, file_path_matcher in _SCANNERS:
        if file_path_matcher(file_path):
            song = scan_function(file_path)
            if song is not None:
                return song
    return None


def _register_default_scanners():
    """Registers the default scanners provided in :mod:`songdetails`.
    
    If you wish to register own scanners, you should use instead
    :func:`register_file_scan` and :func:`register_files_scan` directly within
    your module.
    
    """
    global _HAS_DEFAULTS
    from songdetails.mp3details import scan as mp3_scan
    if _HAS_DEFAULTS:
        return
    _HAS_DEFAULTS = True
    
    # Register individual scanners
    register_file_scan(mp3_scan, ('.mp3', ))
