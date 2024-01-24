import asyncio
import os
import pty
import shutil
import subprocess
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def run_command(command):
    # Start a subprocess with a pseudo-terminal
    master, slave = pty.openpty()
    process = subprocess.Popen(command, stdin=slave, stdout=slave, stderr=slave, close_fds=True, shell=True)

    # Close the slave PTY file descriptor as it is not needed in the parent process
    os.close(slave)

    # Write input to the master PTY file descriptor
    input_data = 'whoami'
    # os.write(master, input_data.encode('utf-8'))

    # Communicate with the subprocess using the master PTY file descriptor
    while True:
        try:
            output = os.read(master, 1024)
            if not output:
                break
            # Do something with the output, for example, print it
            # print(output.decode('utf-8'), end='')

            message = output.decode('utf-8')

            send_message_to_websocket(message)
        except OSError:
            break

    # Wait for the subprocess to finish
    process.wait()

    # Close the master PTY file descriptor
    os.close(master)


async def run_command_async(command):
    # Start a subprocess with a pseudo-terminal
    master, slave = pty.openpty()
    process = await asyncio.create_subprocess_shell(
        command,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        close_fds=True
    )

    # Close the slave PTY file descriptor as it is not needed in the parent process
    os.close(slave)

    # Write input to the master PTY file descriptor
    input_data = 'whoami'
    # os.write(master, input_data.encode('utf-8'))

    # Communicate with the subprocess using the master PTY file descriptor
    while True:
        try:
            output = os.read(master, 1024)
            if not output:
                break
            # Do something with the output, for example, print it
            # print(output.decode('utf-8'), end='')
            await send_message_to_websocket_async(output.decode('utf-8'))
        except OSError:
            break

    # Wait for the subprocess to finish
    await process.wait()

    # Close the master PTY file descriptor
    os.close(master)


def is_file_exists(filepath):
    if os.path.isfile(filepath):
        return True
    else:
        return False


def download_and_unzip(tool):
    send_message_to_websocket('Downloading ' + str(tool.name) + '...\r\n')

    url = tool.url + '/archive/' + tool.branch + '.zip\r\n'
    send_message_to_websocket(url)

    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))

    send_message_to_websocket('Extracting...\r\n')
    extract_to = os.getenv('EXTERNAL_TOOLS_DIR')
    zipfile.extractall(path=extract_to)

    # Remove directory
    extracted_path = extract_to + '/' + tool.folder + '-' + tool.branch
    new_path = extract_to + '/' + tool.folder
    os.rename(extracted_path, new_path)

    if tool.has_dependencies:
        install_dependencies(new_path)
    else:
        send_message_to_websocket('Successfully installed!\r\n')


def install_dependencies(repo_path):
    send_message_to_websocket("Installing dependencies...\r\n")

    try:
        command = 'cd ' + repo_path + ' && pip install -r requirements.txt'
        run_command(command)

        send_message_to_websocket("Successfully installed!\r\n")
    except Exception as e:
        error_message = str(e.args[0]) if e.args else "An unknown error occurred"

        send_message_to_websocket(error_message + '\r\n')


def re_install(tool):
    tool_path = os.getenv('EXTERNAL_TOOLS_DIR') + '/' + tool.folder
    if os.path.exists(tool_path):
        try:
            shutil.rmtree(tool_path)
            send_message_to_websocket('Deleted old files...\r\n')
        except Exception as e:
            send_message_to_websocket(f"Error deleting folder '{tool_path}': {e}\r\n")

    download_and_unzip(tool)


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
