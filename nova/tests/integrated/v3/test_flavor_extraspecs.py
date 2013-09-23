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


class FlavorExtraSpecsSampleJsonTests(api_sample_base.ApiSampleTestBaseV3):
    extension_name = 'flavor-extra-specs'
    section_name = 'Flavor Extra Specs'
    section_doc = "Create, delete, update, list extra specs of flavor."

    def _flavor_extra_specs_create(self):
        subs = {'value1': 'value1',
                'value2': 'value2'
        }
        response = self._doc_do_post(
            'flavors/%s/flavor-extra-specs', 1,
            'flavor_id', 'flavor-extra-specs-create-req', subs,
            api_desc='Create and update flavor extra specs')
        self._verify_response('flavor-extra-specs-create-resp',
                              subs, response, 201)

    def test_flavor_extra_specs_get(self):
        subs = {'value1': 'value1'}
        self._flavor_extra_specs_create()
        response = self._doc_do_get(
            'flavors/%s/flavor-extra-specs/%s', (1, 'key1'),
            ('flavor_id', 'flavor_extra_spec_key'),
            api_desc='Show an extra spec for specified flavor by the key')
        self._verify_response('flavor-extra-specs-get-resp',
                              subs, response, 200)

    def test_flavor_extra_specs_list(self):
        subs = {'value1': 'value1',
                'value2': 'value2'
        }
        self._flavor_extra_specs_create()
        response = self._doc_do_get(
            'flavors/%s/flavor-extra-specs', 1, 'flavor_id',
            api_desc='List all extra specs for specified flavor')
        self._verify_response('flavor-extra-specs-list-resp',
                              subs, response, 200)

    def test_flavor_extra_specs_create(self):
        self._flavor_extra_specs_create()

    def test_flavor_extra_specs_update(self):
        subs = {'value1': 'new_value1'}
        self._flavor_extra_specs_create()
        response = self._doc_do_put(
            'flavors/%s/flavor-extra-specs/%s', (1, 'key1'),
            ('flavor_id', 'flavor_extra_spec_key'),
            'flavor-extra-specs-update-req',
            subs, api_desc='Update specified extra spec value by the key')
        self._verify_response('flavor-extra-specs-update-resp',
                              subs, response, 200)

    def test_flavor_extra_specs_delete(self):
        self._flavor_extra_specs_create()
        response = self._doc_do_delete(
            'flavors/%s/flavor-extra-specs/%s', (1, 'key1'),
            ('flavor_id', 'flavor_extra_spec_key'),
            api_desc='Delete an extra spec by the key')
        self._verify_delete_response('flavor-extra-sepc-delete', response,
                                     204)
        self.assertEqual(response.read(), '')


class FlavorExtraSpecsSampleXmlTests(FlavorExtraSpecsSampleJsonTests):
    ctype = 'xml'
