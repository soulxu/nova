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

from oslo.config import cfg

from nova.tests.integrated.v3 import test_servers

CONF = cfg.CONF


class ShelveJsonTest(test_servers.ServersSampleBase):
    extension_name = "os-shelve"
    section_name = 'Shelve'
    section_doc = ("Instance shelve mode.Shelving will power down the "
                   "instance, and snapshot if not volume backed."
                   "Unshelving will restore the instance, which may involve "
                   "re-scheduling and rebuilding it from a snapshot.")

    def setUp(self):
        super(ShelveJsonTest, self).setUp()
        # Don't offload instance, so we can test the offload call.
        CONF.shelved_offload_time = -1

    def _test_server_action(self, uuid, action, api_desc=None):
        response = self._doc_do_post(
            'servers/%s/action', uuid, 'server_id',
            'os-shelve',
            {'action': action},
            api_desc=api_desc)
        if api_desc:
            self._verify_no_response('os-shelve-%s' % action, response, 202)

    def test_shelve(self):
        uuid = self._post_server()
        self._test_server_action(uuid, 'shelve',
                                 "Move an instance into shelved mode.")

    def test_shelve_offload(self):
        uuid = self._post_server()
        self._test_server_action(uuid, 'shelve')
        self._test_server_action(
            uuid, 'shelve_offload',
            "Force removal of a shelved instance from the compute node.")

    def test_unshelve(self):
        uuid = self._post_server()
        self._test_server_action(uuid, 'shelve')
        self._test_server_action(
            uuid, 'unshelve',
            "Restore an instance from shelved mode.")


class ShelveXmlTest(ShelveJsonTest):
    ctype = 'xml'
