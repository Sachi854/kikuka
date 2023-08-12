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

    def test_get_file_name_from_url(self):
        self.assertEqual(d.get_file_name_from_url(
            "https://civitai.com/models/16014/"), "")
        self.assertEqual(d.get_file_name_from_url(
            "https://civitai.com/models/16014/16014/tnk.pdf"), "tnk.pdf")

    def test_drop_file_extension(self):
        self.assertEqual(d.drop_file_extension("tnk.pdf"), "tnk")
        self.assertEqual(d.drop_file_extension("tnk"), "tnk")

    def test_get_repository_name(self):
        self.assertEqual(d.get_repository_name(
            "https://github.com/hako-mikan/sd-webui-lora-block-weight.git"), "sd-webui-lora-block-weight")
        self.assertEqual(d.get_repository_name(
            "https://github.com/hako-mikan/sd-webui-lora-block-weight"), "sd-webui-lora-block-weight")
        self.assertEqual(d.get_repository_name(
            "https://www.google.co.jp"), "www.google.co.jp")

if __name__ == '__main__':
    print("Running tests for downloader.py")
    unittest.main()
