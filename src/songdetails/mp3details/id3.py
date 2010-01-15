"""
ID3 Helper for :mod:`songdetails.mp3details`.

"""
from tagger import ID3FrameException
from tagger import ID3v1
from tagger import ID3v2

__all__ = ["ID3TagDescriptor"]

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

def _genre_convert(genre):
    """If the genre is number, or something numbery, convert to string.
    
    Tries to lookup from known numeric genre table for the actual genre. Even in
    ID3v2 tags there seems to be numeric genres used by some players, such as:
    :const:`"(17)"` meaning Rock, number comes apparently from ID3v1 specs and
    parentheses for fun.
    
    http://en.wikipedia.org/wiki/ID3 and
    http://www.multimediasoft.com/amp3dj/help/amp3dj_00003e.htm#ss13.3
    
    :param genre: Genre, or genre number.
    :type genre: string, or int
    
    :return: Textual representation of genre number.
    :rtype: string
    :raise KeyError: Raised when genre is not found.
    
    """
    
    # Numeric genre
    genre_number = None
    
    # Even in ID3v2 tags some of them includes the genres such as: "(17)"
    # meaning probably same as in ID3v1 tags ("Rock").
    try:
        genre_number = int(genre.strip("()"))
    except (ValueError, TypeError):
        pass
    
    # We convert number to meaningful string.
    if genre_number is not None:
        try:
            return _NUMERIC_GENRES[genre_number]
        except KeyError:
            pass
    
    return genre


def _track_convert(track):
    """Converts track to number.
    
    :param track: Track number of the song.
    :type track: string, or int
    
    :raise ValueError: Raised if cannot be converted.
    
    :return: Number representing track I{order number} in album.
    :rtype: int
    
    """
    if '/' in track:
        return int(track.split("/")[0])
    return int(track)    


def _force_unicode(bstr, encoding, fallback_encodings=None):
    """Force unicode, ignore unknown.
    
    Forces the given string to unicode with first guessing, then forcing by
    using given encoding and ignoring unknown characters. This is sadly many
    times necessary, since there usually are only pieces of string without 
    proper encoding, such as file system file names where usually any bytes
    are accepted as filenames.
    
    :param bstr: String
    :type bstr: Basestring
    
    :param encoding: Assumed encoding, notice that by giving encoding that can
        decode all 8-bit characters such as ISO-8859-1 you effectively may be
        decoding all string regardless were they in that encoding or not.
    :type encoding: string
    
    :param fallback_encodings: Fallback on trying these encodings if not the
        assumed encoding.
    :type fallback_encodings: list of string
    
    :return: Unicoded given string
    :rtype: unicode string
    
    """
    # We got unicode, we give unicode
    if isinstance(bstr, unicode):
        return bstr
    
    if fallback_encodings is None:
        fallback_encodings = ['UTF-16', 'UTF-8', 'ISO-8859-1']
        
    encodings = [encoding] + fallback_encodings
    
    for enc in encodings:
        try:
            return bstr.decode(enc)
        except UnicodeDecodeError:
            pass
        
    # Finally, force the unicode
    return bstr.decode(encoding, 'ignore')


