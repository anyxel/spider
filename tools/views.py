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
        data = {
            'message': 'Hello, this is a JSON response!',
            'status': 'success'
        }

        if (not get_tool_name) or (not get_cmd):
            format_message = "<div class='command-danger'>Select a tool and enter command!</div>"
            send_message_to_websocket(format_message)

        try:
            tool = Tools.objects.get(name=str(get_tool_name))

            lang = tool.lang
            repo_path = 'external-tools/' + tool.folder
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
                error_message = str(e.args[0]) if e.args else "An unknown error occurred"
                print(error_message)

                if "ModuleNotFoundError" in error_message:
                    send_message_to_websocket("ModuleNotFoundError")
                    send_message_to_websocket("Installing the modules...")

                    install_dependencies(repo_path)

        except Tools.DoesNotExist:
            error_message = "Tool not found"

        # Ajax response
        return JsonResponse(data)
