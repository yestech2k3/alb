import logging
import os
import unittest
import json
import copy

gSAMPLE_CONFIG = None
LOG = logging.getLogger(__name__)

from avi.f5_converter.pool_converter import PoolConfigConv
import avi.f5_converter.conversion_util as conv_util

def setUpModule():
    LOG.setLevel(logging.DEBUG)
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    dir_path = os.path.abspath(os.path.dirname(__file__))
    dir_path = dir_path.rsplit(os.path.sep, 1)[0]
    dir_path = dir_path + os.path.sep + "output"
    logging.basicConfig(filename=os.path.join(dir_path, 'converter.log'),
                        level=logging.DEBUG, format=formatter)
    cfg_file = open('test_pool_converter.conf', 'r')
    cfg = cfg_file.read()
    global gSAMPLE_CONFIG
    gSAMPLE_CONFIG = json.loads(cfg)
    dir_path = os.path.abspath(os.path.dirname(__file__))
    dir_path = dir_path.rsplit(os.path.sep, 1)[0]
    dir_path = dir_path + os.path.sep + "output"
    status_file = dir_path + os.path.sep + "ConversionStatus.csv"
    csv_file = open(status_file, 'w')
    conv_util.add_csv_headers(csv_file)


class Test(unittest.TestCase):

    def test_pool_group_conversion_v11(self):
        pool_converter = PoolConfigConv.get_instance('11')
        avi_config = gSAMPLE_CONFIG["avi_config"]
        f5_config_dict = gSAMPLE_CONFIG["pool_config_v11"]
        f5_config_dict_cp = copy.deepcopy(f5_config_dict)
        pool_converter.convert(f5_config_dict, avi_config, {})
        assert avi_config.get('PoolGroup', None)
        assert avi_config.get('PriorityLabels', None)

    def test_pool_group_conversion_v10(self):
        pool_converter = PoolConfigConv.get_instance('10')
        avi_config = gSAMPLE_CONFIG["avi_config"]
        f5_config_dict = gSAMPLE_CONFIG["pool_config_v10"]
        f5_config_dict_cp = copy.deepcopy(f5_config_dict)
        pool_converter.convert(f5_config_dict, avi_config, {})
        pool_groups = avi_config.get('PoolGroup', None)
        assert avi_config.get('PoolGroup', None)
        assert avi_config.get('PriorityLabels', None)



