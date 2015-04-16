from django import template

register = template.Library()


@register.simple_tag
def status_icon(event):
    return '<img src="' + event.get_status().icon + '"/>'

@register.simple_tag
def query_params(alarms, events, sensor_type, floor):
    params = []
    if alarms is not None:
        params.append('alarm_page=%d' % alarms)
    if events is not None:
        params.append('event_page=%d' % events)
    if sensor_type is not None:
        params.append('type=%d' % sensor_type.pk)
    if floor is not None:
        params.append('floor_page=%d' % floor)
    if params:
        return '?'+('&'.join(params))
    else:
        return ''