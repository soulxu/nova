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


class AggregatesSampleJsonTest(api_sample_base.ApiSampleTestBaseV3):
    extension_name = "os-aggregates"
    section_name = 'Aggregates'
    section_doc = "Admin-only aggregate administration."

    def test_aggregate_create(self):
        subs = {
            "aggregate_id": '(?P<id>\d+)'
        }
        response = self._doc_do_post(
            'os-aggregates', (), (), 'aggregate-post-req', {},
            api_desc="Creates an aggregate, given its name and "
                     "availability_zone.")
        subs.update(self._get_regexes())
        return self._verify_response('aggregate-post-resp',
                                     subs, response, 201)

    def test_list_aggregates(self):
        self.test_aggregate_create()
        response = self._doc_do_get(
            'os-aggregates', (), (),
            api_desc="Returns a list a host aggregate's id, name, "
                     "availability_zone.")
        subs = self._get_regexes()
        self._verify_response('aggregates-list-get-resp', subs, response, 200)

    def test_aggregate_get(self):
        agg_id = self.test_aggregate_create()
        response = self._doc_do_get(
            'os-aggregates/%s', agg_id, 'aggregate_id',
            api_desc="Shows the details of an aggregate, hosts and metadata "
                     "included.")
        subs = self._get_regexes()
        self._verify_response('aggregates-get-resp', subs, response, 200)

    def test_add_metadata(self):
        agg_id = self.test_aggregate_create()
        response = self._doc_do_post(
            'os-aggregates/%s/action', agg_id, 'aggregate_id',
            'aggregate-metadata-post-req', {'action': 'set_metadata'},
            api_desc="Add new metadata and replaces the aggregate's existing "
                     "metadata with new metadata.")
        subs = self._get_regexes()
        self._verify_response('aggregates-metadata-post-resp', subs,
                              response, 200)

    def test_add_host(self):
        aggregate_id = self.test_aggregate_create()
        subs = {
            "host_name": self.compute.host,
        }
        response = self._doc_do_post(
            'os-aggregates/%s/action', aggregate_id, 'aggregate_id',
            'aggregate-add-host-post-req', subs,
            api_desc="Adds a host to the specified aggregate.")
        subs.update(self._get_regexes())
        self._verify_response('aggregates-add-host-post-resp', subs,
                              response, 202)

    def test_remove_host(self):
        self.test_add_host()
        subs = {
            "host_name": self.compute.host,
        }
        response = self._doc_do_post(
            'os-aggregates/%s/action', 1, 'aggregate_id',
            'aggregate-remove-host-post-req', subs,
            api_desc="Removes a host from the specified aggregate.")
        subs.update(self._get_regexes())
        self._verify_response('aggregates-remove-host-post-resp',
                              subs, response, 202)

    def test_update_aggregate(self):
        aggregate_id = self.test_aggregate_create()
        response = self._doc_do_put(
            'os-aggregates/%s', aggregate_id, 'aggregate_id',
            'aggregate-update-post-req', {},
            api_desc="Updates the name and/or availability_zone of "
                     "given aggregate.")
        subs = self._get_regexes()
        self._verify_response('aggregate-update-post-resp',
                              subs, response, 200)


class AggregatesSampleXmlTest(AggregatesSampleJsonTest):
    ctype = 'xml'
