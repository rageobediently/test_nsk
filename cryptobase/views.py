from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cryptobase.models import Value
from django.core import serializers


@csrf_exempt
def get_high_low(request, pair):
    data = Value.objects.select_related('coin').filter(coin__name=pair).filter(is_hours=True)
    if data is None:
        response = {
            'error': 'Pair not found'
        }
        status = 404
    else:
        response = {'pair': pair, 'values': []}
        response['values'].append(get_dict('min',data.order_by('low').first()))
        response['values'].append(get_dict('max', data.order_by('high').last()))
        status = 200
    return JsonResponse(response, status=status)


def get_dict(type,obj):
    response = obj.json
    response['Type'] = type
    return response
