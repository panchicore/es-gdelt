import os
import zipfile
import requests
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_PATH = os.path.join(BASE_PATH, "")
ZIP_EXTRACT_PATH = os.path.join(BASE_PATH, "data", "old")


def slack(message):
    data = {
        "username": "gdelt-luis-machine",
        "text": message,
        "icon_emoji": ":google:"
    }
    requests.post("https://hooks.slack.com/services/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", json=data)


def download_file(url):
    print 'downloading:', url
    local_filename = url.split('/')[-1]
    local_filename = os.path.join(DOWNLOAD_PATH, local_filename)
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def unzip(path):
    print 'unzipping:', path
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(ZIP_EXTRACT_PATH)
    zip_ref.close()


def get():
    BASE_URL = "http://data.gdeltproject.org/events/"
    res = requests.get(BASE_URL + "index.html")
    targets = []
    for line in res.content.split("\n"):
        if line.count(".export.CSV.zip") > 0:
            download_url = BASE_URL + line.split("\"")[1]
            targets.append(download_url)

    for download_url in targets:
        filename = download_file(download_url)
        unzip(filename)
        os.remove(filename)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pass
    get()