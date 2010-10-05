"""
Template tag for dynamically loading static media.
"""
import sys

from django import template
from django.core.cache import cache
from django.utils import functional

staticmedia = sys.modules['staticmedia']


register = template.Library()


class MediaNode(template.Node):
    """
    Finds the first instance of the static media on the filesystem.

    See `staticmedia.resolve` docstring.

    This tag uses the cache framework as medias are unlikely to change
    very often, and templates will redundantly call specific static
    media (i.e. a button image).
    """
    url = 0
    path = 1

    def __init__(
        self, url_or_path, media_name, asvar=None, fail_silently=False):

        self.url_or_path = url_or_path
        self.media_name = media_name
        self.asvar = asvar
        self.fail_silently = fail_silently

    def render(self, context):
        """
        Return the dynamic media url directly or as a context variable
        """
        media_name = self.media_name.resolve(context)
        # use caching framework to save the media path
        media_url_path = cache.get('staticmedia:%s' % media_name)
        if not media_url_path:
            try:
                media_url_path = staticmedia.resolve(media_name)
            except staticmedia.StaticMediaNotFound, error:
                if not self.fail_silently:
                    raise
                else:
                    media_url_path = None
            if media_url_path:
                cache.set('staticmedia:%s' % media_name, media_url_path)

        if media_url_path:
            value = media_url_path[self.url_or_path]
        else:
            value = u''

        if self.asvar:
            context[self.asvar] = value
            return u''
        else:
            return value


def _media(parser, token, url_or_path=None):
    """
    {% mediaurl %} and {% mediapath %} tag

    Viable forms::

        {% media(url|path) "media_name" %}
        {% media(url|path) "media_name" as <context_variable> %}
        {% media(url|path) <from_template.variable> as <context_variable> %}
        {% media(url|path) ... fail_silently %}

    Where the first just returns the url or path and the second loads
    it into a template context variable. You can also pass template
    variables that resolves the url or path of a resource as the first
    argument. If 'fail_silently' is one of the tokens, the
    ``StaticMediaNotFound`` exception will be supressed and an empty
    string will be returned instead.
    """
    tokens = token.split_contents()

    if tokens[-1] == 'fail_silently':
        fail_silently = True
        tokens = tokens[:-1]
    else:
        fail_silently = False

    if len(tokens) > 4:
        raise template.TemplateSyntaxError(
            '%s tag given wrong number of arguments' % tokens[0])
    if len(tokens) == 1:
        raise template.TemplateSyntaxError(
            '%s tag takes 1 or 3 arguments: \'x\', or \'x as y\'')

    media_name = parser.compile_filter(tokens[1])
    if len(tokens) == 4:
        asvar = tokens[3]
    else:
        asvar = None

    return MediaNode(url_or_path, media_name, asvar, fail_silently)


register.tag('mediaurl', functional.curry(_media, url_or_path=MediaNode.url))
register.tag('mediapath', functional.curry(_media, url_or_path=MediaNode.path))
