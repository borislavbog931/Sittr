from django import template
from django.utils.safestring import mark_safe
import math

register = template.Library()


@register.filter
def stars_html_5(rating_10):
    if rating_10 is None:
        return ""

    try:
        r10 = float(rating_10)
    except (TypeError, ValueError):
        return ""

    r10 = max(0.0, min(10.0, r10))

    stars = r10 / 2.0

    full = int(math.floor(stars))
    frac = stars - full

    half = 0
    if frac >= 0.75:
        full += 1
    elif frac >= 0.25:
        half = 1

    full = min(full, 5)
    empty = 5 - full - half

    icons = []
    icons += ['<i class="bi bi-star-fill"></i>'] * full
    icons += ['<i class="bi bi-star-half"></i>'] * half
    icons += ['<i class="bi bi-star"></i>'] * empty

    return mark_safe("".join(icons))
