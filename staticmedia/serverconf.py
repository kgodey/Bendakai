import staticmedia


def nginx(fp=None, **options):
    directives = []
    for mount_point in staticmedia.get_mount_points():
        if not options:
            directives.append('location %s { alias %s; }' % mount_point)
        else:
            params = (' '.join(map(lambda i: '%s %s;' % i, options.items())),)
            directive = 'location %s { alias %s; %s }' % (mount_point + params)
            directives.append(directive)
    if fp:
        fp.write('\n'.join(directives))
    else:
        return '\n'.join(directives)


def apache(fp=None, **options):
    directives = []
    for mount_url, mount_path in staticmedia.get_mount_points():
        directives.append(
            'Alias "%s" "%s"' % (mount_url, mount_path))
        if 'diroptions' in options:
            directives.append(
                '<Directory "%s">\n    Options %s\n</Directory>' % (
                     mount_path, options['diroptions']))
    if fp:
        fp.write('\n'.join(directives))
    else:
        return '\n'.join(directives)


def lighttpd(fp=None, **options):
    directives = []

    for mount_point in staticmedia.get_mount_points():
        directives.append('alias.url += ( "%s" => "%s" )' % mount_point)

    if fp:
        fp.write('\n'.join(directives))
    else:
        return '\n'.join(directives)
