# Copyright 2013 NEC Corporation.  All rights reserved.
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
"""
Request Body validating middleware.

"""

import functools

from nova.openstack.common import importutils
from validators import _SchemaValidator


def _get_parameters_helper(body, schema, mapping, params):
    if 'properties' in schema:
        for key in schema['properties'].keys():
            params[mapping.get(key, key)] = body.get(key)


def _get_parameters(body, schema, params):
    mapping = {}
    if 'ext:mapping' in schema:
        mapping = dict(schema['ext:mapping'])
    root_key, root_schema = schema['properties'].items()[0]
    _get_parameters_helper(body[root_key], root_schema, mapping, params)


def schema(request_body_schema):
    """Register a schema to validate request body.

    Registered schema will be used for validating request body just before
    API method executing.

    :argument dict request_body_schema: a schema to validate request body

    """

    def add_validator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            req = kwargs['req']
            if isinstance(request_body_schema, str):
                # There isn't only support v2.1 and v3. There will support
                # any version for micro_version.
                version = '2_1' if req.api_version == '2' else '3_0'
                schema_path = ('nova.api.openstack.compute.schemas.v3.'
                               '%(extension)s_%(version)s.%(extension)s') % {
                                    'extension': request_body_schema,
                                    'version': version}
                schema = importutils.import_class(schema_path)
            schema_validator = _SchemaValidator(schema)
            schema_validator.validate(kwargs['body'])
            _get_parameters(kwargs['body'], schema, kwargs)
            return func(*args, **kwargs)
        return wrapper
    return add_validator
