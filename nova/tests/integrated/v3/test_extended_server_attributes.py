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


class ExtendedServerAttributesJsonTest(test_servers.ServersSampleBase):
    extension_name = "os-extended-server-attributes"
    section_name = 'Extended Server Attributes'
    section_doc = "Extended Server Attributes support."

    def test_show(self):
        uuid = self._post_server()

        response = self._doc_do_get(
            'servers/%s', uuid, 'server_id',
            api_desc="Returns server details by server id.")
        subs = self._get_regexes()
        subs['hostid'] = '[a-f0-9]+'
        subs['id'] = uuid
        subs['instance_name'] = 'instance-\d{8}'
        subs['hypervisor_hostname'] = r'[\w\.\-]+'
        self._verify_response('server-get-resp', subs, response, 200)

    def test_detail(self):
        uuid = self._post_server()

        response = self._doc_do_get(
            'servers/detail', (), (),
            api_desc="Returns a list of server details for a given user.")
        subs = self._get_regexes()
        subs['hostid'] = '[a-f0-9]+'
        subs['id'] = uuid
        subs['instance_name'] = 'instance-\d{8}'
        subs['hypervisor_hostname'] = r'[\w\.\-]+'
        self._verify_response('servers-detail-resp', subs, response, 200)


class ExtendedServerAttributesXmlTest(ExtendedServerAttributesJsonTest):
    ctype = 'xml'
