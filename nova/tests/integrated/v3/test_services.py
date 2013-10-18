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

from nova import db
from nova.openstack.common import timeutils
from nova.tests.api.openstack.compute.plugins.v3 import test_services
from nova.tests.integrated.v3 import api_sample_base


class ServicesJsonTest(api_sample_base.ApiSampleTestBaseV3):
    extension_name = "os-services"
    section_name = "Services"
    section_doc = ("Index, Update services. Use services extension to get "
                   "service information and status, and service can be "
                   "enabled or disabled.")

    def setUp(self):
        super(ServicesJsonTest, self).setUp()
        self.stubs.Set(db, "service_get_all",
                       test_services.fake_db_api_service_get_all)
        self.stubs.Set(timeutils, "utcnow", test_services.fake_utcnow)
        self.stubs.Set(db, "service_get_by_args",
                       test_services.fake_service_get_by_host_binary)
        self.stubs.Set(db, "service_update",
                       test_services.fake_service_update)

    def tearDown(self):
        super(ServicesJsonTest, self).tearDown()
        timeutils.clear_time_override()

    def test_services_list(self):
        """Return a list of all agent builds."""
        response = self._doc_do_get(
            'os-services', (), (),
            api_desc=('Return a list of all running services. Filter by host '
                      '& service name.'))
        subs = {'binary': 'nova-compute',
                'host': 'host1',
                'zone': 'nova',
                'status': 'disabled',
                'state': 'up'}
        subs.update(self._get_regexes())
        self._verify_response('services-list-get-resp', subs, response, 200)

    def test_service_enable(self):
        """Enable an existing agent build."""
        subs = {"host": "host1",
                'binary': 'nova-compute'}
        response = self._doc_do_put(
            'os-services/enable', (), (), 'service-enable-put-req', subs,
            api_desc='Enable scheduling for a service.')
        subs = {"host": "host1",
                "binary": "nova-compute"}
        self._verify_response('service-enable-put-resp', subs, response, 200)

    def test_service_disable(self):
        """Disable an existing agent build."""
        subs = {"host": "host1",
                'binary': 'nova-compute'}
        response = self._doc_do_put(
            'os-services/disable', (), (), 'service-disable-put-req', subs,
            api_desc='Disable scheduling for a service.')
        subs = {"host": "host1",
                "binary": "nova-compute"}
        self._verify_response('service-disable-put-resp', subs, response, 200)

    def test_service_disable_log_reason(self):
        """Disable an existing service and log the reason."""
        subs = {"host": "host1",
                'binary': 'nova-compute',
                'disabled_reason': 'test2'}
        response = self._doc_do_put(
            'os-services/disable-log-reason', (), (),
            'service-disable-log-put-req', subs,
            api_desc='Disable scheduling for a service with reason.')
        return self._verify_response('service-disable-log-put-resp',
                                     subs, response, 200)


class ServicesXmlTest(ServicesJsonTest):
    ctype = 'xml'
