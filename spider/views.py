from django.http import JsonResponse
from django.shortcuts import render

from core.helper import run_command, send_message_to_websocket


def home(request):
    return render(request, "home.html", {})


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

    if not command:
        message = "Please enter a command!"

    # Run
    try:
        if command:
            run_command(command)
    except Exception as e:
        message = str(e.args[0]) if e.args else "An unknown error occurred"
        run_command(message)

    data = {
        'message': message,
    }
    return JsonResponse(data)
