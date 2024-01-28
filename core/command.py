from django.conf import settings


def prepare_command(tool, command):
    lang = tool.lang

    if not lang:
        cmd = tool.run + ' ' + command
    else:
        tool_path = "/app/" + settings.EXTERNAL_TOOLS_DIR + '/' + tool.folder
        filepath = tool_path + '/' + tool.run

        cmd = lang + ' ' + filepath + ' ' + command

    return cmd
