import downloader as d
import unittest
import urllib.parse
import urllib.request
import os


class TestDownloader(unittest.TestCase):
    def test_get_download_site_dict(self):
        site = [{"url": "https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x-AnimeSharp.pth", "type": "UpscaleModel"},
                {"url": "https://huggingface.co/datasets/gsdf/EasyNegative/resolve/main/EasyNegative.safetensors",
                    "type": "TextualInversion"},
                {"url": "https://github.com/Sachi854/kukuri.git", "type": "output"},
                {"url": "https://civitai.com/models/9828/faruzan-genshin-impact"}]
        result = {'huggingface.co': [{"url": "https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x-AnimeSharp.pth", "type": "UpscaleModel"},
                                     {"url": "https://huggingface.co/datasets/gsdf/EasyNegative/resolve/main/EasyNegative.safetensors", "type": "TextualInversion"}],
                  'github.com': [{"url": "https://github.com/Sachi854/kukuri.git", "type": "output"}],
                  'civitai.com': [{"url": "https://civitai.com/models/9828/faruzan-genshin-impact"}]}
        self.assertEqual(d.get_download_site_dict(site), result)
        site.append(
            {"urll": "https://civitai.com/models/9828/faruzan-genshin-impact"})
        self.assertRaises(KeyError, d.get_download_site_dict, site)

    def test_get_repo_name(self):
        self.assertEqual(d.get_repo_name(
            "https://github.com/Sachi854/kukuri.git"), "kukuri")
        self.assertEqual(d.get_repo_name(
            "https://github.com/Sachi854/kukuri"), "kukuri")

    def test_generate_git_clone_path_dict(self):
        cwd = os.getcwd() + '/'
        self.assertEqual(d.generate_git_clone_path_dict({"output": "output/"}, {
                         "url": "https://github.com/Sachi854/kukuri.git", "type": "output"}), {"path": cwd+"output/kukuri", "url": "https://github.com/Sachi854/kukuri.git"})
        self.assertEqual(d.generate_git_clone_path_dict({"output": "output/"}, {
                         "url": "https://github.com/Sachi854/kukuri", "type": "output"}), {"path": cwd+"output/kukuri", "url": "https://github.com/Sachi854/kukuri"})

    def test_generate_curl_path_dict(self):
        cwd = os.getcwd() + '/'
        self.assertEqual(d.generate_curl_path_dict({"output": "output/"}, {"url": "https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x-AnimeSharp.pth", "type": "output"}), {
                         "path": cwd+"output/4x-AnimeSharp.pth", "url": "https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x-AnimeSharp.pth"})

    def test_parse_civitai_url(self):
        self.assertRaises(IndexError, d.parse_civitai_url,
                          "https://github.com/Sachi854/kukuri.git")

    def test_generate_civitai_path_list(self):
        cwd = os.getcwd() + '/'
        self.assertEqual(d.generate_civitai_path_list({"Checkpoint": "ComfyUI/models/checkpoints/",
                                                       "VAE": "ComfyUI/models/vae/", }, {"url": "https://civitai.com/models/122533"}), [
            {"path": cwd+"ComfyUI/models/checkpoints/animagineXL_v10.safetensors",
                "url": "https://civitai.com/api/download/models/133462"},
            {"path": cwd+"ComfyUI/models/vae/sdxl_vae.safetensors", "url": "https://civitai.com/api/download/models/133462?type=VAE&format=SafeTensor"}])

    def test_generate_download_path_dict(self):
        cwd = os.getcwd() + '/'
        self.assertEqual(d.generate_download_path_dict({
            "Checkpoint": "ComfyUI/models/checkpoints/",
            "VAE": "ComfyUI/models/vae/",
            "TextualInversion": "ComfyUI/models/embeddings/",
            "AestheticGradient": "ComfyUI/models/embeddings/",
            "Hypernetwork": "ComfyUI/models/hypernetworks/",
            "LORA": "ComfyUI/models/loras/",
            "Controlnet": "ComfyUI/models/controlnet/",
            "UpscaleModel": "ComfyUI/models/upscale_models/",
            "output": "ComfyUI/output/"},
            {'github.com': [{
                "url": "https://github.com/Sachi854/kukuri.git", "type": "output"}],
             'huggingface.co': [{"url": "https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x-AnimeSharp.pth", "type": "output"}],
             'civitai.com': [{"url": "https://civitai.com/models/122533"}]}),
            {
                "git": [
                    {"path": cwd+"ComfyUI/output/kukuri",
                        "url": "https://github.com/Sachi854/kukuri"}
                ],
                "curl": [
                    {"path": cwd+"ComfyUI/models/upscale_models/4x-AnimeSharp.pth",
                     "url": "https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x-AnimeSharp.pth"},
                    {"path": cwd+"ComfyUI/models/checkpoints/animagineXL_v10.safetensors",
                     "url": "https://civitai.com/api/download/models/133462"},
                    {"path": cwd+"ComfyUI/models/vae/sdxl_vae.safetensors",
                        "url": "https://civitai.com/api/download/models/133462?type=VAE&format=SafeTensor"}
                ]
        })


if __name__ == '__main__':
    unittest.main()
