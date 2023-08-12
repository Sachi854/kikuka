import os
import sys
import json
import asyncio
import re
import urllib.parse
import urllib.request

# extensions

# define the get api function
# this function will get the api
# arguments: url
# return: json


def get_civitai_api(url):
    endpoint_url = "https://civitai.com/api/v1/models/" + url.split('/')[-2]
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(endpoint_url, headers=headers)
    with urllib.request.urlopen(req) as response:
        the_page = response.read().decode("utf-8")
    return json.loads(the_page)


# define the get file name from url function
# this function will get the file name from the url
# arguments: url
# return: file name
def get_file_name_from_url(url):
    return url.split('/')[-1]


# define the get repository name function
# this function will get the repository name from the url
# arguments: url
# return: repository name
def get_repository_name(url):
    return re.search(r"/([^/]+)\.git$", url).group(1)


# define the async git clone function
# this function will clone a git repository
# arguments: file path, url
# return: none
async def async_git_clone(file_path, url):
    print(url)
    # create a command
    command = ["git", "clone", "--depth=1", url,
               file_path + get_repository_name(url)]
    # create a process
    process = await asyncio.create_subprocess_exec(*command)
    # wait for the process to complete
    await process.wait()


# define the async download function
# this function will download a file using curl
# arguments: file path, url
# return: none
async def async_download(file_path, url):
    print(url)
    # create a command
    command = ['curl', '-Lo', file_path, url]
    # create a process
    process = await asyncio.create_subprocess_exec(*command)
    # wait for the process to complete
    await process.wait()


async def main():
    # get the home directory
    working_dir = os.getcwd() + '/'

    if not sys.stdin.isatty():
        # read the standard input as json
        json_data = json.loads(sys.stdin.read())
    # not exists the standard input
    else:
        # if exists the command line argument, get the command line argument
        # command line arguments : -f <file path>
        # if arguments are not set, throw an error
        try:
            file_path = sys.argv[sys.argv.index('-f') + 1]
            # opne the file
            with open(file_path, 'r') as f:
                # read the file as json
                json_data = json.loads(f.read())
        except ValueError:
            print('Please set the command line arguments')
            print('Usage: python file_fetcher.py -f json_file_path')
            exit(1)

    print(working_dir)

    # mkdir the directory
    print("mkdir")
    for i in json_data["directory"]:
        if i == "ControlNet":
            continue
        elif not os.path.exists(i):
            os.makedirs(
                working_dir + json_data["directory"][i], exist_ok=True)
        else:
            print("Directory already exists!!")

    # download the controlnet files
    print("download files")
    tasks = []
    for i in json_data["url"]:
        # get domain name from url
        domain_name = urllib.parse.urlparse(i["url"]).netloc
        if domain_name == "github.com":
            file_path = working_dir + json_data["directory"][i["type"]]
            file_path_clone = file_path + get_repository_name(i["url"])
            if not os.path.exists(file_path_clone):
                tasks.append(asyncio.create_task(async_git_clone(
                    file_path, i["url"])))
        elif domain_name == "civitai.com":
            j = get_civitai_api(i["url"])
            file_path = working_dir + \
                json_data["directory"][j["type"]] + \
                j["modelVersions"][0]["files"][0]["name"]
            if not os.path.exists(file_path):
                tasks.append(asyncio.create_task(async_download(
                    file_path, j["modelVersions"][0]["files"][0]["downloadUrl"])))
        elif domain_name == "huggingface.co":
            file_path = working_dir + \
                json_data["directory"][i["type"]] + \
                get_file_name_from_url(i["url"])
            if not os.path.exists(file_path):
                tasks.append(asyncio.create_task(async_download(
                    file_path, i["url"])))
        else:
            print("Unknown site")
            exit(1)
    # download the files asynchronously
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
    print("Done!!")
