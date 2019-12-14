from unittest import TestCase

from mediaug.augment import Pipeline
from mediaug.dataset import Dataset


class TestAugment(TestCase):

    def test_pipeline_init(self):
        ds = Dataset('/Users/sean/projects/cancerDetection/data/cells')
        pipeline = Pipeline(ds)
    


    