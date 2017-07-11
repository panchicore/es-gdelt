import os
import zipfile
import requests
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_PATH = os.path.join(BASE_PATH, "")
ZIP_EXTRACT_PATH = os.path.join(BASE_PATH, "data", "realtime")


def slack(message):
    """
    Notify activities to slack channels.
    Set SLACK_NOTIFICATIONS_ENABLED and SLACK_NOTIFICATIONS_ENABLED env vars.
    :param message: 
    :return: 
    """
    if os.environ.get("SLACK_NOTIFICATIONS_ENABLED", None):
        data = {
            "username": "gdelt-cron",
            "text": message,
            "icon_emoji": ":google:"
        }
        requests.post(os.environ.get("SLACK_NOTIFICATIONS_URL"), json=data)


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
    res = requests.get("http://data.gdeltproject.org/gdeltv2/lastupdate.txt")
    url = None

    for line in res.content.split("\n"):
        if not line:
            continue

        if line.count(".export.CSV.zip") > 0:
            url = line.split(" ")[2]

    if not url:
        return

    filename = download_file(url)
    unzip(filename)
    os.remove(filename)
    slack("downloaded {}".format(filename))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print "more than 1"
    get()