from django.http import JsonResponse
from django.shortcuts import render

from core.helper import run_command, send_message_to_websocket


def index(request):
    return render(request, "home.html", {})


def setup(request):
    output = run_command('./setup.sh')

    return render(request, "setup.html", {
        'output': output,
    })


def terminal2(request):
    return render(request, "test.html", )


def terminal(request):
    # Index
    if request.method == 'GET':
        return render(request, "terminal.html", )

    # POST method
    if request.method == 'POST':

        data = {
            'message': 'Hello, this is a JSON response!',
            'status': 'success'
        }

        command = request.POST.get('cmd')

        if command:
            try:
                run_command(command)
                # asyncio.run(run_command(command))

            except Exception as e:
                error_message = str(e.args[0]) if e.args else "An unknown error occurred"

                send_message_to_websocket(e)
        else:
            format_message = "<div class='command-danger'>Please enter a command!</div>"
            send_message_to_websocket(format_message)

        # Ajax response
        return JsonResponse(data)
