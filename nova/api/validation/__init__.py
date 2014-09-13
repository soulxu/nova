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


def _fetch_param(body, mapping, params):
    for key in body.keys():
        if key in mapping:
            params[mapping[key]] = body[key]
        elif isinstance(body[key], dict):
            _fetch_param(body[key], mapping, params)


def _build_body(schema, mapping, params, body):
    for prop in schema['properties'].keys():
        if schema['properties'][prop]['type'] == 'object':
            body[prop] = {}
            _build_body(schema['properties'][prop], mapping, params,
                        body[prop])
        else:
            body[prop] = params[mapping[prop]]


def _mapping_resquest(request_body_schema, body):
    mapping = request_body_schema['ext:mapping']
    params = {}
    _fetch_param(body, mapping, params)
    return params


def _mapping_response(response_body_schema, params):
    mapping = response_body_schema['ext:mapping']
    body = {}
    _build_body(response_body_schema, mapping, params, body)
    return body


def schema(request_body_schema=None, schema=None):
    """Register a schema to validate request body.

    Registered schema will be used for validating request body just before
    API method executing.

    :argument dict request_body_schema: a schema to validate request body

    """

    def add_validator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) == 1:
                req = kwargs['req']
            else:
                req = args[1]
            if schema:
                request_body_schema = getattr(
                    schema, "request_%s" % req.version.replace('.', '_'))
                body = kwargs.pop('body')
            else:
                body = kwargs['body']
            schema_validator = _SchemaValidator(request_body_schema)
            schema_validator.validate(body)
            if schema:
                params = _mapping_resquest(request_body_schema, body)
                kwargs['params'] = params

            ret =  func(*args, **kwargs)

            if schema:
                response_body_schema = getattr(
                        schema, "response_%s" % req.version.replace('.', '_'))
                return _mapping_response(response_body_schema, ret)
            return ret
        return wrapper
    return add_validator
