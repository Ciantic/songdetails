Python package ``songdetails`` 
==============================

Pure Python package for retrieving details of songs in computer. The main 
purpose is to provide easiest possible interface for *updating* and *retrieving*
information. For example the ID3 feature of multiple same named frames is not
default, the default is the fact that single song most likely has single artist,
title, album name, etc.

Why on earth would you want to create yet another tagger thingie? Simply there 
doesn't seem to be any decent tagging program licensed for free use, those 
which are free are under GPL, and that is no-no for most of the projects.

End-users
---------

### Dependencies

* [`mpeg1audio`](http://github.com/Ciantic/mpeg1audio/)
* [`pytagger`](http://github.com/Ciantic/pytagger/)

*Note:* Both of the dependencies are *pure* python packages.

### Installation

Remember to first get the above dependencies.

This package uses `distutils` and is easily installed using that:

	$ setup.py install
	
Under Windows you can start the command prompt with administrator rights (by 
right clicking `cmd.exe` and using "Run as administrator") then run the above 
command.
	
### Usage example:

    >>> import songdetails
    >>> song = songdetails.scan("data/song.mp3")
    >>> if song is not None:
    ...     print song.duration
    0:03:12

#### Saving changes:

    >>> import songdetails
    >>> song = songdetails.scan("data/commit.mp3")
    >>> if song is not None:
    ...     song.artist = "Great artist"
    ...     song.save()

Developers
----------

This project uses Eclipse with [PyDev](http://pydev.sourceforge.net/), [Pylint](http://www.logilab.org/857) and [Sphinx documentation generator](http://sphinx.pocoo.org/). Accordingly all docstrings and docs are in reStructuredText, which ultimately is generated to HTML.

### Eclipse workspace

#### Project references

`songdetails` has two project references: `pytagger` and `mpeg1audio`. It is best to create own workspace for this project, where you also add those two projects.

#### Launch configurations

There exists two Eclipse launch configurations:

 * `tests/Tests for songdetails.launch` - Unit tests.
 * `docs/SphinxDoc songdetails.launch` - Generating documentation.

Using Eclipse you must go to Run Configurations *dialog* and run them once so they appear to the list.
