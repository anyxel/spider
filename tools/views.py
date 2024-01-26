from django.shortcuts import render

from tools.models import Tools


def index(request):
    if request.method == 'GET':
        tools = Tools.objects.all()

        return render(request, "tools.html", {
            'tools': tools,
        })
