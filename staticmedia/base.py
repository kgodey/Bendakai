import os
import posixpath

from django.conf import settings
from django.conf.urls.defaults import patterns


class StaticMediaNotFound(Exception): pass


def get_mount_points():
    """
    Get the available media mount points for the site.

    First, the mount points specified by the 'STATICMEDIA_MOUNTS'
    setting will be collected, after which each app in the
    'INSTALLED_APPS' setting is checked for a 'media' directory in the
    package source for static files to be served by the webserver. If
    this directory exists and is not a Python module, it is included
    as a mount point.
    """
    mounts = []

    url_prefix = getattr(settings, 'STATICMEDIA_URL', '/appmedia')
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]

    # collect mounts specified in the settings, we want these to be
    # first since they also serve as overrides for the app mounts
    for mount_url, mount_path in getattr(settings, 'STATICMEDIA_MOUNTS', []):
        if mount_url.endswith('/'):
            mount_url = mount_url[:-1]
        mounts.append((mount_url, mount_path))

    # collect static paths in each installed app.
    for app in settings.INSTALLED_APPS:
        # django apps are always module dirs
        app_label = app.rsplit('.', 1)[-1]
        app_module_path = __import__(app, {}, {}, ['']).__path__[0]
        app_static_path = os.path.join(app_module_path, 'media')
        if (os.path.lexists(app_static_path) and
            os.path.isdir(app_static_path) and not
            os.path.lexists(os.path.join(app_static_path, '__init__.py'))):

            # only consider the static dir in the app package source
            # if its not an importable python module itself since we
            # don't want to server python source.
            app_static_url = posixpath.join(url_prefix, app_label)
            mounts.append((app_static_url, app_static_path))

    return mounts


def resolve(media_name):
    """
    Resolve the given relative path against the available mount points.

    First, the mount points specified by the 'STATICMEDIA_MOUNTS'
    settings are checked, followed by static media mount points for
    each installed app that has one. The relative url is prefixed with
    each given mount point's path on the filesystem, and if a file
    exists in this location, then `media_name` is prefixed with the
    mount point's url prefix.

    Returns a tuple in the form (absolute_media_url, media_path).
    """
    if media_name.startswith('/'):
        media_name = media_name[1:]
    relative_path = media_name.replace('/', os.sep)

    for mount_url, mount_path in get_mount_points():
        media_path = os.path.join(mount_path, relative_path)
        if os.path.lexists(media_path):
            return (
                posixpath.join(mount_url, media_name),
                media_path)  

    raise StaticMediaNotFound(media_name)


def url(media_name):
    """
    Resolve the absolute url for the given static media.
    """
    return resolve(media_name)[0]


def path(media_name):
    """
    Resolve the path on the given static media.
    """
    return resolve(media_name)[1]


def serve(show_indexes=False, debug=False):
    """
    Generate static serve mounts for your assets.

    ``show_indexes`` gets passed to ``django.views.static.serve``.

    Example usage in your urlconf::

        import staticmedia

        urlpatterns = patterns('',
            # ... urls here
        ) + staticmedia.serve()
    """
    if debug and not settings.DEBUG:
        return patterns('')

    media_patterns = []
    for mount_url, mount_path in get_mount_points():
        if mount_url.startswith('/'):
            mount_url = mount_url[1:]
        media_patterns.append(
            ('^%s/(?P<path>.*)$' % mount_url, 'serve',
             {'document_root': mount_path, 'show_indexes': show_indexes}))
    return patterns('django.views.static', *media_patterns)
