from django.shortcuts import render
from menu.models import MenuItem


def build_menu_tree(menu_items, parent=None):
    tree = []
    for item in menu_items:
        if item.parent_id == parent:
            children = build_menu_tree(menu_items, parent=item.id)
            tree.append({'item': item, 'children': children})
    return tree


def menu_view(request):
    all_items = MenuItem.objects.all()
    menu_tree = build_menu_tree(all_items)
    active_path = []
    return render(request, 'tree_menu/menu.html', {'menu_tree': menu_tree, 'active_path': active_path})
