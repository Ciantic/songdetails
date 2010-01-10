``songdetails`` package documentation.
==================================

Installation
============

Dependencies
------------

 * :mod:`mpeg1audio` - http://github.com/Ciantic/mpeg1audio/
 * :mod:`pytagger` - http://github.com/scy/pytagger/

Installation
------------

Remember to first get the above dependencies.

This package uses `distutils` and is easily installed using that:

	$ setup.py install
	
Under Windows you can start the command prompt with administrator rights (by 
right clicking `cmd.exe` and using "Run as administrator") then run the above 
command.
	
Usage example:
==============

    >>> import songdetails
    >>> song = songdetails.scan("tests/data/song.mp3")
    >>> if song is not None:
    ...     print song.duration
    0:03:12
