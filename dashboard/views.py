from django.shortcuts import render

from core.helper import run_command, is_file_exists, download_and_unzip


def index(request):
    get_cmd = ''
    output = ''

    return render(request, "dashboard.html", {
        'command': get_cmd,
        'output': output,
    })
