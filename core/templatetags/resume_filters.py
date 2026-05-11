from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()

_STRIP_CHARS = '•·–—-* '

@register.filter
def as_bullets(value):
    """Render a newline-separated string as a styled <ul> bullet list.
    Strips common manual bullet characters (•, -, *, etc.) from line starts."""
    if not value:
        return ''
    lines = [line.strip().lstrip(_STRIP_CHARS) for line in value.splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return ''
    items = ''.join(f'<li>{escape(line)}</li>' for line in lines)
    return mark_safe(f'<ul class="resume-bullets">{items}</ul>')
