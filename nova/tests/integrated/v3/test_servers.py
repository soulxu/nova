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

from nova.tests.image import fake
from nova.tests.integrated.v3 import api_sample_base


class ServersSampleBase(api_sample_base.ApiSampleTestBaseV3):
    def _post_server(self):
        subs = {
            'image_id': fake.get_valid_image_id(),
            'host': self._get_host(),
            'glance_host': self._get_glance_host()
        }
        response = self._do_post('servers', 'server-post-req', subs)
        subs = self._get_regexes()
        return self._verify_response('server-post-resp', subs, response, 202)

    def _doc_post_server(self, api_desc):
        subs = {
            'image_id': fake.get_valid_image_id(),
            'host': self._get_host(),
            'glance_host': self._get_glance_host()
        }
        response = self._doc_do_post('servers', (), (), 'server-post-req',
                                     subs,
                                     api_desc=api_desc)
        subs = self._get_regexes()
        return self._verify_response('server-post-resp', subs, response, 202)


class ServersSampleJsonTest(ServersSampleBase):
    sample_dir = 'servers'
    extension_name = 'servers'
    section_name = 'Servers'
    section_doc = 'Creates, shows, lists, deletes and updates servers.'

    def test_servers_post(self):
        return self._doc_post_server('Create new server.')

    def test_servers_get(self):
        uuid = self.test_servers_post()
        response = self._doc_do_get(
            'servers/%s', uuid, 'server_id',
            api_desc="Returns server details by server id.")
        subs = self._get_regexes()
        subs['hostid'] = '[a-f0-9]+'
        subs['id'] = uuid
        subs['hypervisor_hostname'] = r'[\w\.\-]+'
        subs['mac_addr'] = '(?:[a-f0-9]{2}:){5}[a-f0-9]{2}'
        self._verify_response('server-get-resp', subs, response, 200)

    def test_servers_list(self):
        uuid = self._post_server()
        response = self._doc_do_get(
            'servers', (), (),
            api_desc=("Returns a list of server names and ids for a given "
                      "user."))
        subs = self._get_regexes()
        subs['id'] = uuid
        self._verify_response('servers-list-resp', subs, response, 200)

    def test_servers_details(self):
        uuid = self._post_server()
        response = self._doc_do_get(
            'servers/detail', (), (),
            api_desc="Returns a list of server details for a given user.")
        subs = self._get_regexes()
        subs['hostid'] = '[a-f0-9]+'
        subs['id'] = uuid
        subs['hypervisor_hostname'] = r'[\w\.\-]+'
        subs['mac_addr'] = '(?:[a-f0-9]{2}:){5}[a-f0-9]{2}'
        self._verify_response('servers-details-resp', subs, response, 200)


class ServersSampleXmlTest(ServersSampleJsonTest):
    ctype = 'xml'


class ServersSampleAllExtensionJsonTest(ServersSampleJsonTest):
    all_extensions = True
    section_name = 'Servers with all extensions'


class ServersSampleAllExtensionXmlTest(ServersSampleXmlTest):
    all_extensions = True
    section_name = 'Servers with all extensions'
