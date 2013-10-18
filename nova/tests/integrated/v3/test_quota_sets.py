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

from nova.tests.integrated.v3 import api_sample_base


class QuotaSetsSampleJsonTests(api_sample_base.ApiSampleTestBaseV3):
    extension_name = "os-quota-sets"
    section_name = 'Quota Sets'
    section_doc = "Quotas management support."

    def test_show_quotas(self):
        # Get api sample to show quotas.
        response = self._doc_do_get('os-quota-sets/%s', 'fake_tenant',
                                    'tenant_id',
                                    api_desc='Shows quotas for tenant.')
        self._verify_response('quotas-show-get-resp', {}, response, 200)

    def test_show_quotas_defaults(self):
        # Get api sample to show quotas defaults.
        response = self._doc_do_get(
            'os-quota-sets/%s/defaults', 'fake_tenant', 'tenant_id',
            api_desc='Shows default quotas for tenant.')
        self._verify_response('quotas-show-defaults-get-resp',
                              {}, response, 200)

    def test_update_quotas(self):
        # Get api sample to update quotas.
        response = self._doc_do_put('os-quota-sets/%s', 'fake_tenant',
                                    'tenant_id', 'quotas-update-post-req',
                                    {}, api_desc='Updates quota for tenant.')
        self._verify_response('quotas-update-post-resp', {}, response, 200)

    def test_delete_quotas(self):
        # Get api sample to delete quota.
        response = self._doc_do_delete('os-quota-sets/%s', 'fake_tenant',
                                       'tenant_id',
                                       api_desc='Deletes quota for user.')
        self._verify_no_response('quota-delete', response, 204)
        self.assertEqual(response.read(), '')

    def test_update_quotas_force(self):
        # Get api sample to update quotas.
        response = self._doc_do_put('os-quota-sets/%s', 'fake_tenant',
                                    'tenant_id',
                                    'quotas-update-force-post-req', {},
                                    api_desc='Force update quota for tenant.')
        return self._verify_response('quotas-update-force-post-resp', {},
                                     response, 200)

    def test_show_quotas_for_user(self):
        # Get api sample to show quotas for user.
        response = self._doc_do_get('os-quota-sets/%s?user_id=%s',
                                    ('fake_tenant', 1),
                                    ('tenant_id', 'user_id'),
                                    api_desc='Shows quota for user')
        self._verify_response('user-quotas-show-get-resp', {}, response, 200)

    def test_delete_quotas_for_user(self):
        response = self._doc_do_delete('os-quota-sets/%s?user_id=%s',
                                       ('fake_tenant', 1),
                                       ('tenant_id', 'user_id'),
                                       api_desc='Deletes quota for user.')
        self._verify_no_response('quota-user-delete', response, 204)
        self.assertEqual(response.read(), '')

    def test_update_quotas_for_user(self):
        # Get api sample to update quotas for user.
        response = self._doc_do_put('os-quota-sets/%s?user_id=%s',
                                    ('fake_tenant', 1),
                                    ('tenant_id', 'user_id'),
                                    'user-quotas-update-post-req', {},
                                    api_desc='Updates quota for user.')
        return self._verify_response('user-quotas-update-post-resp', {},
                                     response, 200)


class QuotaSetsSampleXmlTests(QuotaSetsSampleJsonTests):
    ctype = "xml"
