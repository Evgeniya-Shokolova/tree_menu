from django import template
from menu.models import MenuItem

register = template.Library()


def build_menu_tree(menu_items):
    """
    Строит словарь из id -> пункт меню.
    Рекурсивно добавляет детей к каждому пункту.
    """
    items = {item.id: {'item': item, 'children': []} for item in menu_items}
    root_items = []

    for item in menu_items:
        if item.parent_id:
            items[item.parent_id]['children'].append(items[item.id])
        else:
            root_items.append(items[item.id])
    return root_items


def find_path(root_items, current_url):
    """
    Находит путь от корня к активному пункту по url.
    Возвращает множество id элементов меню, входящих в путь.
    """
    result = set()
    active_item_id = None

    def dfs(node, path):
        nonlocal active_item_id
        node_url = node['item'].get_url()
        if node_url == current_url:
            for p in path + [node['item'].id]:
                result.add(p)
            active_item_id = node['item'].id
            return True
        for child in node['children']:
            if dfs(child, path + [node['item'].id]):
                return True
        return False

    for node in root_items:
        if dfs(node, []):
            break
    return result, active_item_id


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Template tag для отображения древовидного меню.
    """
    try:

        menu = MenuItem.objects.get(name=menu_name)
        items = list(MenuItem.objects.filter(menu=menu).select_related('parent'))
    except MenuItem.DoesNotExist:
        return {'menu_tree': [], 'active_path': []}

    request = context['request']
    current_url = request.path
    active_item = None
    path_ids = set()
    for item in items:
        if item.get_url() == current_url:
            active_item = item
            break
    while active_item:
        path_ids.add(active_item.id)
        active_item = active_item.parent

    menu_tree = build_menu_tree(items)

    return {
        'menu_tree': menu_tree,
        'active_path': path_ids,
        'current_url': current_url,
    }
