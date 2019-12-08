import os
from unittest import TestCase

from mediaug.download import get_data_cache, download_sipakmed


class TestDownload(TestCase):
    def test_get_data_cache(self):
        get_data_cache()
        self.assertTrue(True)

    def test_download_sipakmed(self):
        download_sipakmed()
        cache = get_data_cache()
        self.assertTrue(os.path.exists(os.path.join(cache, 'sipakmed_raw')))
