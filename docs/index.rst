SongDetails package documentation.
==================================

.. toctree::
   :maxdepth: 2

   songdetails
   mp3details
   glossary


Installation
============

Dependencies
------------

 * :mod:`mpeg1audio` - http://github.com/Ciantic/mpeg1audio/
 * :mod:`pytagger` - http://github.com/scy/pytagger/

	
Usage example:
==============

    >>> import songdetails
    >>> song = songdetails.scan("tests/data/song.mp3")
    >>> if song is not None:
    ...     print song.duration
    0:03:12
	
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`