===============
``songdetails`` 
===============

Pure Python package for retrieving details of songs in computer. The main 
purpose is to provide easiest possible interface for updating and retrieving
information. For example the ID3 feature of multiple same named frames is not
default, the default is the fact that single song most likely has single artist,
title, album name, etc.

End-users
=========

Dependencies
------------

* ``mpeg1audio`` - http://github.com/Ciantic/mpeg1audio/
* ``pytagger`` - http://github.com/scy/pytagger/

Installation
------------

Remember to first get the above dependencies.

This package uses `distutils` and is easily installed using that:

	$ setup.py install
	
Under Windows you can start the command prompt with administrator rights (by 
right clicking `cmd.exe` and using "Run as administrator") then run the above 
command.
	
Usage example:
--------------

    >>> import songdetails
    >>> song = songdetails.scan("tests/data/song.mp3")
    >>> if song is not None:
    ...     print song.duration
    0:03:12


Developers
==========
...