import os
import asyncio
import subprocess

from django.conf import settings

from core.helper import send_message_to_websocket_async, send_message_to_websocket

if os.name == "nt":
    import msvcrt
else:
    import pty

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


def run_command_short(cmd, input=""):
    rst = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input.encode("utf-8"))
    assert rst.returncode == 0, rst.stderr.decode("utf-8")
    return rst.stdout.decode("utf-8")


def prepare_command(tool, command):
    lang = tool.lang

    if not lang:
        cmd = tool.run + ' ' + command
    else:
        tool_path = "/app/" + settings.EXTERNAL_TOOLS_DIR + '/' + tool.directory
        filepath = tool_path + '/' + tool.run

        cmd = lang + ' ' + filepath + ' ' + command

    return cmd
