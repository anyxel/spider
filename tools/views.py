from django.http import JsonResponse
from django.shortcuts import render

from tools.models import Tool, Category


def index(request):
    if request.method == 'GET':
        categories = Category.objects.all().order_by('name')
        tools = Tool.objects.all().order_by('name')

        return render(request, "tools.html", {
            'categories': categories,
            'tools': tools,
        })


def categories(request):
    data = list(Category.objects.values_list('name', flat=True))

    return JsonResponse(data, safe=False)


def tools(request):
    data = list(Tool.objects.values_list('name', flat=True))

    return JsonResponse(data, safe=False)
