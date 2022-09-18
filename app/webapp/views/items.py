from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from webapp.models import Item


def items_view(request: WSGIRequest):
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'items.html', context)


def item_view(request: WSGIRequest):
    pk = request.GET.get('pk')
    try:
        item = Item.objects.get(pk=pk)
        date = str(item.date_to_do)
        return render(request, 'item.html', context={'item': item, 'date': date})
    except ObjectDoesNotExist:
        item = None
        return render(request, 'item.html', context={'item': item})


def add_view(request: WSGIRequest):
    if request.method == 'GET':
        return render(request, 'item_create.html')
    item_data = {
        'description': request.GET.get('description'),
        'state': request.GET.get('state'),
        'date_to_do': request.GET.get('date_to_do')
    }
    item = Item.objects.create(**item_data)
    return redirect(f'/item/?pk={item.pk}')


def edit_view(request: WSGIRequest):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        item = Item.objects.get(pk=pk)
        date = str(item.date_to_do)
        return render(request, 'edit_item.html', context={'item': item, 'date': date})
    item = Item.objects.get(pk=request.POST.get('pk'))
    item.description = request.POST.get('description')
    item.state = request.POST.get('state')
    item.date_to_do = request.POST.get('date_to_do')
    item.save()
    return redirect(f'/items/item/?pk={item.pk}')


def delete_view(request: WSGIRequest):
    pk = request.GET.get('pk')
    item = Item.objects.get(pk=pk)
    item.delete()
    return redirect('items_view')