from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect


from . import models
from . import forms


def menu_list(request):
    menus = models.Menu.objects.all().prefetch_related('items')
    return render(request,
                  'menu/list_all_current_menus.html',
                  {'menus': menus})


def menu_detail(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    item = get_object_or_404(models.Item.objects.select_related(), pk=pk)
    return render(request, 'menu/item_detail.html', {'item': item})


def create_new_menu(request):
    form = forms.MenuForm()
    if request.method == "POST":
        form = forms.MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect('menu:menu_detail', pk=menu.pk)
    return render(request, 'menu/menu_form.html', {'form': form})


def edit_menu(request, pk):
    try:
        menu = models.Menu.objects.get(pk=pk)
    except ObjectDoesNotExist:
        menu = None
    form = forms.MenuForm(instance=menu)
    if request.method == "POST":
        form = forms.MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu = form.save()
            return redirect('menu:menu_detail', pk=menu.pk)

    return render(request, 'menu/menu_form.html', {
        'menu': menu,
        'form': form, })


def edit_item(request, pk):
    try:
        item = models.Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        item = None
    form = forms.ItemForm(instance=item)
    if request.method == 'POST':
        form = forms.ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect('menu:item_detail', pk=item.pk)
    return render(request,
                  'menu/item_form.html',
                  {'item': item, 'form': form})
