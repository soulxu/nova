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

import coverage

from nova.api.openstack.compute.plugins.v3 import coverage as coverage_ext
from nova.tests.api.openstack.compute.plugins.v3 import test_coverage
from nova.tests.integrated.v3 import api_sample_base


class CoverageJsonTests(api_sample_base.ApiSampleTestBaseV3):
    extension_name = "os-coverage"
    section_name = 'Coverage'
    section_doc = ("This adds support for enabling Ned Batchelder's coverage "
                   "module for nova from an external api call.")

    def setUp(self):
        super(CoverageJsonTests, self).setUp()

        def _fake_check_coverage(self):
            return False

        def _fake_xml_report(self, outfile=None):
            return

        self.stubs.Set(coverage_ext.CoverageController, '_check_coverage',
                       _fake_check_coverage)
        self.stubs.Set(coverage, 'coverage', test_coverage.FakeCoverage)

    def _test_start_coverage(self):
        # Start coverage data collection.
        subs = {}
        response = self._doc_do_post(
            'os-coverage/action', (), (),
            'coverage-start-post-req', subs,
            api_desc='Begin recording coverage information.')
        self._verify_no_response('coverage-start', response, 204)

    def test_start_coverage(self):
        self._test_start_coverage()

    def test_start_coverage_combine(self):
        # Start coverage data collection.
        subs = {}
        response = self._doc_do_post(
            'os-coverage/action', (), (),
            'coverage-start-combine-post-req', subs,
            api_desc=('Begin recording coverage information,'
                      'and combine the report'))
        self._verify_no_response('coverage-start-combine', response, 204)

    def test_stop_coverage(self):
        # Stop coverage data collection.
        subs = {
            'path': '/.*',
        }
        response = self._doc_do_post(
            'os-coverage/action', (), (),
            'coverage-stop-post-req', subs,
            api_desc='Stop recording coverage information')
        subs.update(self._get_regexes())
        self._verify_response('coverage-stop-post-resp', subs, response, 200)

    def test_report_coverage(self):
        # Generate a coverage report.
        subs = {
            'filename': 'report',
            'path': '/.*/report',
        }
        response = self._doc_do_post(
            'os-coverage/action', (), (),
            'coverage-report-post-req', subs,
            api_desc='Generate a coverage report.')
        subs.update(self._get_regexes())
        self._verify_response('coverage-report-post-resp', subs, response, 200)

    def test_report_coverage_xml(self):
        subs = {
            'filename': 'report',
            'path': '/.*/report',
        }
        response = self._doc_do_post(
            'os-coverage/action', (), (),
            'coverage-report-xml-post-req', subs,
            api_desc='Generate a coverage report with xml format.')
        subs.update(self._get_regexes())
        self._verify_response('coverage-report-xml-post-resp',
                              subs, response, 200)

    def test_reset_coverage(self):
        self._test_start_coverage()
        response = self._doc_do_post(
            'os-coverage/action', (), (),
            'coverage-reset-post-req', {},
            api_desc='Reset recording coverage information')
        self.assertEqual(response.status, 204)


class CoverageXmlTests(CoverageJsonTests):
    ctype = "xml"
