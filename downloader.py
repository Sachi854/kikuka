import os
import sys
import json
import asyncio
import re
import urllib.parse
import urllib.request


def get_download_site_dict(json_data: dict) -> dict:
    download_site_dict = {}
    for i in json_data:
        # get domain name from url of i
        domain_name = urllib.parse.urlparse(i["url"]).netloc
        # if the domain name is not in the download site dict, add it
        if domain_name not in download_site_dict:
            download_site_dict[domain_name] = []
        # append i to the download site dict value list with the domain name
        download_site_dict[domain_name].append(i)

    # return the download site dict
    return download_site_dict


def get_repo_name(url: str) -> str:
    # get the last part of the url
    last_part = url.split('/')[-1]
    # remove the .git suffix
    repo_name = last_part.replace('.git', '')
    # return the repo name
    return repo_name


def generate_git_clone_path_dict(download_base_path_dict: dict, download_git_dict: dict) -> dict:
    cwd = os.getcwd() + '/'
    path = cwd + download_base_path_dict[download_git_dict["type"]
                                         ] + get_repo_name(download_git_dict["url"])
    return {"path": path, "url": download_git_dict["url"]}


def generate_curl_path_dict(download_base_path_dict: dict, download_curl_dict: dict) -> dict:
    cwd = os.getcwd() + '/'
    path = cwd + download_base_path_dict[download_curl_dict["type"]
                                         ] + download_curl_dict["url"].split('/')[-1]
    return {"path": path, "url": download_curl_dict["url"]}


def parse_civitai_url(url: str) -> dict:
    endpoint_url = "https://civitai.com/api/v1/models/"
    path = urllib.parse.urlparse(url).path
    path_list = path.split("/")
    number_list = [x for x in path_list if x.isdigit()]
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(
        endpoint_url + number_list[-1], headers=headers)
    with urllib.request.urlopen(req) as response:
        the_page = response.read().decode("utf-8")
    return json.loads(the_page)


def generate_civitai_path_list(download_base_path_dict: dict, download_civitai_dict: dict) -> list:
    result = []
    cwd = os.getcwd() + '/'
    civitai_json = parse_civitai_url(download_civitai_dict["url"])
    for i in civitai_json["modelVersions"][0]["files"]:
        if i["type"] == "VAE":
            path = cwd + download_base_path_dict["VAE"] + i["name"]
            result.append({"path": path, "url": i["downloadUrl"]})
        else:
            path = cwd + \
                download_base_path_dict[civitai_json["type"]] + i["name"]
            result.append({"path": path, "url": i["downloadUrl"]})
    return result


def generate_download_path_dict(download_base_path_dict: dict, download_site_dict: dict) -> dict:
    result = {"git": [], "curl": []}
    for i in download_site_dict['github.com']:
        result["git"].append(
            generate_git_clone_path_dict(download_base_path_dict=download_base_path_dict, download_git_dict=i))
    for i in download_site_dict['huggingface.co']:
        result["curl"].append(generate_curl_path_dict(
            download_base_path_dict=download_base_path_dict, download_curl_dict=i))
    for i in download_site_dict['civitai.com']:
        result["curl"].extend(generate_civitai_path_list(
            download_base_path_dict=download_base_path_dict, download_civitai_dict=i))
    return result


async def async_git_clone(path: str, url: str) -> None:
    print(url)
    # create a command
    command = ["git", "clone", "--depth=1", url,
               path]
    # create a process
    process = await asyncio.create_subprocess_exec(*command)
    # wait for the process to complete
    await process.wait()


async def async_curl(path: str, url: str) -> None:
    print(url)
    # create a command
    command = ['curl', '-Lo', path, url]
    # create a process
    process = await asyncio.create_subprocess_exec(*command)
    # wait for the process to complete
    await process.wait()


async def async_download(download_path_dict: dict) -> None:
    tasks = []
    for i in download_path_dict["git"]:
        if not os.path.exists(i["path"]):
            tasks.append(asyncio.create_task(
                async_git_clone(path=i["path"], url=i["url"])))
    for i in download_path_dict["curl"]:
        if not os.path.exists(i["path"]):
            tasks.append(asyncio.create_task(
                async_curl(path=i["path"], url=i["url"])))
    await asyncio.gather(*tasks)


def main():
    cwd = os.getcwd() + '/'
    if not sys.stdin.isatty():
        # read the standard input as json
        json_data = json.loads(sys.stdin.read())
    # not exists the standard input
    else:
        print("Please input the json data.")
        exit(1)

    # mkdir if not exists
    download_base_path_dict = json_data["path"]
    for i in download_base_path_dict.values():
        if not os.path.exists(i):
            os.makedirs(
                cwd + i, exist_ok=True)

    # genereate download site dict
    download_site_dict = get_download_site_dict(json_data=json_data["url"])
    download_site_dict = generate_download_path_dict(
        download_base_path_dict=download_base_path_dict, download_site_dict=download_site_dict)

    # async download
    print("start download")
    asyncio.run(async_download(download_path_dict=download_site_dict))

    # print the result
    print("finish download")


if __name__ == '__main__':
    main()
