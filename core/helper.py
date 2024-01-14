import os
import subprocess
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse


def run_command(cmd, input=""):
    rst = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input.encode("utf-8"))
    assert rst.returncode == 0, rst.stderr.decode("utf-8")
    return rst.stdout.decode("utf-8")


def is_file_exists(filepath):
    if os.path.isfile(filepath):
        return True
    else:
        return False


def download_and_unzip(tool):
    print('Downloading ' + str(tool.name) + '...')

    http_response = urlopen(tool.url)
    zipfile = ZipFile(BytesIO(http_response.read()))

    print('Extracting...')
    extract_to = 'external-tools'
    zipfile.extractall(path=extract_to)

    if tool.has_dependencies:
        repo_path = extract_to + '/' + tool.folder
        install_dependencies(repo_path)
    else:
        print('Successfully installed!')


def install_dependencies(repo_path):
    print('Installing dependencies...')

    try:
        command = 'cd ' + repo_path + ' && pip install -r requirements.txt'

        run_command(command)

        print('Successfully installed!')
    except Exception as e:
        error_message = str(e.args[0]) if e.args else "An unknown error occurred"

        print(error_message)


def send_message_to_websocket(message):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "terminal",
        {
            "type": "chat.message",
            "message": message,
        },
    )
