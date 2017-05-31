#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.


def _read_cpu_info():
    f = open('/proc/cpuinfo', 'r')
    ret = f.readlines()
    f.close()
    return ret


def _get_cpu_detail(cpu_info):
    ret = {}

    for info in cpu_info:
        key, value = info.split(':')
        key = key.strip()
        value = value.strip()
        if key == 'processor':
            ret['id'] = int(value)
        elif key == 'cpu MHz':
            ret['frequency'] = float(value)

    return ret


def get_cpus_detail():
    ret = []
    single_cpu_info = []

    for line in _read_cpu_info():
        if line == '\n':
            ret.append(_get_cpu_detail(single_cpu_info))
            single_cpu_info = []
        else:
            single_cpu_info.append(line)

    return ret
