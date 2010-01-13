"""
Module to help mp3details retrieve MPEG-1 audio metadata.
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

from mpeg1audio import MPEGAudio, MPEGAudioHeaderException
from songdetails.mp3details.exceptions import MP3DetailsException

__all__ = ['MPEGAudioDescriptor']

class MPEGAudioDescriptor(object):
    """MPEG Audio descriptor"""
    def __init__(self, name):
        """Create MPEG Audio descriptor.
        
        :param name: Name of the mpeg audio attribute, for example C
            {"duration"}.
        :type name: string
        
        """
        self.name = name
        
    def __set__(self, instance, value):
        """Set value.
        
        :param instance: Instance of owner.
        :type instance: object
        
        :param value: New value.
        :type value: object
        
        """
        pass
        
    def __get__(self, instance, instance_class=None): #@UnusedVariable
        """Get value.
        
        :param instance: Instance of owner.
        :type instance: object
        
        :param instance_class: Class of instance?
        :type instance_class: class
         
        """
        if instance is None:
            return
        
        return getattr(instance._mpegaudio, self.name)
    
    @classmethod
    def initialize_owner(cls, instance, filepath, force=False):
        """Initialize MPEG audio descriptor for object.
        
        :param instance: Owner instance.
        :type instance: object
        
        :param filepath: File path to MP3.
        :type filepath: string
        
        :param force: Force re-initialization, rewriting the values.
        :type force: bool
        
        :raise MP3DetailsException: Raised if the file is not MPEG Audio file.
        
        """
        if not hasattr(instance, "_mpegaudio") or force:
            try:
                instance._mpegaudio = MPEGAudio(open(filepath, 'rb'))
            except MPEGAudioHeaderException:
                raise MP3DetailsException('Not MPEG Audio file.')