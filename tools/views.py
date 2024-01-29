from django.shortcuts import render

from tools.models import Tool


def index(request):
    if request.method == 'GET':
        tools = Tool.objects.all().order_by('name')

        return render(request, "tools.html", {
            'tools': tools,
        })