class ID3TagDescriptor(object):
    """ID3vTag descriptor"""
    def __init__(self, v24fid, v23fid=None, v22fid=None, v1fid=None,
                 converter=None):
        """Create id3v descriptor.
        
        :param v24fid: ID3v2.4 Frame ID, for example "TALB" for album.
        :type v24fid: string, or None
        
        :param v23fid: ID3v2.3 Frame ID, for example "TALB" for album.
        :type v23fid: string, or None
        
        :param v22fidd: ID3v2 Frame ID, for example "TAL" for album.
        :type v22fidd: string, or None
        
        :param v1fid: ID3v1 Frame "ID", for example "album".
        :type v1fid: string, or None
        
        :keyword converter: Value converter, converts the raw value to new type.
        :type converter: lambda oldValue: newValue, or None
        
        :see: L{ID3TagDescriptor.initialize_owner}
        
        """
        self.v1fid = v1fid
        self.v22fid = v22fid
        self.v23fid = v23fid
        self.v24fid = v24fid
        self.converter = converter or (lambda x: x)
    
    def _get_fid_by_version(self, instance):
        """Get FID For this version.
        
        :param instance: Instance of owner of this descriptor
        :return: Returns Frame ID used for setting and getting values. 
        :rtype: string
        
        """
        # Note that there exists two pytagger versions, other has id3v2 frame
        # version number as string, and other as floats.
        #
        # The one with string frame version numbers is most likely the newer
        # codebase.
        if instance._id3v2.version in (2.4, "2.4"):
            return self.v24fid
        elif instance._id3v2.version in (2.3, "2.3"):
            return self.v23fid
        elif instance._id3v2.version in (2.2, "2.2"):
            return self.v22fid
        else:
            return self.v24fid # TODO: CHECK!
    
    def __set__(self, instance, value):
        """Set value.
        
        :param instance: Instance of owner.
        :type instance: object
        
        :param value: New value.
        :type value: unicode string
        
        """
        if not hasattr(instance, "_id3v2"):
            return
        
        fid = self._get_fid_by_version(instance)
        if fid is None:
            return
        
        new_frame = instance._id3v2.new_frame(fid)
        new_frame.set_text(_force_unicode(value, 'utf-16'))
        
        # Remove existing (only first)
        if instance._id3v2_frames.has_key(fid):
            instance._id3v2.frames.remove(instance._id3v2_frames[fid][0])
            del instance._id3v2_frames[fid][0]
        
        instance._id3v2.frames.append(new_frame)
        instance._id3v2_frames.setdefault(fid, [])
        instance._id3v2_frames[fid].append(new_frame)
    
    def __get__(self, instance, instance_class=None): #@UnusedVariable
        """Get value.
        
        :param instance: Instance of owner.
        :type instance: object
        
        :param instance_class: Class of instance?
        :type instance_class: class
         
        """
        
        if instance is None:
            return None
        
        # First priority, get id3v2 frame item if found
        try:
            return self.converter(self._get_id3v2(instance))
        except ValueError:
            pass
        
        # Second priority, get id3v1 frame item if found
        try:
            return self.converter(self._get_id3v1(instance))
        except ValueError:
            pass
        
        # Nothing was found, we still have to return None.
        return None
        
    def _get_id3v1(self, instance):
        """Get ID3v1 value.
        
        :param instance: Instance having descriptor.
        :type instance: object.
        
        :raise ValueError: Raised when value cannot be retrieved.
        
        """
        try:
            return _force_unicode(getattr(instance._id3v1, self.v1fid),
                                    'ISO-8859-1')
        except AttributeError:
            raise ValueError('Cannot find the id3v1 frame, or frame ID.')

    def _get_id3v2(self, instance):
        """Get ID3v2 value.
        
        :param instance: Instance having descriptor.
        :type instance: object.
        
        :raise ValueError: Raised when value cannot be retrieved.
        
        """
        
        id3v2_frames = instance._id3v2_frames
        
        fid = self._get_fid_by_version(instance)
        
        try:
            # Parse field
            first_frame = id3v2_frames[fid][0]
        except KeyError:
            pass
        else:
            first_frame.parse_field()
            first_string = first_frame.strings[0].replace("\x00", "")
            return _force_unicode(first_string, first_frame.encoding)
            
        raise ValueError('Cannot find the id3v2 frame, or frame ID.')
    
    @classmethod
    def initialize_owner(cls, instance, filepath, force=False):
        """Initializes the owner of this descriptor for using the descriptor.
        
        :param instance: Owner instance.
        :type instance: object
        
        :param filepath: File path to MP3.
        :type filepath: string
        
        :param force: Force re-initialization, rewriting the values.
        :type force: bool
        
        """
        if not hasattr(instance, "_id3v1") or force:     
            # Parse ID3v1:
            instance._id3v1 = ID3v1(filepath)
        
        if not hasattr(instance, "_id3v2") or force:
            # Parse ID3v2
            instance._id3v2 = ID3v2(filepath)
        
        if not hasattr(instance, "_id3v2_frames") or force:
            # ID3v2 Frames:
            instance._id3v2_frames = {}
            for frame in instance._id3v2.frames:
                instance._id3v2_frames.setdefault(frame.fid, [])
                instance._id3v2_frames[frame.fid].append(frame)
    
    @classmethod
    def save(cls, instance):
        """Saves the changes in instance.
        
        :param instance: Owner instance.
        :type instance: object
        
        """        
        instance._id3v2.commit()


