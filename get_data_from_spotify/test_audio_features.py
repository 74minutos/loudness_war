import unittest
import tempfile
from get_data_from_spotify import get_audio_analysis
from get_data_from_spotify import join_data

class Test(unittest.TestCase):
    def test_tracks_analysis_to_directory(self):
        # this creates a temporary directory for testing: this way we don't
        # leave crap all over the file system
        with tempfile.TemporaryDirectory() as temp_dir:
            data = [{'track_name':123, 'track_id': 123}]
            get_audio_analysis.track_analysis_to_directory(temp_dir, data, 'test.json')
            testing_loading_data = join_data.getting_data_to_join(temp_dir)
            for test in testing_loading_data:
                self.assertEqual(data, test)
