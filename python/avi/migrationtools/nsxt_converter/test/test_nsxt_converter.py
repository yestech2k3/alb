import argparse
import logging
import os
import unittest
import json
import copy
import pytest
import sys
import pandas as pd

from avi.migrationtools.nsxt_converter import nsxt_config_converter
from avi.migrationtools.nsxt_converter.alb_converter import ALBConverter
from avi.migrationtools.nsxt_converter.nsxt_converter import NsxtConverter
from avi.migrationtools.nsxt_converter.monitor_converter import MonitorConfigConv
from avi.migrationtools.nsxt_converter.profile_converter import ProfileConfigConv

gSAMPLE_CONFIG = None
LOG = logging.getLogger(__name__)

from avi.migrationtools.nsxt_converter.pools_converter import PoolConfigConv
import avi.migrationtools.nsxt_converter.converter_constants as conv_const
import avi.migrationtools.nsxt_converter.conversion_util as conv_util

from conftest import option

avi_cfg_file = open(option.avi_config_file, 'r')
avi_cfg = avi_cfg_file.read()
avi_config_file = json.loads(avi_cfg)
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               'output'))
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
input_path = output_dir + os.path.sep + "input"
if not os.path.exists(input_path):
    os.makedirs(input_path)
output_path = output_dir + os.path.sep + "output"
if not os.path.exists(output_path):
    os.makedirs(output_path)

def setUpModule():
    cfg_file = open(option.nsx_lb_config, 'r')
    cfg = cfg_file.read()
    global nsx_config
    nsx_config = json.loads(cfg)
    global nsxt_attributes
    nsxt_attributes = conv_const.init()

