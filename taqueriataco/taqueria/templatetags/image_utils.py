from urllib.parse import urlparse
from django import template

register = template.Library()


@register.filter
def direct_image_url(url):
    """Attempt to convert known image page URLs (e.g. imgur) to a direct image URL.

    - If URL already looks like an image (ends with .jpg/.png/.gif/.webp), return as-is.
    - For Imgur single-image pages like `https://imgur.com/abc123` convert to
      `https://i.imgur.com/abc123.jpg` (common case). Album links (`/a/`) cannot be
      converted automatically and will return an empty string so template can show
      a placeholder.
    """
    if not url:
        return ''

    url = url.strip()
    lowered = url.lower()
    # If it already ends with an image extension, return as-is
    for ext in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
        if lowered.endswith(ext):
            return url

    try:
        parsed = urlparse(url)
    except Exception:
        return url

    # Handle Imgur album or page links
    host = parsed.netloc.lower()
    path = parsed.path.lstrip('/')

    if 'imgur.com' in host:
        # album links like /a/<id> cannot be mapped to a single image
        if path.startswith('a/') or path == 'a':
            return ''
        # For direct imgur pages like /<id> -> try i.imgur.com/<id>.jpg
        if path:
            # guess jpg; if that fails user should provide direct link
            return f'https://i.imgur.com/{path}.jpg'

    # Fallback: return original URL and let browser try it
    return url
