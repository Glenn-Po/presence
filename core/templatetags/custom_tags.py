from django import template

register = template.Library()


@register.filter
def nth_split(value: str, index: int):
    # split the value by whitespace and return the first item
    array = value.split()
    if len(array) <= index:
        return ''
    return array[index]


@register.filter
def str_equal(value: str, arg: str):
    return arg == value
