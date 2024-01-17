import os
import subprocess
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def run_command(cmd, input=""):
    format_message = "<div class='command'>" + cmd + "</div><hr class='separator'>"
    send_message_to_websocket(format_message)

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while process.poll() is None:
        line = process.stdout.readline().rstrip()
        if line:
            string_data = line.decode('utf-8')
            send_message_to_websocket(string_data)


def is_file_exists(filepath):
    if os.path.isfile(filepath):
        return True
    else:
        return False


def download_and_unzip(tool):
    send_message_to_websocket('Downloading ' + str(tool.name) + '...')

    url = tool.url + '/archive/' + tool.branch + '.zip'
    send_message_to_websocket(url)

    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))

    send_message_to_websocket('Extracting...')
    extract_to = 'external-tools'
    zipfile.extractall(path=extract_to)

    if tool.has_dependencies:
        repo_path = extract_to + '/' + tool.folder + '-' + tool.branch
        install_dependencies(repo_path)
    else:
        send_message_to_websocket('Successfully installed!')


def install_dependencies(repo_path):
    send_message_to_websocket("Installing dependencies...")

    try:
        command = 'cd ' + repo_path + ' && pip install -r requirements.txt'

        run_command(command)

        send_message_to_websocket("Successfully installed!")
    except Exception as e:
        error_message = str(e.args[0]) if e.args else "An unknown error occurred"

        send_message_to_websocket(error_message)


def send_message_to_websocket(message):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "terminal",
        {
            "type": "chat.message",
            "message": message,
        },
    )


async def send_message_to_websocket_async(message):
    channel_layer = get_channel_layer()

    await channel_layer.group_send("terminal", {
        "type": "chat.message",
        "message": message,
    })
