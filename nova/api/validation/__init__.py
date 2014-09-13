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

from validators import _SchemaValidator


def _get_specified_version_schema(prefix, req, schema):
    return getattr(schema, "%s_%s" % (prefix, req.version.replace('.', '_')))


def schema(request_body_schema=None, schema=None, request_obj_cls=None):
    """Register a schema to validate request body.

    Registered schema will be used for validating request body just before
    API method executing.

    :argument dict request_body_schema: a schema to validate request body

    """

    def add_validator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if 'req' in kwargs:
                req = kwargs['req']
            else:
                req = args[1]
            if schema:
                request_body_schema = _get_specified_version_schema('request',
                                                                    req,
                                                                    schema)
                body = kwargs.pop('body')
            else:
                body = kwargs['body']

            schema_validator = _SchemaValidator(request_body_schema)
            schema_validator.validate(body)

            if schema:
                request_obj = request_obj_cls.obj_from_primitive_by_schema(
                    body, request_body_schema)
                kwargs['param_obj'] = request_obj

            ret =  func(*args, **kwargs)

            if schema:
                response_body_schema = _get_specified_version_schema(
                    'response', req, schema)
                return ret.obj_to_primitive_by_schema(response_body_schema)
            return ret
        return wrapper
    return add_validator