class Test(unittest.TestCase):

    def test_pool_conversion(self):

        pool_config = nsx_config['LbPools']
        avi_pool_config = avi_config_file.get('Pool', None)

        assert avi_pool_config

        for index, pool in enumerate(avi_pool_config):
            assert pool.get('name')
            assert pool.get('lb_algorithm')
            if pool_config[index].get('member'):
                assert pool.get('servers')
            if pool_config[index].get('active_monitor_path'):
                assert len(pool['health_monitor_refs']) == len(pool_config[index]['active_monitor_path'])

        assert len(pool_config) == len(avi_pool_config)

    def test_profile_conversion(self):

        profile_config = nsx_config['LbAppProfiles']
        avi_app_profile_config = avi_config_file.get('ApplicationProfile', None)
        avi_network_profile_confg = avi_config_file.get('NetworkProfile', None)

        assert avi_app_profile_config
        assert avi_network_profile_confg
        assert len(profile_config) == len(avi_app_profile_config) + len(avi_network_profile_confg)

    def test_health_monitor_conversion(self):

        avi_monitor_config = avi_config_file.get('HealthMonitor', None)
        monitor_config = nsx_config['LbMonitorProfiles']
        assert avi_monitor_config
        non_passive_monitor_count = 0
        index = 0
        for monitor in monitor_config:
            if monitor.get('resource_type') not in ['LBPassiveMonitorProfile']:
                non_passive_monitor_count += 1
                if monitor.get('interval'):
                    assert monitor.get('interval') == avi_monitor_config[index]['send_interval']
                if monitor.get('fall_count'):
                    assert monitor.get('fall_count') == avi_monitor_config[index]['failed_checks']
                if monitor.get('rise_count'):
                    assert monitor.get('rise_count') == avi_monitor_config[index]['successful_checks']
                if monitor.get('timeout'):
                    assert monitor.get('timeout') == avi_monitor_config[index]['send_interval']
                if monitor.get('monitor_port'):
                    assert monitor.get('monitor_port') == avi_monitor_config[index]['monitor_port']
                index += 1

        assert non_passive_monitor_count == len(avi_monitor_config)

    def test_config_hm_http(self):
        avi_monitor_config = avi_config_file.get('HealthMonitor', None)
        monitor_config = nsx_config['LbMonitorProfiles']
        lb_http = []
        for lb_hm in monitor_config:
            if lb_hm.get('resource_type') in ['LBHttpMonitorProfile']:
                lb_http.append(lb_hm)

        for alb_hm in avi_monitor_config:
            for monitor in lb_http:
                if alb_hm['name'] == monitor['display_name']:
                    if monitor.get('request_url'):
                        assert monitor['request_url'] == alb_hm['http_monitor']['http_request']
                    if monitor.get('request_body'):
                        assert monitor['request_body'] == alb_hm['http_monitor']['http_request_body']
                    if monitor.get('response_body'):
                        assert monitor['response_body'] == alb_hm['http_monitor']['http_response']

    def test_config_hm_https(self):
        avi_monitor_config = avi_config_file.get('HealthMonitor', None)
        monitor_config = nsx_config['LbMonitorProfiles']
        lb_https = []
        for lb_hm in monitor_config:
            if lb_hm.get('resource_type') in ['LBHttpsMonitorProfile']:
                lb_https.append(lb_hm)

        for alb_hm in avi_monitor_config:
            for monitor in lb_https:
                if alb_hm['name'] == monitor['display_name']:
                    if monitor.get('request_url'):
                        assert monitor['request_url'] == alb_hm['https_monitor']['http_request']
                    if monitor.get('request_body'):
                        assert monitor['request_body'] == alb_hm['https_monitor']['http_request_body']
                    if monitor.get('response_body'):
                        assert monitor['response_body'] == alb_hm['https_monitor']['http_response']

    def test_config_hm_udp(self):
        avi_monitor_config = avi_config_file.get('HealthMonitor', None)
        monitor_config = nsx_config['LbMonitorProfiles']
        lb_udp=[]
        for lb_hm in monitor_config:
            if lb_hm.get('resource_type') in ['LBUdpMonitorProfile']:
                lb_udp.append(lb_hm)

        for alb_hm in avi_monitor_config:
            for monitor in lb_udp:
                if alb_hm['name'] == monitor['display_name']:
                    if monitor.get('send'):
                        assert monitor['send'] == alb_hm['udp_monitor']['udp_request']
                    if monitor.get('receive'):
                        assert monitor['receive'] == alb_hm['udp_monitor']['udp_response']

    def test_config_hm_tcp(self):
        avi_monitor_config = avi_config_file.get('HealthMonitor', None)
        monitor_config = nsx_config['LbMonitorProfiles']
        lb_tcp = []
        for lb_hm in monitor_config:
            if lb_hm.get('resource_type') in ['LBTcpMonitorProfile']:
                lb_tcp.append(lb_hm)

        for alb_hm in avi_monitor_config:
            for monitor in lb_tcp:
                if alb_hm['name'] == monitor['display_name']:
                    if monitor.get('send'):
                        assert monitor['send'] == alb_hm['tcp_monitor']['tcp_request']
                    if monitor.get('receive'):
                        assert monitor['receive'] == alb_hm['tcp_monitor']['tcp_response']

    def test_converted_status(self):

        assert nsx_config['LbPools'] and avi_config_file['Pool']
        assert nsx_config['LbMonitorProfiles'] and avi_config_file['HealthMonitor']
        data_path = option.conv_excel
        data = pd.read_excel(data_path)
        for k, row in data.iterrows():
            assert row['Status'] != "skipped"

    def test_healthmonitor_prefix(self):
        """
        for testing prefix in HealthMonitors
        """
        prefix = "AVI"

        avi_config = dict()
        monitor_converter = MonitorConfigConv(nsxt_attributes)
        monitor_converter.convert(avi_config, nsx_config, prefix)
        avi_monitor_config = avi_config.get('HealthMonitor', None)
        assert avi_monitor_config

        for hm in avi_monitor_config:
            assert hm['name'].startswith(prefix)

    def test_pool_prefix(self):
        """
        for testing prefix in Pool
        """
        prefix = "AVI"
        avi_config = dict()
        pool_converter = PoolConfigConv(nsxt_attributes)
        pool_converter.convert(avi_config, nsx_config, '', prefix)
        avi_pool_config = avi_config['Pool']

        assert avi_pool_config
        for pools in avi_pool_config:
            assert pools['name'].startswith(prefix)
            if pools['health_monitor_refs']:
                for pool_hm in pools['health_monitor_refs']:
                    assert pool_hm.split('name=')[1].startswith(prefix)

    def test_profile_prefix(self):
        """
        for testing prefix in ApplicationProfiles
        """
        prefix = "AVI"
        avi_config = dict()
        profile_converter = ProfileConfigConv(nsxt_attributes)
        profile_converter.convert(avi_config, nsx_config, prefix)
        avi_app_profile_config = avi_config.get('ApplicationProfile', None)
        avi_network_profile_confg = avi_config.get('NetworkProfile', None)

        assert avi_app_profile_config
        for app_pr in avi_app_profile_config:
            assert app_pr['name'].startswith(prefix)
        assert avi_network_profile_confg
        for np_pr in avi_network_profile_confg:
            assert np_pr['name'].startswith(prefix)

    def test_migrate_to(self):
        """
        added migrate_to
        """
        migrate_to='NSX'
        nsxt_config_converter.convert(nsx_config,input_path,output_path,'cloud','',migrate_to)

    def test_skipped_object(self):
        """
        test case for skipped objct
        """
        data_path = option.conv_excel
        data = pd.read_excel(data_path)
        for k, row in data.iterrows():
            if row['NsxT SubType'] in ['LBPassiveMonitorProfile']:
                assert row['Status'] == 'SKIPPED'



