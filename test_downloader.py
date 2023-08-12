import downloader as d
import unittest
import urllib.parse
import urllib.request


class TestDownloader(unittest.TestCase):
    # test get_civitai_api function
    def test_get_civitai_api(self):
        self.assertEqual(d.get_civitai_api(
            "https://civitai.com/models/16014/")["id"], 16014)
        self.assertRaises(urllib.error.HTTPError, d.get_civitai_api,
                          "https://www.google.co.jp")

if __name__ == '__main__':
    print("Running tests for downloader.py")
    unittest.main()
