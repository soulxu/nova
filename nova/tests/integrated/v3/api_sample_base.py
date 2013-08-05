# vim: tabstop=4 shiftwidth=4 softtabstop=4
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

import os

from oslo.config import cfg

from nova.api.openstack import API_V3_CORE_EXTENSIONS  # noqa
from nova.openstack.common import jsonutils
from nova import test
from nova.tests import fake_network
from nova.tests import fake_utils
from nova.tests.integrated import api_samples_test_base

CONF = cfg.CONF


class ApiSampleTestBaseV3(api_samples_test_base.ApiSampleTestBase):
    _api_version = 'v3'
    sample_dir = None
    extra_extensions_to_load = None
    section_name = None
    section_doc = None

    def setUp(self):
        extends = []
        self.flags(use_ipv6=False,
                   osapi_compute_link_prefix=self._get_host(),
                   osapi_glance_link_prefix=self._get_glance_host())
        if not self.all_extensions:
            # Set the whitelist to ensure only the extensions we are
            # interested in are loaded so the api samples don't include
            # data from extensions we are not interested in
            whitelist = API_V3_CORE_EXTENSIONS.copy()
            if self.extension_name:
                whitelist.add(self.extension_name)
            if self.extra_extensions_to_load:
                whitelist.update(set(self.extra_extensions_to_load))

            CONF.set_override('extensions_whitelist', whitelist,
                              'osapi_v3')

        super(ApiSampleTestBaseV3, self).setUp()
        self.useFixture(test.SampleNetworks(host=self.network.host))
        fake_network.stub_compute_with_ips(self.stubs)
        fake_utils.stub_out_utils_spawn_n(self.stubs)
        self.generate_samples = os.getenv('GENERATE_SAMPLES') is not None
        self.metainfo = {}

    @classmethod
    def _get_sample_path(cls, name, dirname, suffix=''):
        parts = [dirname]
        parts.append('api_samples')
        if cls.all_extensions:
            parts.append('all_extensions')
        elif cls.sample_dir:
            parts.append(cls.sample_dir)
        elif cls.extension_name:
            parts.append(cls.extension_name)
        parts.append(name + "." + cls.ctype + suffix)
        return os.path.join(*parts)

    @classmethod
    def _get_sample(cls, name):
        dirname = os.path.dirname(os.path.abspath(__file__))
        dirname = os.path.normpath(os.path.join(dirname, "../../../../doc/v3"))
        return cls._get_sample_path(name, dirname)

    @classmethod
    def _get_template(cls, name):
        dirname = os.path.dirname(os.path.abspath(__file__))
        return cls._get_sample_path(name, dirname, suffix='.tpl')

    def _doc_get_response(self, url, method, body=None, strip_version=False,
                           **kwargs):
        response = self._get_response(url, method, body, strip_version)
        if 'api_desc' in kwargs:
            self.metainfo['section_name'] = self.section_name
            self.metainfo['extension'] = self.extension_name
            self.metainfo['extension_description'] = self.section_doc
            self.metainfo['method'] = method
            self.metainfo['description'] = kwargs['api_desc']
            self.metainfo['status'] = response.status
            self.metainfo['url'] = kwargs['url_doc']
        return response

    def _convert_url_params(self, params, is_doc=False):

        if not isinstance(params, tuple):
            params = (params,)
        if is_doc:
            return tuple("{" + param + "}" for param in params)
        else:
            return params

    def _doc_do_get(self, url, url_api_params, url_doc_params,
                    strip_version=False, **kwargs):
        url_api = url % self._convert_url_params(url_api_params)
        url_doc = url % self._convert_url_params(url_doc_params, is_doc=True)
        kwargs['url_doc'] = url_doc
        return self._doc_get_response(url_api, 'GET', None, strip_version,
                                      **kwargs)

    def _doc_do_post(self, url, url_api_params, url_doc_params, name, subs,
                     method='POST', **kwargs):
        url_api = url % self._convert_url_params(url_api_params)
        url_doc = url % self._convert_url_params(url_doc_params, is_doc=True)
        kwargs['url_doc'] = url_doc
        if method in ['POST', 'PUT'] and 'api_desc' in kwargs:
            self.metainfo['request'] = name + "." + self.ctype
        body = self._read_template(name) % subs
        sample = self._get_sample(name)
        if self.generate_samples and not os.path.exists(sample):
                self._write_sample(name, body)
        return self._doc_get_response(url_api, method, body, False, **kwargs)

    def _doc_do_put(self, url, url_api_params, url_doc_params, name, subs,
                    **kwargs):
        return self._doc_do_post(url, url_api_params, url_doc_params, name,
                                 subs, method='PUT', **kwargs)

    def _doc_do_delete(self, url, url_api_params, url_doc_params, **kwargs):
        url_api = url % self._convert_url_params(url_api_params)
        url_doc = url % self._convert_url_params(url_doc_params, is_doc=True)
        kwargs['url_doc'] = url_doc
        return self._doc_get_response(url_api, 'DELETE', None, False, **kwargs)

    def _write_metafile(self, name, has_response):
        if self.generate_samples and 'section_name' in self.metainfo:
            metafile_name = self._get_sample(name) + ".meta"
            if not os.path.exists(metafile_name):
                if has_response:
                    self.metainfo['response'] = name + '.' + self.ctype
                with open(metafile_name, 'w') as outf:
                    outf.write(jsonutils.dumps(self.metainfo, sort_keys=True,
                                               indent=4))

    def _verify_response(self, name, subs, response, exp_code):
        response = super(ApiSampleTestBaseV3, self)._verify_response(
            name, subs, response, exp_code)
        self._write_metafile(name, has_response=True)
        return response

    def _verify_delete_response(self, name, response, exp_code):
        self.assertEqual(response.status, exp_code)
        self._write_metafile(name, has_response=False)
