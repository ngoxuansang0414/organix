from django import template

register = template.Library()

@register.filter(name="weight")
def weight(w):
    if w >= 1000:
        w = float(w)/1000
        return f"{w} kg" 
    else:
        return f"{w} g"