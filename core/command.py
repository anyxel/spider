import subprocess

from core.helper import send_message_to_websocket


def run_command_bkp(cmd, input=""):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while process.poll() is None:
        line = process.stdout.readline().rstrip()
        if line:
            string_data = line.decode('utf-8')
            send_message_to_websocket(string_data)


def run_command_bkp1(cmd, input=""):
    rst = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input.encode("utf-8"))
    rst.returncode == 0, rst.stderr.decode("utf-8")
    return rst.stdout.decode("utf-8")


async def run_command_bkp2(cmd, input=""):
    try:
        cmd = cmd + " > tmp.txt"

        rst = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input.encode("utf-8"))

        rst.returncode == 0, rst.stderr.decode("utf-8")
        ss = rst.stdout.decode("utf-8")

        print(ss)

    except Exception as e:
        error_message = str(e.args[0]) if e.args else "An unknown error occurred"
        print(e.args[0])
