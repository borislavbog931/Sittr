import os

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static as django_static

register = template.Library()


@register.simple_tag
def static_v(path):
    """Like {% static %}, but appends the file's mtime as a cache-busting
    query param in DEBUG so browsers can't serve a stale disk-cached copy
    across edits during development."""
    url = django_static(path)
    if settings.DEBUG:
        absolute_path = finders.find(path)
        if absolute_path:
            try:
                url = f"{url}?v={int(os.path.getmtime(absolute_path))}"
            except OSError:
                pass
    return url
