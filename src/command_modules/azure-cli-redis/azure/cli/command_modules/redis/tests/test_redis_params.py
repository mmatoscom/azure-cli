#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

import unittest

from azure.cli.core.application import APPLICATION, Configuration

def mock_echo_args(command_name, parameters):
    try:
        argv = ' '.join((command_name, parameters)).split()
        APPLICATION.initialize(Configuration(argv))
        command_table = APPLICATION.configuration.get_command_table()
        prefunc = command_table[command_name].handler
        command_table[command_name].handler = lambda args: args
        parsed_namespace = APPLICATION.execute(argv)
        return parsed_namespace
    finally:
        command_table[command_name].handler = prefunc

class Test_RedisCache(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_parse_redis_create(self):

        args = mock_echo_args('redis create',
                              '--tenant-settings {\"hello\":1} -g wombat -n asldkj --sku-family c -l westus  --sku-capacity 1  --sku-name basic') # pylint: disable=line-too-long
        subset = set(dict(
            sku_family='c',
            sku_capacity='1',
            sku_name='basic',
            name='asldkj'
            ).items())

        superset = set([(k, v) for k, v in args.result.items() if not isinstance(v, dict)])

        self.assertTrue(
            subset.issubset(superset)
            )

        tenant_settings = dict(hello=1)
        self.assertDictEqual(tenant_settings, args.result['tenant_settings'])
