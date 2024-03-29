from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from core.command import prepare_command, run_command_short, run_command
from tools.models import Tool


def home(request):
    app_name = "Anyxel Spider"
    return render(request, "home.html", {
        "app_name": app_name
    })


def setup(request):
    output = run_command_short('./setup.sh')

    return render(request, "setup.html", {
        'output': output,
    })


def terminal(request):
    return render(request, "terminal.html", )


def runCommand(request):
    command_type = request.POST.get('type')
    tool_name = request.POST.get('tool')
    command = request.POST.get('command')

    tool = None
    if tool_name:
        tool = Tool.objects.get(name=str(tool_name))

    # Run
    try:
        if command_type == 'install':
            data = {
                'success': False,
                'command': "cd /app && ./tools/scripts/" + tool.script
            }
            return JsonResponse(data)

        elif command_type == 'openDir':
            if tool.directory:
                message = 'Success'
                cmd = "cd /app/" + settings.EXTERNAL_TOOLS_DIR + '/' + tool.directory
            else:
                message = 'No directory found for this tool!'
                cmd = ""

            data = {
                'success': False,
                'message': message,
                'command': cmd
            }
            return JsonResponse(data)

        else:
            cmd = prepare_command(tool, command)
            data = {
                'success': True,
                'command': cmd,
            }
            return JsonResponse(data)
    except Exception as e:
        message = str(e.args[0]) if e.args else "An unknown error occurred"
        run_command(message)

    data = {
        'message': message,
    }
    return JsonResponse(data)
