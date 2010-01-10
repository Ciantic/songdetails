"""songdetails - package tests"""

import unittest
import songdetails

class SongTests(unittest.TestCase):
    """Simple song tests."""
    def setUp(self):
        pass
        
    def testScan(self):
        """Scan test"""
        songs = songdetails.scan(["data/song.mp3"])
        self.assertEqual(songs[0].artist, "Rauli Badding Somerjoki")
        self.assertEqual(songs[0].duration.seconds, 192)
        