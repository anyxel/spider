import json

from django.http import JsonResponse
from django.shortcuts import render

from tools.models import Tool, Category


def index(request):
    if request.method == 'GET':
        return render(request, "tools.html")


def categories(request):
    data = list(Category.objects.values_list('name', flat=True))
    sorted_data = sorted(data, key=lambda x: str(x).lower())

    return JsonResponse(sorted_data, safe=False)


def tools(request):
    data = json.loads(request.body.decode('utf-8'))

    category_name = data.get('category', None)
    if category_name:
        category = Category.objects.get(name=str(category_name))
        category_slug = category.slug

        data = list(Tool.objects.filter(category_slug=category_slug).values_list('name', flat=True))
        data = sorted(data, key=lambda x: str(x).lower())
        return JsonResponse(data, safe=False)

    else:
        data = list(Tool.objects.values_list('name', flat=True))
        data = sorted(data, key=lambda x: str(x).lower())
        return JsonResponse(data, safe=False)
