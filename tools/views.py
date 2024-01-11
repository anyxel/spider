from django.http import HttpResponse
from django.shortcuts import render

from spider.helper import run_command


def index(request):
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
    # return HttpResponse('k:' + output)
