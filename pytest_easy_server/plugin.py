# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pytest plugin for pytest-easy-server project.
"""

from __future__ import absolute_import, print_function
import os
import pytest

import easy_server

DEFAULT_SERVER_FILE = 'es_server.yml'

DOCS_LINK = 'https://pytest-easy-server.readthedocs.io/'


def pytest_addoption(parser):
    """
    Add command line options and config (ini) parameters for this plugin.

    group.addoption() supports the same arguments as argparse.add_argument().
    """

    group = parser.getgroup('pytest-easy-server')
    group.description = "pytest-easy-server - " \
        "Pytest plugin for easy testing against servers, " \
        "see {}".format(DOCS_LINK)

    group.addoption(
        '--es-file',
        dest='es_file',
        metavar="FILE",
        action='store',
        default=DEFAULT_SERVER_FILE,
        help="""\
Path name of the easy-server file to be used.
Default: {fn} in current directory.
""".format(fn=DEFAULT_SERVER_FILE))

    group.addoption(
        '--es-nickname',
        dest='es_nickname',
        metavar="NICKNAME",
        action='store',
        default=None,
        help="""\
Nickname of the server or server group to test against.
Default: The default from the easy-server file.
""")


def fixtureid_es_server(fixture_value):
    """
    Return a fixture ID to be used by pytest for fixture `es_server()`.

    Parameters:

      fixture_value (:class:`~easy_server.Server`):
        The server the test runs against.
    """
    es_obj = fixture_value
    assert isinstance(es_obj, easy_server.Server)
    return "easy_server={0}".format(es_obj.nickname)


def pytest_generate_tests(metafunc):
    """
    Pytest plugin function to generate the tests for multiple servers in the
    server file.
    """

    if 'es_server' in metafunc.fixturenames:

        config = metafunc.config
        es_file = os.path.abspath(config.getvalue('es_file'))
        es_nickname = config.getvalue('es_nickname')

        if config.getvalue('verbose'):
            print("\npytest-easy-server: Using server file {fn}".
                  format(fn=es_file))

        # The following constructs place the pytest.exit() call outside of the
        # exception handling which avoids the well-known exception traceback
        # "During handling of the above exception, ...".

        exit_message = None
        try:
            esf_obj = easy_server.ServerFile(es_file)
        except easy_server.ServerFileException as exc:
            exit_message = str(exc)
        if exit_message:
            pytest.exit(exit_message)

        exit_message = None
        try:
            es_obj_list = esf_obj.list_default_servers() \
                if es_nickname is None else esf_obj.list_servers(es_nickname)
        except KeyError as exc:
            exit_message = str(exc)
        if exit_message:
            pytest.exit(exit_message)

        metafunc.parametrize(
            'es_server', es_obj_list, indirect=True,
            ids=fixtureid_es_server)
