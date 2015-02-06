from django import template

register = template.Library()


@register.filter
def get_at_index(list, index):
    return list[index]


@register.filter
def get_range(value):
    return [i + 1 for i in range(value)]