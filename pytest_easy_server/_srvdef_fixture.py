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
Pytest fixture server_definition.
"""

from __future__ import absolute_import, print_function
import pytest

import easy_server

__all__ = ['server_definition']


@pytest.fixture(scope="module")
def server_definition(request):
    """
    Pytest fixture representing the set of server definitions for all servers
    to test against.

    The fixture resolves to a :class:`~pytest_easy_server.ServerDefinition`
    object representing a single server definition. Pytest invokes testcases
    using this fixture for all servers to test against.

    The servers to test against can be controlled with pytest command line
    options:

    .. code-block:: text

        --es-server-file=FILE   Use the specified server definition file.
                                Default: server.yml in current directory.

        --es-vault-file=FILE    Use the specified vault file.
                                Default: vault.yml in current directory.

        --es-nickname=NICKNAME  Use the server or server group with this
                                nickname to test against.
                                Default: default server or server group
                                specified in the server definition file.

    Returns:
      :class:`~easy_server.ServerDefinition`:
      Server definition for each server to test against.
    """
    sd = request.param
    assert isinstance(sd, easy_server.ServerDefinition)
    return sd