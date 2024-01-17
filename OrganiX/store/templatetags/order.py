from django import template
import datetime

register = template.Library()

@register.filter(name='order_date')
def order_date(date):
    return date.strftime("%H:%M, %d-%m-%Y")

