SongDetails package documentation.
==================================

Installation
============

.. rubric:: Dependencies

* :mod:`mpeg1audio` - http://github.com/Ciantic/mpeg1audio/
* :mod:`pytagger` - http://github.com/scy/pytagger/


Usage example:
==============

    >>> import songdetails
    >>> song = songdetails.scan("tests/data/song.mp3")
    >>> if song is not None:
    ...     print song.duration
    0:03:12
	

API Reference
=============

.. autosummary::
   :toctree: api

   songdetails


.. toctree::
   :maxdepth: 2

   glossary


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`