from django.shortcuts import render

from core.helper import run_command, is_file_exists, download_and_unzip
from core.gitrepo import get_tool, install_dependencies


def index(request):
    get_cmd = ''
    output = ''

    repo = get_tool('sublist3r')
    lang = repo['lang']
    has_dependencies = repo['has_dependencies']
    repo_url = repo['url']
    repo_path = 'external-tools/' + repo['folder']
    filepath = repo_path + '/' + repo['filename']

    # Check program is installed
    check = is_file_exists(filepath)
    if not check:
        download_and_unzip(repo_url, 'external-tools')

    # Run commands
    try:
        get_cmd = request.GET.get('cmd')

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

    return render(request, "dashboard.html", {
        'command': get_cmd,
        'output': output,
    })
