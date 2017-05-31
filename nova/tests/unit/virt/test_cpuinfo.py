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

import mock

from nova import test
from nova.virt.libvirt import cpuinfo


class CPUInfoTestCase(test.NoDBTestCase):

    @mock.patch.object(cpuinfo, '_read_cpu_info')
    def test_cpu_info(self, mock_read_cpu_info):
        mock_read_cpu_info.return_value = [
            'processor\t: 0\n',
            'vendor_id\t: GenuineIntel\n',
            'cpu family\t: 6\n',
            'cpu MHz\t\t: 1199.000\n',
            '\n',
            'processor\t: 1\n',
            'vendor_id\t: GenuineIntel\n',
            'cpu family\t: 6\n',
            'cpu MHz\t\t: 2299.000\n',
            '\n']

        ret = cpuinfo.get_cpus_detail()
        self.assertEqual(
            [{'id': 0, 'frequency': 1199.000},
             {'id': 1, 'frequency': 2299.000}],
            ret)
