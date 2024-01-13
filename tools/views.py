from django.shortcuts import render

from core.helper import run_command, is_file_exists, download_and_unzip
from core.gitrepo import get_tool, install_dependencies
from tools.models import Tools


def index(request):
    output = ''
    error_message = ''

    get_tool_name = request.GET.get('name')
    get_cmd = request.GET.get('cmd')

    if (not get_tool_name) or (not get_cmd):
        return render(request, "tools.html", {
            'command': get_cmd,
            'output': output,
            'error_message': 'Select a tool and enter command!',
        })

    try:
        tool = Tools.objects.get(name=str(get_tool_name))

        lang = tool.lang
        has_dependencies = tool.has_dependencies
        repo_url = tool.url
        repo_path = 'external-tools/' + tool.folder
        filepath = repo_path + '/' + tool.filename

        # Check program is installed
        check = is_file_exists(filepath)
        if not check:
            download_and_unzip(repo_url, 'external-tools')

        # Run commands
        try:

            if get_cmd:
                command = lang + ' ' + filepath + ' ' + get_cmd
                output = run_command(command)
        except Exception as e:
            error_message = str(e.args[0]) if e.args else "An unknown error occurred"

            if 'ModuleNotFoundError' in error_message:
                print('ModuleNotFoundError')

                if has_dependencies:
                    install_dependencies(repo_path)
            else:
                print(error_message)

    except Tools.DoesNotExist:
        error_message = "Tool not found"

    return render(request, "tools.html", {
        'command': get_cmd,
        'output': output,
        'error_message': error_message,
    })
