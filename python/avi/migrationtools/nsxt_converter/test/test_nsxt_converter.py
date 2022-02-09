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
from avi.migrationtools.nsxt_converter.persistant_converter import PersistantProfileConfigConv
from avi.migrationtools.nsxt_converter.profile_converter import ProfileConfigConv
from avi.migrationtools.nsxt_converter.ssl_profile_converter import SslProfileConfigConv
from avi.migrationtools.nsxt_converter.vs_converter import VsConfigConv
from avi.migrationtools.avi_migration_utils import get_count, set_update_count

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
object_merge_check = False
avi_config = dict()
merge_object_mapping = {

    'ssl_profile': {'no': 0},
    'app_profile': {'no': 0},
    'network_profile': {'no': 0},
    'health_monitor': {'no': 0},
    'ssl_cert_key': {'no': 0}
}
sys_dict = {}
sys_dict = {}
merge_object_type = ['ApplicationProfile', 'NetworkProfile',
                     'SSLProfile', 'PKIProfile', 'SSLKeyAndCertificate',
                     'ApplicationPersistenceProfile', 'HealthMonitor',
                     'IpAddrGroup']
for key in merge_object_type:
    sys_dict[key] = []


def setUpModule():
    cfg_file = open(option.nsx_lb_config, 'r')
    cfg = cfg_file.read()
    global nsx_config
    nsx_config = json.loads(cfg)
    global nsxt_attributes
    nsxt_attributes = conv_const.init()


