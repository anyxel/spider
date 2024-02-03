import json

from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from core.command import prepare_command
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


def getTool(request):
    data = json.loads(request.body.decode('utf-8'))
    tool_name = data.get('tool', None)

    try:
        tool = Tool.objects.get(name=str(tool_name))
        tool_dict = model_to_dict(tool)

        tool_dict['command'] = prepare_command(tool, '')

        category = Category.objects.get(slug=str(tool.category_slug))
        tool_dict['category'] = category.name

        return JsonResponse(tool_dict, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'message': 'Tool not found'}, status=404)
