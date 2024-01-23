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
        tools = Tools.objects.all()

        return render(request, "tools.html", {
            'tools': tools,
        })

    # POST method
    if request.method == 'POST':
        success = True
        message = 'Success'

        if (not get_tool_name) or (not get_cmd):
            success = False
            message = "Select a tool and enter command!\r\n"
            send_message_to_websocket(message)

            # Ajax response
            data = {
                'success': success,
                'message': message,
            }
            return JsonResponse(data)

        try:
            tool = Tools.objects.get(name=str(get_tool_name))

            lang = tool.lang
            tool_path = os.getenv('EXTERNAL_TOOLS_DIR') + '/' + tool.folder
            filepath = tool_path + '/' + tool.filename

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
                send_message_to_websocket(message + '\r\n')

        except Tools.DoesNotExist:
            success = False
            message = "Tool not found"

        # Ajax response
        data = {
            'success': success,
            'message': message,
        }
        return JsonResponse(data)
