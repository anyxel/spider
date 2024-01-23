import os

from django.http import JsonResponse
from django.shortcuts import render

from core.helper import run_command, is_file_exists, download_and_unzip, send_message_to_websocket, install_dependencies
from tools.models import Tools


def index(request):
    output = ''
    error_message = ''

    get_tool_name = request.POST.get('name')
    get_cmd = request.POST.get('cmd')

    # Index
    if request.method == 'GET':
        return render(request, "tools.html", {
            'command': get_cmd,
            'output': output,
            'error_message': error_message,
        })

    # POST method
    if request.method == 'POST':
        message = 'Success'

        if (not get_tool_name) or (not get_cmd):
            message = "Select a tool and enter command!"
            send_message_to_websocket(message)

        try:
            tool = Tools.objects.get(name=str(get_tool_name))

            lang = tool.lang
            repo_path = os.getenv('EXTERNAL_TOOLS_DIR') + '/' + tool.folder
            filepath = repo_path + '-' + tool.branch + '/' + tool.filename

            # Check program is installed
            check = is_file_exists(filepath)
            if not check:
                download_and_unzip(tool)

            # Run commands
            try:
                if get_cmd:
                    command = lang + ' ' + filepath + ' ' + get_cmd

                    run_command(command)
            except Exception as e:
                message = str(e.args[0]) if e.args else "An unknown error occurred"

                if "ModuleNotFoundError" in error_message:
                    send_message_to_websocket("ModuleNotFoundError")
                    send_message_to_websocket("Installing the modules...")

                    install_dependencies(repo_path)

        except Tools.DoesNotExist:
            message = "Tool not found"

        # Ajax response
        data = {
            'message': message,
        }
        return JsonResponse(data)
