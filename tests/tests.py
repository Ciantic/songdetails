"""songdetails - package tests"""
# -*- coding: iso-8859-1 -*-
import os
import unittest
import doctest
import songdetails
import random
from songdetails import mp3details

class SongTests(unittest.TestCase):
    """Simple song tests."""
    def setUp(self):
        pass
        
    def testScan(self):
        """Scan test"""
        song = songdetails.scan(os.path.join("data", "song.mp3"))
        self.assertEqual(song.artist, "Rauli Badding Somerjoki")
        self.assertEqual(song.duration.seconds, 192)
        
    def testCommit(self):
        """Commit test"""
        # Open and save
        song = songdetails.scan(os.path.join("data", "commit.mp3"))
        random_artist_name = u"Örinä artist%s" % random.random()
        song.artist = random_artist_name
        song.save()
        del song
        
        # Re-open and read
        opensong = songdetails.scan(os.path.join("data", "commit.mp3"))
        self.assertEqual(opensong.artist, random_artist_name)
    
    def testDocTests(self):
        """Doc tests"""
        doctest.testmod(songdetails, raise_on_error=True)
        #doctest.testmod(songdetails.scanners, raise_on_error=True)
        #doctest.testmod(mp3details, raise_on_error=True)
        #doctest.testmod(mp3details.audio, raise_on_error=True)
        #octest.testmod(mp3details.id3, raise_on_error=True)
        #doctest.testmod(mp3details.scanners, raise_on_error=True)
        # doctest.testmod(songdetails, raise_on_error=True)

if __name__ == '__main__':
    doctest.testmod(songdetails, raise_on_error=True)