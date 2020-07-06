# -*- coding: utf-8 -*-
from __future__ import with_statement  # only for python 2.5

import contextlib
import datetime
import os
import shutil
import sys

from invoke import task
from invoke.util import cd
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

SETTINGS_FILE_BASE = 'pelicanconf.py'
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)

CONFIG = {
    'settings_base': SETTINGS_FILE_BASE,
    'settings_publish': 'publishconf.py',
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    'deploy_path': SETTINGS['OUTPUT_PATH'],
    # Github Pages configuration
    'github_pages_branch': 'master',
    'commit_message': "'Publish site on {}'".format(datetime.date.today().isoformat()),
    # Port for `serve`
    'port': 8000,
    # Don't delete github files
    'do_not_delete': ['.git', '.gitmodules', '.gitignore', 'LICENSE', 'README.md']
}


@contextlib.contextmanager
def chdir(dirname=None):
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG['deploy_path']):
        for filename in os.listdir(CONFIG['deploy_path']):
            if filename in CONFIG['do_not_delete']:
                continue
            file_path = os.path.join(CONFIG['deploy_path'], filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)


@task
def build(c):
    """Build local version of site"""
    c.run('pelican -s {settings_base}'.format(**CONFIG))


@task
def rebuild(c):
    """`build` with the delete switch"""
    c.run('pelican -d -s {settings_base}'.format(**CONFIG))


@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    c.run('pelican -r -s {settings_base}'.format(**CONFIG))


@task
def serve(c):
    """Serve site at http://localhost:$PORT/ (default port is 8000)"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG['deploy_path'],
        ('', CONFIG['port']),
        ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {port} ...\n'.format(**CONFIG))
    server.serve_forever()


@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)


@task
def preview(c):
    """Build production version of site"""
    c.run('pelican -s {settings_publish}'.format(**CONFIG))


@task
def livereload(c):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server
    build(c)
    server = Server()
    # Watch the base settings file
    server.watch(CONFIG['settings_base'], lambda: build(c))
    # Watch content source files
    content_file_extensions = ['.md', '.rst']
    for extension in content_file_extensions:
        content_blob = '{0}/**/*{1}'.format(SETTINGS['PATH'], extension)
        server.watch(content_blob, lambda: build(c))
    # Watch the theme's templates and static assets
    theme_path = SETTINGS['THEME']
    server.watch('{}/templates/*.html'.format(theme_path), lambda: build(c))
    static_file_extensions = ['.css', '.js']
    for extension in static_file_extensions:
        static_file = '{0}/static/**/*{1}'.format(theme_path, extension)
        server.watch(static_file, lambda: build(c))
    # Serve output path on configured port
    server.serve(port=CONFIG['port'], root=CONFIG['deploy_path'])


@task
def publish(c):
    """Publish to production via rsync"""
    c.run('pelican -s {settings_publish}'.format(**CONFIG))
    c.run(
        'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        '-e "ssh -p {ssh_port}" '
        '{} {ssh_user}@{ssh_host}:{ssh_path}'.format(
            CONFIG['deploy_path'].rstrip('/') + '/',
            **CONFIG))


@task(clean)
def github(c):
    """Publish to GitHub User Pages"""
    # Get the latest from both github projects
    c.run('git fetch')
    c.run('git pull')
    c.run('git submodule update')

    # Create the site
    preview(c)

    with chdir(CONFIG['deploy_path']):
        # Commit and publish the html site
        c.run('git add -A')
        c.run('git commit -am "{commit_message}"'.format(**CONFIG))
        c.run('git push')

    # Commit and publish the source project
    c.run('git add -A')
    c.run('git commit -am "{commit_message}"'.format(**CONFIG))
    c.run('git push')
