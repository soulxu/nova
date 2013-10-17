# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright 2012 Nebula, Inc.
# Copyright 2013 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from nova.tests.integrated.v3 import test_servers


class ServerDiagnosticsSamplesJsonTest(test_servers.ServersSampleBase):
    extension_name = "os-server-diagnostics"
    section_name = 'Server Diagnostics'
    section_doc = ("Allow Admins to view server diagnostics through server "
                   "action.")

    def test_server_diagnostics_get(self):
        uuid = self._post_server()
        response = self._doc_do_get('servers/%s/os-server-diagnostics', uuid,
                                    'server_id',
                                    api_desc='Get diagnostics of a server')
        subs = self._get_regexes()
        self._verify_response('server-diagnostics-get-resp', subs,
                              response, 200)


class ServerDiagnosticsSamplesXmlTest(ServerDiagnosticsSamplesJsonTest):
    ctype = "xml"
