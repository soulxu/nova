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


class ServerUsageSampleJsonTest(test_servers.ServersSampleBase):
    extension_name = 'os-server-usage'
    section_name = 'Server Usage'
    section_doc = "Adds launched_at and terminated_at on Servers."

    def setUp(self):
        """setUp method for server usage."""
        super(ServerUsageSampleJsonTest, self).setUp()
        self.uuid = self._post_server()

    def test_show(self):
        response = self._doc_do_get(
            'servers/%s', self.uuid, 'server_id',
            api_desc="Returns server details by server id.")
        subs = self._get_regexes()
        subs['id'] = self.uuid
        subs['hostid'] = '[a-f0-9]+'
        self._verify_response('server-get-resp', subs, response, 200)

    def test_details(self):
        response = self._doc_do_get(
            'servers/detail', (), (),
            api_desc="Returns a list of server details for a given user.")
        subs = self._get_regexes()
        subs['id'] = self.uuid
        subs['hostid'] = '[a-f0-9]+'
        self._verify_response('servers-detail-resp', subs, response, 200)


class ServerUsageSampleXmlTest(ServerUsageSampleJsonTest):
    ctype = 'xml'
