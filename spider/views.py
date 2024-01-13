from django.shortcuts import render

from core.helper import run_command


def index(request):
    return render(request, "home.html", {})


def setup(request):
    output = run_command('./setup.sh')

    return render(request, "setup.html", {
        'output': output,
    })


def run(request):
    command = request.GET.get('cmd')

    if command:
        output = run_command(command)
    else:
        command = ''
        output = ''

    return render(request, "command.html", {
        'command': command,
        'output': output,
    })
