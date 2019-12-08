from unittest import TestCase

from mediaug.dataset import Dataset
from mediaug.download import get_data_cache


class TestDataset(TestCase):
    def test_load_sipakmed_cells(self):
        ds = Dataset('/Users/seanwade/projects/cancerDetection/data/sipakmed_processed/cells')
        self.assertEqual(4049, ds.size)
    
    def test_load_sipakmed_slides(self):
        ds = Dataset('/Users/seanwade/projects/cancerDetection/data/sipakmed_processed/slides')
        self.assertEqual(223, len(ds['dyskeratotic']))
        self.assertEqual(966, ds.size)


    