from django import template

register = template.Library()


@register.filter
def get_at_index(list, index):
    return list[index]


@register.filter
def get_range(value):
    if value:
        return [i + 1 for i in range(value)]
    else:
        return []


@register.filter
def add_str(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def get_cookies(request, arg):
    """concatenate arg1 & arg2"""
    return request.COOKIES.get(arg)


@register.filter
def get_session(request, arg):
    """concatenate arg1 & arg2"""
    return request.session.get(arg, "")


@register.filter
def modulo(num, val):
    return num % val