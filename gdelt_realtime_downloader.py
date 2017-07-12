import os
import zipfile
import requests
import sys
import datetime

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
    """

    :param url:
    :return:
    """
    print 'downloading:', url
    local_filename = url.split('/')[-1]
    local_filename = os.path.join(DOWNLOAD_PATH, local_filename)
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    if not r.ok:
        print "request returned with code {}".format(r.status_code)
        return None
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                # f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def unzip(path):
    print 'unzipping:', path
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(ZIP_EXTRACT_PATH)
    zip_ref.close()


def get(_from_date=None):
    """

    :param _from_date:
    :return:
    """
    if not _from_date:
        res = requests.get("http://data.gdeltproject.org/gdeltv2/lastupdate.txt")
        url = None

        for line in res.content.split("\n"):
            if not line:
                continue

            if line.count(".export.CSV.zip") > 0:
                url = line.split(" ")[2]

        if not url:
            return
    else:
        url = "http://data.gdeltproject.org/gdeltv2/{0}.export.CSV.zip".format(_from_date)
        mentions_url = "http://data.gdeltproject.org/gdeltv2/{0}.mentions.CSV.zip".format(_from_date)

    filename = download_file(url)
    if filename:
        unzip(filename)
        os.remove(filename)
        slack("downloaded {}".format(filename))


if __name__ == "__main__":
    """
    To download the current 15 mins update use (good for cron jobs):
    python gdelt_realtime_downloader.py
    To download a time range (good when cron jobs or internet connection fails :))
    python gdelt_realtime_downloader.py 2017-07-12T10:00 2017-07-12T11:00
    """
    if len(sys.argv) > 1:
        _from_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%dT%H:%M")
        _to_date = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%dT%H:%M")
        if _from_date > _to_date:
            raise Exception("{0} must be after {1}".format(_from_date, _to_date))

        while _from_date <= _to_date:
            get(_from_date.strftime("%Y%m%d%H%M%S"))
            _from_date = _from_date + datetime.timedelta(minutes=15)
    else:
        get()