class Test(unittest.TestCase):

    def test_health_monitor_conversion(self):
        tenant="admin"
        monitor_converter = MonitorConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping, sys_dict)
        monitor_converter.convert(avi_config, nsx_config, '',tenant,False)
        avi_monitor_config = avi_config.get('HealthMonitor', None)
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

    def test_pool_conversion(self):

        pool_config = nsx_config['LbPools']
        pool_converter = PoolConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping, sys_dict)
        pool_converter.convert(avi_config, nsx_config, '', '', "admin")
        avi_pool_config = avi_config['Pool']
        print(avi_pool_config)
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
        profile_converter = ProfileConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping, sys_dict)
        profile_converter.convert(avi_config, nsx_config, '', 'admin')
        avi_app_profile_config = avi_config.get('ApplicationProfile', None)
        avi_network_profile_confg = avi_config.get('NetworkProfile', None)

        assert avi_app_profile_config
        assert avi_network_profile_confg
        assert len(profile_config) == len(avi_app_profile_config) + len(avi_network_profile_confg)

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
        lb_udp = []
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
            assert row['Status'] != "ERROR"

    def test_healthmonitor_prefix(self):
        """
        for testing prefix in HealthMonitors
        """

        prefix = "AVI"
        monitor_converter = MonitorConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping, sys_dict)
        monitor_converter.convert(avi_config, nsx_config, prefix,"admin",False)
        avi_monitor_config = avi_config.get('HealthMonitor', None)
        assert avi_monitor_config

        for hm in avi_monitor_config:
            assert hm['name'].startswith(prefix)

    def test_pool_prefix(self):
        """
        for testing prefix in Pool
        """

        prefix = "AVI"
        pool_converter = PoolConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping, sys_dict)
        pool_converter.convert(avi_config, nsx_config, '', prefix,"admin")
        avi_pool_config = avi_config['Pool']

        assert avi_pool_config
        for pools in avi_pool_config:
            assert pools['name'].startswith(prefix)
            if pools.get('health_monitor_refs'):
                for pool_hm in pools['health_monitor_refs']:
                    assert pool_hm.split('name=')[1].startswith(prefix)

    def test_profile_prefix(self):
        """
        for testing prefix in ApplicationProfiles
        """

        prefix = "AVI"
        profile_converter = ProfileConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping, sys_dict)
        profile_converter.convert(avi_config, nsx_config, prefix,"admin")
        avi_app_profile_config = avi_config.get('ApplicationProfile', None)
        avi_network_profile_confg = avi_config.get('NetworkProfile', None)

        assert avi_app_profile_config
        for app_pr in avi_app_profile_config:
            assert app_pr['name'].startswith(prefix)
        assert avi_network_profile_confg
        for np_pr in avi_network_profile_confg:
            assert np_pr['name'].startswith(prefix)

    def test_vs_prefix(self):
        """
        for testing prefix in virtual service
        """

        prefix = "AVI"
        vs_state = True
        vs_converter = VsConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping, sys_dict)
        vs_converter.convert(avi_config, nsx_config, '', prefix,"admin",vs_state, "", "",)
        avi_vs_config = avi_config.get('VirtualService', None)
        assert avi_vs_config

        for hm in avi_vs_config:
            assert hm['name'].startswith(prefix)

    def test_migrate_to(self):
        """
        added migrate_to
        """

        vs_state = False
        migrate_to = 'NSX'
        nsxt_config_converter.convert(nsx_config, input_path, output_path, "admin", 'cloud', '', migrate_to,
                                      object_merge_check,"", vs_state, vs_level_status=False, vrf=None,
                                      segroup=None, not_in_use=True,)

    def test_skipped_object(self):
        """
        test case for skipped objct
        """

        data_path = option.conv_excel
        data = pd.read_excel(data_path)
        for k, row in data.iterrows():
            if row['NsxT SubType'] in ['LBPassiveMonitorProfile', "LBGenericPersistenceProfile"]:
                assert row['Status'] == 'SKIPPED'

    def test_object_merge(self):
        """
        testing with object merge flag
        """
        vs_state = True
        vs_level_status = False
        migrate_to = 'NSX'
        object_merge_check = True
        nsxt_config_converter.convert(nsx_config, input_path, output_path, 'cloud', '', migrate_to,
                                      object_merge_check,
                                      "", vs_state, vs_level_status, vrf=None)

    def test_vs_state_level_true(self):
        """
        testing when vs level status is true
        """
        controller_version="20.1.7"
        vs_state = True
        vs_level_status = True
        migrate_to = 'NSX'
        nsxt_config_converter.convert(nsx_config, input_path, output_path, "admin", 'cloud', '', migrate_to, object_merge_check,
                                      controller_version, vs_state, vs_level_status, vrf=None, segroup=None,
                                      not_in_use=True, custom_mapping=None)
        excel_path = os.path.abspath(
            os.path.join(
                output_path, 'nsxt-report-ConversionStatus.xlsx'
            )
        )
        data = pd.read_excel(excel_path, engine='openpyxl', sheet_name='Status Sheet')
        if "Overall skipped settings" in data and "VS Reference" in data:
            output = True
        else:
            output = False
        assert output

    def test_vs_level_status_false(self):
        """
        testing when vs level status is false
        """

        vs_state = True
        vs_level_status = False
        migrate_to = 'NSX'
        nsxt_config_converter.convert(nsx_config, input_path, output_path, 'cloud', '', migrate_to,
                                      object_merge_check,
                                      "", vs_state, vs_level_status, vrf=None)

    def test_error_and_warning_count(self):

        set_update_count()
        vs_state = False
        vs_level_status = False
        migrate_to = 'NSX'
        nsxt_config_converter.convert(nsx_config, input_path, output_path, 'cloud', '', migrate_to,
                                      object_merge_check,
                                      "", vs_state, vs_level_status, vrf=None)

        assert get_count('error') == 0

    def test_ssl_prefix(self):
        """
        for testing prefix in ssl profile
        """

        prefix = "AVI"
        ssl_converter = SslProfileConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping, sys_dict)
        ssl_converter.convert(avi_config, nsx_config, prefix, "admin")
        avi_ssl_config = avi_config.get('SSLProfile', None)
        assert avi_ssl_config

        for hm in avi_ssl_config:
            assert hm['name'].startswith(prefix)

    def test_persistance_prefix(self):
        """
        for testing prefix in persistance profile
        """

        prefix = "AVI"
        persistance_converter = PersistantProfileConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping,
                                                            sys_dict)
        persistance_converter.convert(avi_config, nsx_config, prefix, "admin")
        avi_persis_config = avi_config.get('ApplicationPersistenceProfile', None)
        assert avi_persis_config

        for hm in avi_persis_config:
            assert hm['name'].startswith(prefix)

    def test_persistence_conversion(self):

        persistence_config = nsx_config['LbPersistenceProfiles']
        persistance_converter = PersistantProfileConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping,
                                                            sys_dict)
        persistance_converter.convert(avi_config, nsx_config, "","admin")

        avi_persis_config = avi_config.get('ApplicationPersistenceProfile', None)
        for alb_persis in avi_persis_config:
            for persis in persistence_config:
                if alb_persis['name'] == persis['display_name'] :
                    if persis['resource_type'] == "LBCookiePersistenceProfile":
                        if persis['cookie_name']:
                            assert alb_persis['http_cookie_persistence_profile']
                            assert persis['cookie_name'] == alb_persis['http_cookie_persistence_profile']['cookie_name']
                    elif persis['resource_type'] == "LBSourceIpPersistenceProfile":
                        if persis['timeout']:
                            assert alb_persis['ip_persistence_profile']
                            assert persis['timeout'] == alb_persis['ip_persistence_profile']['ip_persistent_timeout']

        assert avi_persis_config

    def test_ssl_profile_conversion(self):

        ssl_client_config = nsx_config['LbClientSslProfiles']
        ssl_server_config=nsx_config['LbServerSslProfiles']
        ssl_converter = SslProfileConfigConv(nsxt_attributes, object_merge_check, merge_object_mapping, sys_dict)
        ssl_converter.convert(avi_config, nsx_config, "", "admin")
        avi_ssl_config = avi_config.get('SSLProfile', None)
        assert avi_ssl_config
        assert len(avi_ssl_config) == len(ssl_client_config) + len(ssl_server_config)


