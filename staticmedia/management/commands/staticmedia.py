import sys

from django.core import management


staticmedia = sys.modules['staticmedia']
serverconf = __import__('%s.serverconf' % staticmedia.__name__, {}, {}, [''])


HELP_TEXT = r"""
  staticmedia <subcommand> [options]

  'staticmedia' or 'staticmedia list-mounts' lists configued mount points.
  'staticmedia apache-conf' generates mounts for Apache.
  'staticmedia nginx-conf' generates mounts for nginx.
  'staticmedia lighttpd-conf' generates mounts for Lighttpd.
"""


class Command(management.BaseCommand):
    help = 'Manage dynamic assets for this site'
    args = '<list-mounts|apache-conf|nginx-conf|lighttpd-conf>'

    def handle(self, *args, **options):
        if not args:
            subcommand = 'list-mounts'
        else:
            subcommand = args[0]
            args = args[1:]

        options = {}
        for arg in args:
            if '=' in arg:
                options.update([arg.split('=', 1)])

        if subcommand == 'list-mounts':
            self.list_mounts()
        elif subcommand == 'apache-conf':
            self.generate_conf('apache', **options)
        elif subcommand == 'nginx-conf':
            self.generate_conf('nginx', **options)
        elif subcommand == 'lighttpd-conf':
            self.generate_conf('lighttpd', **options)

    def list_mounts(self):
        for mount_url, mount_path in staticmedia.get_mount_points():
            print '%s\t%s' % (mount_url, mount_path)

    def generate_conf(self, server, **options):
        getattr(serverconf, server)(sys.stdout, **options)

    def usage(self, subcommand):
        return HELP_TEXT