_NUMERIC_GENRES = {
    0 : "Blues",
    1 : "Classic Rock",
    2 : "Country",
    3 : "Dance",
    4 : "Disco",
    5 : "Funk",
    6 : "Grunge",
    7 : "Hip-Hop",
    8 : "Jazz",
    9 : "Metal",
    10 : "New Age",
    11 : "Oldies",
    12 : "Other",
    13 : "Pop",
    14 : "R&B",
    15 : "Rap",
    16 : "Reggae",
    17 : "Rock",
    18 : "Techno",
    19 : "Industrial",
    20 : "Alternative",
    21 : "Ska",
    22 : "Death Metal",
    23 : "Pranks",
    24 : "Soundtrack",
    25 : "Euro-Techno",
    26 : "Ambient",
    27 : "Trip-Hop",
    28 : "Vocal",
    29 : "Jazz+Funk",
    30 : "Fusion",
    31 : "Trance",
    32 : "Classical",
    33 : "Instrumental",
    34 : "Acid",
    35 : "House",
    36 : "Game",
    37 : "Sound Clip",
    38 : "Gospel",
    39 : "Noise",
    40 : "Alternative Rock",
    41 : "Bass",
    42 : "Soul",
    43 : "Punk",
    44 : "Space",
    45 : "Meditative",
    46 : "Instrumental Pop",
    47 : "Instrumental Rock",
    48 : "Ethnic",
    49 : "Gothic",
    50 : "Darkwave",
    51 : "Techno-Industrial",
    52 : "Electronic",
    53 : "Pop-Folk",
    54 : "Eurodance",
    55 : "Dream",
    56 : "Southern Rock",
    57 : "Comedy",
    58 : "Cult",
    59 : "Gangsta",
    60 : "Top 40",
    61 : "Christian Rap",
    62 : "Pop/Funk",
    63 : "Jungle",
    64 : "Native US",
    65 : "Cabaret",
    66 : "New Wave",
    67 : "Psychadelic",
    68 : "Rave",
    69 : "Showtunes",
    70 : "Trailer",
    71 : "Lo-Fi",
    72 : "Tribal",
    73 : "Acid Punk",
    74 : "Acid Jazz",
    75 : "Polka",
    76 : "Retro",
    77 : "Musical",
    78 : "Rock & Roll",
    79 : "Hard Rock",
    80 : "Folk",
    81 : "Folk-Rock",
    82 : "National Folk",
    83 : "Swing",
    84 : "Fast Fusion",
    85 : "Bebob",
    86 : "Latin",
    87 : "Revival",
    88 : "Celtic",
    89 : "Bluegrass",
    90 : "Avantgarde",
    91 : "Gothic Rock",
    92 : "Progressive Rock",
    93 : "Psychedelic Rock",
    94 : "Symphonic Rock",
    95 : "Slow Rock",
    96 : "Big Band",
    97 : "Chorus",
    98 : "Easy Listening",
    99 : "Acoustic",
    100 : "Humour",
    101 : "Speech",
    102 : "Chanson",
    103 : "Opera",
    104 : "Chamber Music",
    105 : "Sonata",
    106 : "Symphony",
    107 : "Booty Bass",
    108 : "Primus",
    109 : "Porn Groove",
    110 : "Satire",
    111 : "Slow Jam",
    112 : "Club",
    113 : "Tango",
    114 : "Samba",
    115 : "Folklore",
    116 : "Ballad",
    117 : "Power Ballad",
    118 : "Rhythmic Soul",
    119 : "Freestyle",
    120 : "Duet",
    121 : "Punk Rock",
    122 : "Drum Solo",
    123 : "Acapella",
    124 : "Euro-House",
    125 : "Dance Hall",
    126 : "Goa",
    127 : "Drum & Bass",
    128 : "Club - House",
    129 : "Hardcore",
    130 : "Terror",
    131 : "Indie",
    132 : "BritPop",
    133 : "Negerpunk",
    134 : "Polsk Punk",
    135 : "Beat",
    136 : "Christian Gangsta Rap", # My favorite!
    137 : "Heavy Metal",
    138 : "Black Metal",
    139 : "Crossover",
    140 : "Contemporary Christian",
    141 : "Christian Rock",
    142 : "Merengue",
    143 : "Salsa",
    144 : "Thrash Metal",
    145 : "Anime",
    146 : "JPop",
    147 : "Synthpop",
}
