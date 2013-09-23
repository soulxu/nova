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


class FlavorsSampleJsonTest(api_sample_base.ApiSampleTestBaseV3):
    extension_name = 'flavors'
    sample_dir = 'flavors'
    section_name = 'Flavors'
    section_doc = "Flavors Extension."

    def test_flavors_get(self):
        response = self._doc_do_get(
            'flavors/%s', 1, 'flavor_id',
            api_desc="Return data about the given flavor id.")
        subs = self._get_regexes()
        self._verify_response('flavor-get-resp', subs, response, 200)

    def test_flavors_list(self):
        response = self._doc_do_get(
            'flavors', (), (), api_desc="Return all flavors in brief.")
        subs = self._get_regexes()
        self._verify_response('flavors-list-resp', subs, response, 200)

    def test_flavors_detail(self):
        response = self._doc_do_get('flavors/detail', (), (),
                                    api_desc="Return all flavors in detail.")
        subs = self._get_regexes()
        self._verify_response('flavors-detail-resp', subs, response, 200)


class FlavorsSampleXmlTest(FlavorsSampleJsonTest):
    ctype = 'xml'
