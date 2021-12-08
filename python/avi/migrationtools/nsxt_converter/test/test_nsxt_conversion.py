# Copyright 2021 VMware, Inc.
# SPDX-License-Identifier: Apache License 2.0

import copy
import logging
import os
import unittest
import csv

import avi.migrationtools.nsxt_converter.nsxt_config_converter as nsxt_config_converter

import avi.migrationtools.nsxt_converter.nsxt_converter as nsxt_converter

gSAMPLE_CONFIG = None
LOG = logging.getLogger(__name__)


def setUpModule():
    LOG.setLevel(logging.DEBUG)
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    dir_path = os.path.abspath(os.path.dirname(__file__))
    dir_path = dir_path.rsplit(os.path.sep, 1)[0]
    dir_path = dir_path + os.path.sep + "output"
    logging.basicConfig(filename=os.path.join(dir_path, 'converter.log'),
                        level=logging.DEBUG, format=formatter)
    dir_path = os.path.abspath(os.path.dirname(__file__))
    cfg_file = open(dir_path+os.path.sep+'nsxt.conf', 'r')
    cfg = cfg_file.read()
    global gSAMPLE_CONFIG
    gSAMPLE_CONFIG = cfg


class Test(unittest.TestCase):

    def test_config_conversion(self):
        dir_path = os.path.abspath(os.path.dirname(__file__))
        dir_path = dir_path.rsplit(os.path.sep, 1)[0]
        nsxt_config_dict = gSAMPLE_CONFIG

        assert nsxt_config_dict.get("LBServices", None)
        assert nsxt_config_dict.get("LbMonitorProfiles", None)
        assert nsxt_config_dict.get("LbPools", None)
        assert nsxt_config_dict.get("LbAppProfiles", None)

        avi_config_dict = nsxt_config_converter.convert(
            nsxt_config_dict, dir_path+os.path.sep+"output", "disable",
            "certs", '11')
        assert avi_config_dict
        with open('%s%soutput%sConversionStatus.csv' %
                          (dir_path, os.path.sep, os.path.sep)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                assert row['Status'] != 'error'


if __name__ == "__main__":
    unittest.main()
