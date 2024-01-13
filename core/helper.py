import os
import subprocess
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile


def run_command(cmd, input=""):
    rst = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input.encode("utf-8"))
    assert rst.returncode == 0, rst.stderr.decode("utf-8")
    return rst.stdout.decode("utf-8")


def is_file_exists(filepath):
    if os.path.isfile(filepath):
        return True
    else:
        return False


def download_and_unzip(url, extract_to='.'):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)

