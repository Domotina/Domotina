from django import template

register = template.Library()


@register.simple_tag
def status_icon(event):
    return '<img src="' + event.get_status().icon + '"/>'