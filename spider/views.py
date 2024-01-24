import os

from django.http import JsonResponse
from django.shortcuts import render

from core.helper import run_command, send_message_to_websocket, re_install
from tools.models import Tools


def home(request):
    app_name = os.getenv("APP_NAME")
    return render(request, "home.html", {
        "app_name": app_name
    })


def setup(request):
    output = run_command('./setup.sh')

    return render(request, "setup.html", {
        'output': output,
    })


def terminal(request):
    return render(request, "terminal.html", )


def runCommand(request):
    message = 'Success'
    command = request.POST.get('command')
    tool_name = request.POST.get('tool')

    if not command:
        message = "Please enter a command!"

    # Run
    try:
        if command:
            if command == 'reinstall':
                tool = Tools.objects.get(name=str(tool_name))

                send_message_to_websocket('Re-Installing ' + str(tool.name) + '...\r\n')

                re_install(tool)
            else:
                run_command(command)
    except Exception as e:
        message = str(e.args[0]) if e.args else "An unknown error occurred"
        run_command(message)

    data = {
        'message': message,
    }
    return JsonResponse(data)
