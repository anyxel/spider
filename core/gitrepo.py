from core.helper import run_command
from tools.models import Tools


def get_tool(name):
    sublist3r = {
        "lang": 'python',
        "name": 'Sublist3r',
        "url": 'https://github.com/aboul3la/Sublist3r/archive/master.zip',
        "folder": 'Sublist3r-master',
        "filename": 'sublist3r.py',
        "has_dependencies": True,
    }

    repositories = {
        "sublist3r": sublist3r,
    }

    return repositories[name]


# def install_dependencies(repo_path):
#     try:
#         command = 'cd ' + repo_path + ' && pip install -r requirements.txt'
#         print(command)
#
#         output = run_command(command)
#
#         print('ModuleNotFoundError')
#     except Exception as e:
#         error_message = str(e.args[0]) if e.args else "An unknown error occurred"
#
#         print(error_message)
