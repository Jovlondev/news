from django import template

register = template.Library()

@register.filter
def nfilter(query_set, atrs, *args, **kwargs):
    print("\n\n", query_set)
    print("\n\n", atrs)
    print("\n\n", args)
    print("\n\n", kwargs)
    print("\n\n")
    return 'Hello'
