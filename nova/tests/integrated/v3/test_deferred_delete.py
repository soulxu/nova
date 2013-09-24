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


class DeferredDeleteSampleJsonTests(test_servers.ServersSampleBase):
    extension_name = "os-deferred-delete"
    section_name = 'Deferred Delete'
    section_doc = "Instance deferred delete."

    def setUp(self):
        super(DeferredDeleteSampleJsonTests, self).setUp()
        self.flags(reclaim_instance_interval=1)

    def test_restore(self):
        uuid = self._post_server()
        response = self._do_delete('servers/%s' % uuid)

        response = self._doc_do_post(
            'servers/%s/action', uuid, 'server_id', 'restore-post-req', {},
            api_desc="Restore a previously deleted instance.")
        self._verify_response('restore', {}, response, 202, has_response=False)
        self.assertEqual(response.read(), '')

    def test_force_delete(self):
        uuid = self._post_server()
        response = self._do_delete('servers/%s' % uuid)

        response = self._doc_do_post(
            'servers/%s/action', uuid, 'server_id', 'force-delete-post-req',
            {}, api_desc='Force delete of instance before deferred cleanup.')
        self._verify_response('force-delete', {}, response, 202,
                              has_response=False)
        self.assertEqual(response.read(), '')


class DeferredDeleteSampleXmlTests(DeferredDeleteSampleJsonTests):
        ctype = 'xml'
