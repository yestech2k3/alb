# Copyright 2021 VMware, Inc.
# SPDX-License-Identifier: Apache License 2.0

"""
This testsuite contains the initial test cases for testing the
f5 converter tool along with its options / parameters
"""
import unittest
import json
import logging
import os
import subprocess
import sys

import pandas as pd
import pytest
import yaml
from avi.migrationtools.f5_converter.test.conftest import option
from avi.migrationtools.avi_migration_utils import MigrationUtil
from avi.migrationtools.avi_migration_utils import get_count, set_update_count
from avi.migrationtools.f5_converter.f5_converter import F5Converter, get_terminal_args, \
    ARG_DEFAULT_VALUE
from avi.migrationtools.test.common.excel_reader \
    import percentage_success, output_sanitization, output_vs_level_status
from avi.migrationtools.test.common.test_clean_reboot \
    import verify_controller_is_up, clean_reboot
from avi.migrationtools.test.common.test_tenant_cloud \
    import create_segroup, create_vrf_context
import ansible_runner
from avi.migrationtools.avi_migration_utils import MigrationUtil
common_avi_util = MigrationUtil()

config_file = option.config
input_file = option.file
input_file_version = option.fileVersion
output_file = option.out
# config_file = pytest.config.getoption("--config")
# input_file = pytest.config.getoption("--file")
# input_file_version = pytest.config.getoption("--fileVersion")
# output_file = pytest.config.getoption("--out")
if not output_file:
    output_file = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'output'))
input_file_v10 = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'bigip_v10.conf'))
input_file_v11 = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'hol_advanced_bigip.conf'))
input_role_config_file = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'custom_config.yaml'))
input_config_yaml = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'config.yaml'))

v10 = '10'
v11 = '11'

if input_file_version == '10' and input_file:
    v10 = '10'
    input_file_v10 = input_file
elif input_file_version == '11' and input_file:
    v11 = '11'
    input_file_v11 = input_file
# elif any([input_file_version, input_file]):
# print("Both arguments 'input_file_version' and 'input_file' are mandatory")
# sys.exit(0)


with open(config_file) as f:
    file_attribute = yaml.load(f, Loader=yaml.Loader)

setup = dict(
    controller_version_v17=file_attribute['controller_version_v17'],
    file_version_v10=v10,
    file_version_v11=v11,
    version=True,
    option=file_attribute['option'],
    controller_ip_17_1_1=file_attribute['controller_ip_17_1_1'],
    controller_user_17_1_1=file_attribute['controller_user_17_1_1'],
    controller_password_17_1_1=file_attribute['controller_password_17_1_1'],
    f5_host_ip_v10=file_attribute['f5_host_ip_v10'],
    f5_host_ip_v11=file_attribute['f5_host_ip_v11'],
    f5_ssh_user=file_attribute['f5_ssh_user'],
    f5_ssh_user_10=file_attribute['f5_ssh_user_10'],
    f5_ssh_password=file_attribute['f5_ssh_password'],
    f5_ssh_port=file_attribute['f5_ssh_port'],
    no_profile_merge=file_attribute['no_profile_merge'],
    prefix=file_attribute['prefix'],
    cloud_name=file_attribute['cloud_name'],
    tenant=file_attribute['tenant'],
    input_folder_location=os.path.abspath(os.path.join(os.path.dirname(__file__), 'certs')),
    config_file_name_v10=input_file_v10,
    config_file_name_v11=input_file_v11,
    partition_config='new',  # this is new
    f5_key_file='cd_rt_key.pem',
    ignore_config=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               'ignore-config.yaml')),
    patch=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       'patch.yaml')),
    vs_filter='EngVIP,F5-VIP-80-001,F5-VIP-443-002',
    not_in_use=True,
    skip_file=False,
    ansible=True,
    baseline_profile=None,
    f5_passphrase_file=os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'passphrase.yaml')),
    f5_ansible_object=os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'output',
        'avi_config_create_object.yml')),
    vs_level_status=True,
    test_vip=None,
    output_file_path=output_file,
    vrf='test_vrf',
    segroup='test_se',
    custom_config_file=input_role_config_file,
    distinct_app_profile=True,
    args_config_file=input_config_yaml
)

if not os.path.exists(setup.get("output_file_path")):
    os.mkdir(setup.get("output_file_path"))

formatter = '[%(asctime)s] %(levelname)s [%(funcName)s:%(lineno)d] %(message)s'
logging.basicConfig(filename=os.path.join(
    setup.get('output_file_path'), 'converter.log'),
    level=logging.DEBUG, format=formatter)

mylogger = logging.getLogger(__name__)


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def f5_conv(
        bigip_config_file=None, skip_default_file=False, f5_config_version=None,
        input_folder_location=os.path.abspath(os.path.join(os.path.dirname(__file__), 'certs')),
        output_file_path=output_file, option=ARG_DEFAULT_VALUE['option'],
        user=ARG_DEFAULT_VALUE['user'],
        password=None, controller_ip=None,
        tenant='admin', cloud_name=ARG_DEFAULT_VALUE['cloud_name'],
        vs_state=ARG_DEFAULT_VALUE['vs_state'],
        controller_version=None, f5_host_ip=None, f5_ssh_user=None,
        f5_ssh_password=None, f5_ssh_port=None, f5_key_file=None,
        ignore_config=None, partition_config=None, version=False,
        no_profile_merge=False, patch=None, vs_filter=None,
        ansible_skip_types=[], ansible_filter_types=[], ansible=False,
        prefix=None, convertsnat=False, not_in_use=False, baseline_profile=None,
        f5_passphrase_file=None, vs_level_status=False, test_vip=None,
        vrf=None, segroup=None, custom_config=None, skip_pki=False,
        distinct_app_profile=False, reuse_http_policy=False, args_config_file=None):
    args = Namespace(bigip_config_file=bigip_config_file,
                     skip_default_file=skip_default_file,
                     f5_config_version=f5_config_version,
                     input_folder_location=input_folder_location,
                     output_file_path=output_file_path, option=option,
                     user=user, password=password, controller_ip=controller_ip,
                     tenant=tenant, cloud_name=cloud_name, vs_state=vs_state,
                     controller_version=controller_version,
                     f5_host_ip=f5_host_ip, f5_ssh_user=f5_ssh_user,
                     f5_ssh_password=f5_ssh_password,
                     f5_ssh_port=f5_ssh_port, f5_key_file=f5_key_file,
                     ignore_config=ignore_config,
                     partition_config=partition_config, version=version,
                     no_object_merge=no_profile_merge, patch=patch,
                     vs_filter=vs_filter, ansible_skip_types=ansible_skip_types,
                     ansible_filter_types=ansible_filter_types, ansible=ansible,
                     prefix=prefix, convertsnat=convertsnat,
                     not_in_use=not_in_use, baseline_profile=baseline_profile,
                     f5_passphrase_file=f5_passphrase_file,
                     vs_level_status=vs_level_status, test_vip=test_vip,
                     vrf=vrf, segroup=segroup,
                     custom_config=custom_config,
                     skip_pki=skip_pki,
                     distinct_app_profile=distinct_app_profile,
                     reuse_http_policy=reuse_http_policy,
                     args_config_file=args_config_file)

    args = get_terminal_args(terminal_args=args)
    f5_converter = F5Converter(args)
    avi_config = f5_converter.convert()
    return avi_config


class TestF5Converter:

    @pytest.fixture
    def cleanup(self):
        import avi.migrationtools.f5_converter.conversion_util as conv
        import shutil
        conv.csv_writer_dict_list = list()
        if os.path.exists(output_file):
            for each_file in os.listdir(output_file):
                file_path = os.path.join(output_file, each_file)
                try:
                    if os.path.isfile(file_path):
                        if file_path.endswith('.log'):
                            open('converter.log', 'w').close()
                        else:
                            os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(e)

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_1_0
    def test_download_v11(self, cleanup):
        """
        Download Input File Flow, Test for Controller v17.1.1
        """
        f5_conv(f5_host_ip=setup.get('f5_host_ip_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_ssh_user=setup.get('f5_ssh_user'),
                f5_ssh_password=setup.get('f5_ssh_password'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                f5_config_version=setup.get('file_version_v11'),
                option=setup.get('option'),
                controller_ip=setup.get('controller_ip_17_1_1'),
                user=setup.get('controller_user_17_1_1'),
                password=setup.get('controller_password_17_1_1'),
                skip_pki=True)

    # Dont have version 10 F5 instance so commenting the tests
    # @pytest.mark.skip_travis
    # @pytest.mark.TCID1_48_1497_2_0
    # def test_download_v10(self, cleanup):
    #     """
    #     Download Input File Flow, Test for Controller v17.1.1
    #     """
    #     f5_conv(f5_host_ip=setup.get('f5_host_ip_v10'),
    #             controller_version=setup.get('controller_version_v17'),
    #             f5_ssh_user=setup.get('f5_ssh_user_10'),
    #             f5_ssh_password=setup.get('f5_ssh_password'),
    #             f5_ssh_port=setup.get('f5_ssh_port'),
    #             # Dont have version 10 F5 instance
    #             # f5_config_version=setup.get('file_version_v10'),
    #             skip_pki=True)
    #
    # @pytest.mark.skip_travis
    # @pytest.mark.TCID1_48_1497_3_0
    # def test_output_sanitization_v10(self, cleanup):
    #     f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
    #             # Dont have version 10 F5 instance
    #             # f5_config_version=setup.get('file_version_v10'),
    #             controller_version=setup.get('controller_version_v17'),
    #             f5_ssh_port=setup.get('f5_ssh_port'),
    #             output_file_path=output_file,
    #             skip_pki=True)
    #     self.excel_path = os.path.abspath(os.path.join(
    #         output_file, 'bigip_v10-ConversionStatus.xlsx'))
    #     self.json_path = os.path.abspath(os.path.join(
    #         output_file, 'bigip_v10-Output.json'))
    #     self.log_path = os.path.abspath(os.path.join(
    #         output_file, 'converter.log'))
    #     assert output_sanitization(self.excel_path, self.json_path,
    #                                self.log_path)

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_4_0
    def test_output_sanitization_v11(self, cleanup):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                output_file_path=output_file,
                skip_pki=True)
        self.excel_path = os.path.abspath(os.path.join(
            output_file, 'hol_advanced_bigip-ConversionStatus.xlsx'))
        self.json_path = os.path.abspath(os.path.join(
            output_file, 'hol_advanced_bigip-Output.json'))
        self.log_path = os.path.abspath(os.path.join(
            output_file, 'converter.log'))
        assert output_sanitization(self.excel_path,
                                   self.json_path,
                                   self.log_path)

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_5_0
    def test_excel_report_v11(self, cleanup):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                output_file_path=output_file)
        percentage_success(os.path.join(output_file,
                                        'hol_advanced_bigip-ConversionStatus.xlsx'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_6_0
    def test_without_options_v10(self, cleanup):
        """
        Check the Configuration file for V10
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                f5_config_version=setup.get('file_version_v10'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_7_0
    def test_without_options_v11(self, cleanup):
        """
        Check the configuration file for v11
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_8_0
    def test_no_profile_merge_v10(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        No_profile_merge Flag Reset
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                no_profile_merge=setup.get('no_profile_merge'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_9_0
    def test_no_profile_merge_v11(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        No_profile_merge Flag Reset
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                no_profile_merge=setup.get('no_profile_merge'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_10_0
    def test_prefix_v10(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        Prefix Added
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                prefix=setup.get('prefix'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_11_0
    def test_prefix_v11(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        Prefix Added
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                prefix=setup.get('prefix'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_12_0
    def test_cloud_name_v10(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        Prefix Added
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                cloud_name=setup.get('cloud_name'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_13_0
    def test_cloud_name_v11(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        Prefix Added
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                cloud_name=setup.get('cloud_name'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_14_0
    def test_tenant_v10(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        Tenant Added
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                tenant=setup.get('tenant'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_15_0
    def test_tenant_v11(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        Tenant Added
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                tenant=setup.get('tenant'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_16_0
    def test_input_folder_path_not_provided_v10(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        Input Folder path not provided
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                input_folder_location=setup.get('input_folder_location'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_17_0
    def test_input_folder_path_not_provided_v11(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        Input Folder path not provided
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                input_folder_location=setup.get('input_folder_location'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_18_0
    def test_ignore_config_v10(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        ignore_config option usage
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                ignore_config=setup.get('ignore_config'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_19_0
    def test_ignore_config_v11(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        ignore_config option usage
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                ignore_config=setup.get('ignore_config'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_20_0
    def test_patch_v10(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        Patch option usage
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                patch=setup.get('patch'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_21_0
    def test_patch_v11(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        Patch option usage
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                patch=setup.get('patch'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_22_0
    def test_not_in_use_v10(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        No_profile_merge Flag Reset
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                not_in_use=setup.get('not_in_use'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_23_0
    def test_not_in_use_v11(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        No_profile_merge Flag Reset
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                not_in_use=setup.get('not_in_use'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_24_0
    def test_passphrase_v10(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        No_profile_merge Flag Reset
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                f5_passphrase_file=setup.get('f5_passphrase_file'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_25_0
    def test_passphrase_v11(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        No_profile_merge Flag Reset
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                f5_passphrase_file=setup.get('f5_passphrase_file'),
                skip_pki=True)

    @pytest.mark.skip_travis
    def test_reboot_clean_v10_17_1_1_before_upload_config(self, cleanup):
        """""
        Verify Controller v17.1.1 is running and clean reboot avi api.
        After controller setup completed, upload the AviInternal
        certificate file.
        """
        is_up = verify_controller_is_up(file_attribute['controller_ip_17_1_1'],
                                        file_attribute[
                                            'controller_user_17_1_1'],
                                        file_attribute[
                                            'controller_password_17_1_1'])
        if is_up:
            clean_reboot(file_attribute['controller_ip_17_1_1'],
                         file_attribute['controller_user_17_1_1'],
                         file_attribute['controller_password_17_1_1'],
                         file_attribute['controller_version_v17'],
                         file_attribute['license_file_path'])
            print("Controller is running properly.")
        else:
            print("Controller is not running properly.")

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_26_0
    def test_auto_upload_v10_17_1_1(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        AutoUpload Flow
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                f5_config_version=setup.get('file_version_v10'),
                controller_version=setup.get('controller_version_v17'),
                option=setup.get('option'),
                controller_ip=setup.get('controller_ip_17_1_1'),
                user=setup.get('controller_user_17_1_1'),
                password=setup.get('controller_password_17_1_1'),
                skip_pki=True)

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_27_0
    def test_reboot_clean_v10_17_1_1(self, cleanup):
        """""
        Verify Controller v17.1.1 is running and clean reboot avi api.
        After controller setup completed, upload the AviInternal
        certificate file.
        """
        is_up = verify_controller_is_up(file_attribute['controller_ip_17_1_1'],
                                        file_attribute[
                                            'controller_user_17_1_1'],
                                        file_attribute[
                                            'controller_password_17_1_1'])
        if is_up:
            clean_reboot(file_attribute['controller_ip_17_1_1'],
                         file_attribute['controller_user_17_1_1'],
                         file_attribute['controller_password_17_1_1'],
                         file_attribute['controller_version_v17'],
                         file_attribute['license_file_path'])
            print("Controller is running properly.")
        else:
            print("Controller is not running properly.")

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_28_0
    def test_cross_tenant_auto_upload(self, cleanup):
        """
        Input File on Local Filesystem, Test for cloning of cross tenant
        references on the Controller,
        AutoUpload Flow
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                option=setup.get('option'),
                controller_ip=setup.get('controller_ip_17_1_1'),
                user=setup.get('controller_user_17_1_1'),
                password=setup.get('controller_password_17_1_1'),
                skip_pki=True)

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_29_0
    def test_reboot_clean_v11_17_1_1(self, cleanup):
        """""
        Verify Controller v17.1.1 is running and clean reboot avi api.
        After controller setup completed, upload the AviInternal
        certificate file.
        """
        is_up = verify_controller_is_up(file_attribute['controller_ip_17_1_1'],
                                        file_attribute[
                                            'controller_user_17_1_1'],
                                        file_attribute[
                                            'controller_password_17_1_1'])
        if is_up:
            clean_reboot(file_attribute['controller_ip_17_1_1'],
                         file_attribute['controller_user_17_1_1'],
                         file_attribute['controller_password_17_1_1'],
                         file_attribute['controller_version_v17'],
                         file_attribute['license_file_path'])
            print("Controller is running properly.")
        else:
            print("Controller is not running properly.")

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_30_0
    def test_auto_upload_v11_17_1_1(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        AutoUpload Flow
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                output_file_path=setup.get('output_file_path'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                option=setup.get('option'),
                controller_ip=setup.get('controller_ip_17_1_1'),
                user=setup.get('controller_user_17_1_1'),
                password=setup.get('controller_password_17_1_1'),
                skip_pki=True)

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_31_0
    def test_create_ansible_object_creation_v11(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1
        Create Ansible Script based on Flag
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                output_file_path=setup.get('output_file_path'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                ansible=setup.get('ansible'),
                skip_pki=True)
        file_name = output_file + '/avi_config_create_object.yml'
        with open(file_name) as o_file:
            file_object = yaml.load(o_file, Loader=yaml.Loader)
            assert file_object[0].get('tasks', False)

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_32_0
    def test_reboot_clean_ansible_v11_17_1_1(self, cleanup):
        """""
        Verify Controller v17.1.1 is running and clean reboot avi api.
        After controller setup completed, upload the AviInternal
        certificate file.
        """
        is_up = verify_controller_is_up(file_attribute['controller_ip_17_1_1'],
                                        file_attribute[
                                            'controller_user_17_1_1'],
                                        file_attribute[
                                            'controller_password_17_1_1'])
        if is_up:
            clean_reboot(file_attribute['controller_ip_17_1_1'],
                         file_attribute['controller_user_17_1_1'],
                         file_attribute['controller_password_17_1_1'],
                         file_attribute['controller_version_v17'],
                         file_attribute['license_file_path'])
            print("Controller is running properly.")
        else:
            print("Controller is not running properly.")

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_33_0
    def test_ansible_object_auto_upload_v11_17_1_1(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1
        AutoUpload Flow
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                output_file_path=setup.get('output_file_path'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v11'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                ansible=setup.get('ansible'),
                skip_pki=True)
        print(subprocess.check_output('pip install avisdk --upgrade',
                                      shell=True))
        print(subprocess.check_output(
            '/usr/local/bin/ansible-galaxy install avinetworks.avisdk avinetworks.avimigrationtools',
            shell=True))
        try:
            output = ansible_runner.run(
                playbook=setup.get('f5_ansible_object'),
                extravars={'controller': setup.get('controller_ip_17_1_1'),
                           'username': setup.get('controller_user_17_1_1'),
                           'password': setup.get('controller_password_17_1_1')},
                verbosity=3,
                quiet=True)
            playbook_stats = output.stats
            playbook_output = output.stdout.read()
            mylogger.info('ansible playbook output: \n{}'.format(playbook_output))
        except:
            mylogger.info('Failed to create object on controller output: \n{}'.format(playbook_output))
            output = False
        assert output

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_34_0
    def test_create_ansible_object_v10(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1
        Create Ansible Script based on Flag
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                output_file_path=setup.get('output_file_path'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                ansible=setup.get('ansible'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_35_0
    def test_vs_level_status_true_v10(self, cleanup):
        """
        Input File on Local Filesystem, VS level option true usage
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                f5_config_version=setup.get('file_version_v10'),
                controller_version=setup.get('controller_version_v17'),
                vs_level_status=setup.get('vs_level_status'),
                f5_ssh_port=setup.get('f5_ssh_port'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_36_0
    def test_vs_level_status_false_v10(self, cleanup):
        """
        Input File on Local Filesystem, VS level option false usage
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_config_version=setup.get('file_version_v10'),
                f5_ssh_port=setup.get('f5_ssh_port'))

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_37_0
    def test_http_cookie_type_on_file_v10(self):

        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                f5_config_version=setup.get('file_version_v10'),
                controller_version=setup.get('controller_version_v17'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                output_file_path=setup.get('output_file_path'))
        file_name = output_file + '/bigip_v10-Output.json'
        with open(file_name) as o_file:
            file_object = yaml.load(o_file, Loader=yaml.Loader)
        persistence_profiles = file_object['ApplicationPersistenceProfile']
        for p_type in persistence_profiles:
            if "COOKIE" in p_type['persistence_type']:
                assert (p_type['persistence_type'] ==
                        'PERSISTENCE_TYPE_HTTP_COOKIE')

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_38_0
    def test_http_cookie_type_on_file_v11(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                output_file_path=setup.get('output_file_path'))
        file_name = output_file + '/hol_advanced_bigip-Output.json'
        with open(file_name) as o_file:
            file_object = yaml.load(o_file, Loader=yaml.Loader)
        persistence_profiles = file_object['ApplicationPersistenceProfile']
        for p_type in persistence_profiles:
            if "COOKIE" in p_type['persistence_type']:
                assert (p_type['persistence_type'] ==
                        'PERSISTENCE_TYPE_HTTP_COOKIE')

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_39_0
    def test_vrf_flag_on_file_v10(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                f5_config_version=setup.get('file_version_v10'),
                controller_version=setup.get('controller_version_v17'),
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                vrf=setup.get('vrf'),
                )

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_39_0
    def test_vrf_flag_on_file_v10(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                f5_config_version=setup.get('file_version_v10'),
                controller_version=setup.get('controller_version_v17'),
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                segroup=setup.get('segroup')
                )

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_40_0
    def test_vrf_flag_on_file_v11(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                vrf=setup.get('vrf'),
                )

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_40_0
    def test_vrf_flag_on_file_v11(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                segroup=setup.get('segroup')
                )

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_41_0
    def test_error_and_warning_count_on_file_v11(self):
        set_update_count()
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'))

        assert get_count('error') == 0

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_42_0
    def test_error_and_warning_count_on_file_v10(self):
        set_update_count()
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                f5_config_version=setup.get('file_version_v10'),
                controller_version=setup.get('controller_version_v17'),
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'))

        assert get_count('error') == 0

    @pytest.mark.travis
    def test_pool_hm_ref_v11(self, cleanup):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['Pool']

            pool_with_hm = [data for data in vs_object if data['name'] == "hol-advanced-pool-01"]
            # Check if health monitor ref migrated to Avi
            assert pool_with_hm[0].get('health_monitor_refs')

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_43_0
    def test_pool_sharing_on_v11(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']

            first_vs = [data for data in vs_object if data['name'] == "11-hol-advanced-http-vs"]
            second_vs = [data for data in vs_object if data['name'] == "12-hol-advanced-http-vs"]

            first_pool = first_vs[0]['pool_ref'].split(
                'name=')[1].split('&')[0]
            second_pool = second_vs[0]['pool_ref'].split(
                'name=')[1].split('&')[0]
            assert first_pool == second_pool

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_44_0
    def test_pool_without_sharing_on_v11(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']

            first_vs = [data for data in vs_object if data['name'] == "10-hol-advanced-http-vs"]
            second_vs = [data for data in vs_object if data['name'] == "11-hol-advanced-http-vs"]

            first_pool = first_vs[0]['pool_ref'].split('name=')[1].split('&')[0]
            second_pool = second_vs[0]['pool_ref'].split('name=')[1].split(
                '&')[0]
            assert first_pool != second_pool

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_45_0
    def test_pool_sharing_on_v10(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                f5_config_version=setup.get('file_version_v10'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'))

        o_file = "%s/%s" % (output_file, "bigip_v10-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']

            first_vs = [data for data in vs_object if data['name'] ==
                        "F5-v10-VIP-443-002"]
            second_vs = [data for data in vs_object if data['name'] ==
                         "F5-v10-VIP-443-003"]

            first_pool = first_vs[0]['pool_ref'].split('name=')[1].split('&')[0]
            second_pool = second_vs[0]['pool_ref'].split('name=')[1].split(
                '&')[0]
            assert first_pool == second_pool

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_46_0
    def test_pool_without_sharing_on_v10(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                f5_config_version=setup.get('file_version_v10'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'))

        o_file = "%s/%s" % (output_file, "bigip_v10-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']

            first_vs = [data for data in vs_object if data['name'] ==
                        "F5-v10-VIP-443-001"]
            second_vs = [data for data in vs_object if data['name'] ==
                         "F5-v10-VIP-443-002"]

            first_pool = first_vs[0]['pool_ref'].split('name=')[1].split('&')[0]
            second_pool = second_vs[0]['pool_ref'].split('name=')[1].split(
                '&')[0]
            assert first_pool != second_pool

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_47_0
    def test_rule_config_v11(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                output_file_path=setup.get('output_file_path'),
                custom_config=setup.get('custom_config_file'),
                f5_ssh_port=setup.get('f5_ssh_port'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_datascript = data['VSDataScriptSet']
            vs_object = data['VirtualService']
            http_policy_set = data['HTTPPolicySet']
            network_security_policy = data['NetworkSecurityPolicy']

            vs_data = [data for data in vs_object if data['name']
                       == "01-hol-advanced-http-vs"]
            data_script = vs_data[0]['vs_datascripts']
            for i in data_script:
                ds_name = i['vs_datascript_set_ref'].split('name=')[1].split(
                    '&')[0]
                script_set = [data['name'] for data in vs_datascript if
                              data['name'] == ds_name][0]
                print(script_set, " ", ds_name)
                assert script_set == ds_name

            vs_data = [data for data in vs_object if data['name']
                       == "11-hol-advanced-http-vs"]
            httppolicies = vs_data[0]['http_policies']
            for i in httppolicies:
                policy_name = i['http_policy_set_ref'].split('name=')[1].split(
                    '&')[0]
                httppolicy = [data['name'] for data in http_policy_set
                              if data['name'] == policy_name][0]
                print(policy_name, " ", httppolicy)
                assert policy_name == httppolicy

            vs_data_for_policy_set = [data for data in vs_object if
                                      data['name'] == "21-hol-advanced-http-vs"]
            vsdatascript = vs_data_for_policy_set[0]['vs_datascripts']
            for i in vsdatascript:
                ds_name = i['vs_datascript_set_ref'].split('name=')[1].split(
                    '&')[0]
                script_set = [data['name'] for data in vs_datascript
                              if data['name'] == ds_name][0]
                print(script_set, " ", ds_name)
                assert script_set == ds_name

            vs_data = [data for data in vs_object if data['name'] == "32-hol-advanced-http-vs"]
            httppolicy = vs_data[0]['http_policies']
            for i in httppolicy:
                policy_name = i['http_policy_set_ref'].split('name=')[1].split(
                    '&')[0]
                if policy_name == '_sys_https_redirect-EngVIP':
                    httppolicy = [data['name'] for data in http_policy_set if
                                  data['name'] == policy_name
                                  and '_sys_https_redirect-EngVIP'][0]
                    print(policy_name, " ", httppolicy)
                    assert policy_name == httppolicy

            vs_data = [data for data in vs_object if data['name'] == "41-hol-advanced-http-vs"]
            policy_ref = vs_data[0]['network_security_policy_ref']
            policy_name = policy_ref.split('name=')[1].split('&')[0]
            network_profile_name = [i['name'] for i in network_security_policy
                                    if i['name'] == policy_name][0]
            assert network_profile_name == policy_name

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_48_0
    def test_singke_vs_rules_with_multiple_objects(self):

        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                output_file_path=setup.get('output_file_path'),
                custom_config=setup.get('custom_config_file'),
                f5_ssh_port=setup.get('f5_ssh_port'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']
            http_policy_set = data['HTTPPolicySet']
            network_security_policy = data['NetworkSecurityPolicy']

        vs_data = [data for data in vs_object if data['name']
                   == "40-hol-advanced-http-vs"]
        httppolicy = vs_data[0]['http_policies']
        for i in httppolicy:
            policy_name = i['http_policy_set_ref'].split('name=')[1].split(
                '&')[0]
            if policy_name == 'Test-support-Profile-HTTP-HTTP-Policy-Set':
                httppolicy = [data['name'] for data in http_policy_set if
                              data['name'] == policy_name and
                              'Test-support-Profile-HTTP-HTTP-Policy-Set'][0]
                print(policy_name, " ", httppolicy)
                assert policy_name == httppolicy

        vs_data = [data for data in vs_object if data['name']
                   == "40-hol-advanced-http-vs"]
        policy_ref = vs_data[0]['network_security_policy_ref']
        policy_name = policy_ref.split('name=')[1].split('&')[0]
        network_profile_name = [i['name'] for i in network_security_policy
                                if i['name'] == policy_name][0]
        assert network_profile_name == policy_name

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_49_0
    def test_custom_config_for_hm(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                output_file_path=setup.get('output_file_path'),
                custom_config=setup.get('custom_config_file'),
                f5_ssh_port=setup.get('f5_ssh_port'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(input_role_config_file) as i_file:
            custom_config = yaml.load(i_file, Loader=yaml.Loader)

        with open(o_file) as json_file:
            data = json.load(json_file)
            hm_object = data['HealthMonitor']
            hmdata = [hm for hm in hm_object if hm['name'] == "dns_hol"][0]
        config_data = custom_config['healthmonitor_custom_config'][0]
        assert hmdata['failed_checks'] == config_data['avi_config'][
            'failed_checks']
        assert hmdata['send_interval'] == config_data['avi_config'][
            'send_interval']
        assert hmdata['receive_timeout'] == config_data['avi_config'][
            'receive_timeout']
        assert (hmdata['external_monitor']['command_code'] ==
                config_data['avi_config']['external_monitor']['command_code'])

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_50_0
    def test_reboot_clean_v11_17_1_1_for_custom_config(self, cleanup):
        """""
        Verify Controller v17.1.1 is running and clean reboot avi api.
        After controller setup completed, upload the AviInternal
        certificate file.
        """
        is_up = verify_controller_is_up(file_attribute['controller_ip_17_1_1'],
                                        file_attribute[
                                            'controller_user_17_1_1'],
                                        file_attribute[
                                            'controller_password_17_1_1'])
        if is_up:
            clean_reboot(file_attribute['controller_ip_17_1_1'],
                         file_attribute['controller_user_17_1_1'],
                         file_attribute['controller_password_17_1_1'],
                         file_attribute['controller_version_v17'],
                         file_attribute['license_file_path'])
            print("Controller is running properly.")
        else:
            print("Controller is not running properly.")

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_51_0
    def test_custom_config_object_upload(self):

        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                controller_ip=setup.get('controller_ip_17_1_1'),
                user=setup.get('controller_user_17_1_1'),
                password=setup.get('controller_password_17_1_1'),
                option=setup.get('option'),
                output_file_path=setup.get('output_file_path'),
                custom_config=setup.get('custom_config_file'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                skip_pki=True)

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_52_0
    def test_vs_level_status_with_v11(self):

        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                output_file_path=setup.get('output_file_path'),
                vs_level_status=setup.get('vs_level_status'),
                f5_ssh_port=setup.get('f5_ssh_port')
                )
        self.excel_path = os.path.abspath(
            os.path.join(
                output_file, 'hol_advanced_bigip-ConversionStatus.xlsx'
            )
        )
        assert output_vs_level_status(self.excel_path)

    @pytest.mark.travis
    def test_vs_level_status_and_segroup_with_v11(self):

        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                output_file_path=setup.get('output_file_path'),
                vs_level_status=setup.get('vs_level_status'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                segroup=setup.get('segroup')
                )
        self.excel_path = os.path.abspath(
            os.path.join(
                output_file, 'hol_advanced_bigip-ConversionStatus.xlsx'
            )
        )
        assert output_vs_level_status(self.excel_path)

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_53_0
    def test_reboot_clean_for_segroup_v11_17_1_1(self, cleanup):
        """""
        Verify Controller v17.1.1 is running and clean reboot avi api.
        After controller setup completed, upload the AviInternal
        certificate file.
        """
        is_up = verify_controller_is_up(
            file_attribute['controller_ip_17_1_1'],
            file_attribute['controller_user_17_1_1'],
            file_attribute['controller_password_17_1_1'])
        if is_up:
            clean_reboot(file_attribute['controller_ip_17_1_1'],
                         file_attribute['controller_user_17_1_1'],
                         file_attribute['controller_password_17_1_1'],
                         file_attribute['controller_version_v17'],
                         file_attribute['license_file_path'])
            print("Controller is running properly.")
        else:
            print("Controller is not running properly.")

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_54_0
    def test_segroup_and_upload_v11_17_1_1(self, cleanup):
        """
        Input File on Local Filesystem, Test for Controller v17.1.1,
        AutoUpload Flow
        """
        res = create_segroup(
            file_attribute['controller_ip_17_1_1'],
            file_attribute['controller_user_17_1_1'],
            file_attribute['controller_password_17_1_1'],
            setup.get('segroup'))

        if res.status_code in [200, 201]:
            f5_conv(
                bigip_config_file=setup.get('config_file_name_v11'),
                output_file_path=setup.get('output_file_path'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                option=setup.get('option'),
                controller_ip=setup.get('controller_ip_17_1_1'),
                user=setup.get('controller_user_17_1_1'),
                password=setup.get('controller_password_17_1_1'),
                segroup=setup.get('segroup'),
                skip_pki=True)
        else:
            raise Exception("Controller segroup creation faild %s" %
                            res.content)

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_55_0
    def test_reboot_clean_v11_17_1_1_for_vrf_ref(self, cleanup):
        """""
        Verify Controller v17.1.1 is running and clean reboot avi api.
        After controller setup completed, upload the AviInternal
        certificate file.
        """
        is_up = verify_controller_is_up(
            file_attribute['controller_ip_17_1_1'],
            file_attribute['controller_user_17_1_1'],
            file_attribute['controller_password_17_1_1'])
        if is_up:
            clean_reboot(file_attribute['controller_ip_17_1_1'],
                         file_attribute['controller_user_17_1_1'],
                         file_attribute['controller_password_17_1_1'],
                         file_attribute['controller_version_v17'],
                         file_attribute['license_file_path'])
            print("Controller is running properly.")
        else:
            print("Controller is not running properly.")

    @pytest.mark.skip_travis
    @pytest.mark.TCID1_48_1497_56_0
    def test_vrf_ref_upload_v11_17_1_1(self):
        res = create_vrf_context(
            file_attribute['controller_ip_17_1_1'],
            file_attribute['controller_user_17_1_1'],
            file_attribute['controller_password_17_1_1'],
            vrf_name=setup.get('vrf'))

        if res.status_code in [200, 201]:
            f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                    f5_config_version=setup.get('file_version_v11'),
                    controller_version=setup.get('controller_version_v17'),
                    output_file_path=setup.get('output_file_path'),
                    controller_ip=setup.get('controller_ip_17_1_1'),
                    user=setup.get('controller_user_17_1_1'),
                    password=setup.get('controller_password_17_1_1'),
                    option=setup.get('option'),
                    vrf=setup.get('vrf'), skip_pki=True)
        else:
            raise Exception("Controller vrf creation faild %s" % res.content)

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_57_0
    def test_application_profile_on_v11(self, cleanup):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                output_file_path=setup.get('output_file_path'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']
            app_ref = []
            for vs in vs_object:
                if vs['name'] == "F5-VIP-80-001":
                    app_ref.append(vs['application_profile_ref'])
                elif vs['name'] == "dns_vs_up":
                    app_ref.append(vs['application_profile_ref'])
                elif vs['name'] == "Opcito-vs":
                    app_ref.append(vs['application_profile_ref'])
            for each_ref in app_ref:
                profile_name = each_ref.split('name=')[1].split('&')[0]
                assert profile_name == "System-L4-Application"

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_58_0
    def test_vs_filter_on_v11(self, cleanup):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                vs_filter=setup.get('vs_filter'),
                vrf=setup.get('vrf'),
                output_file_path=setup.get('output_file_path'))
        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        assert os.path.exists(o_file)

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_59_0
    def test_pool_sharing_policy(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                output_file_path=setup.get('output_file_path'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']
            http_policy_set = data['HTTPPolicySet']
            pools = data['Pool']

        vs_data1 = [data['http_policies'] for data in vs_object if data['name']
                    == "33-hol-advanced-http-vs"][0]

        vs_data2 = [data['http_policies'] for data in vs_object if data['name']
                    == "34-hol-advanced-http-vs"][0]
        vs_list = list()
        vs_list.append(vs_data1[0])
        vs_list.append(vs_data2[0])

        for i in vs_list:
            policy_name = i['http_policy_set_ref'].split('name=')[1].split('&')[
                0]
            rules = [data['http_request_policy']['rules'] for data
                     in http_policy_set if data['name'] == policy_name][0]
            for r in rules:
                pool = r['switching_action']['pool_ref'].split(
                    'name=')[1].split('&')[0]
                pool_name = [data['name'] for data in pools if data['name'] ==
                             pool][0]
                assert pool == pool_name

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_60_0
    def test_check_header_insert_policy_on_v11(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                output_file_path=setup.get('output_file_path'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']
            http_policy_set = data['HTTPPolicySet']

        vs_data = [data for data in vs_object if data['name'] == "81-hol-advanced-http-vs-dmz"]
        httppolicies = vs_data[0]['http_policies']
        for i in httppolicies:
            policy_name = i['http_policy_set_ref'].split('name=')[1].split(
                '&')[0]
            httppolicy = [data['name'] for data in http_policy_set if
                          data['name'] == policy_name][0]
            assert policy_name == httppolicy

    @pytest.mark.travis
    @pytest.mark.TCID1_48_1497_61_0
    def test_check_health_monitor_request_url(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                output_file_path=setup.get('output_file_path'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            hm_object = data['HealthMonitor']
            monitor_urls = []
            for monitor in hm_object:
                if 'https_monitor' in monitor:
                    monitor_urls.append(monitor['https_monitor'][
                                            'http_request'])
                elif 'http_monitor' in monitor:
                    monitor_urls.append(monitor['http_monitor']['http_request'])
            for eachUrl in monitor_urls:
                request = eachUrl.split('\\r')[0]
                assert (request.endswith('HTTP/1.1') or
                        request.endswith('HTTP/1.0'))

    @pytest.mark.travis
    def test_single_http_req_policy_with_multiple_vs(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                output_file_path=setup.get('output_file_path'),
                custom_config=setup.get('custom_config_file'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']
            http_policy_set = data['HTTPPolicySet']

        vs_data_of_va1 = [data for data in vs_object if data['name']
                          == "33-hol-advanced-http-vs"]
        vs_data_of_va2 = [data for data in vs_object if data['name']
                          == "34-hol-advanced-http-vs"]
        httppolicydata1 = vs_data_of_va1[0]['http_policies']
        httppolicydata2 = vs_data_of_va2[0]['http_policies']
        for i in httppolicydata1:
            policy_name = i['http_policy_set_ref'].split('name=')[1].split(
                '&')[0]
            if 'hol_context_switch_policy' in policy_name:
                policy_name_1 = [data['name'] for data in http_policy_set
                                 if data['name'] == policy_name][0]
                print(policy_name, " ", policy_name_1)
                assert policy_name == policy_name_1

        for i in httppolicydata2:
            policy_name = i['http_policy_set_ref'].split('name=')[1].split(
                '&')[0]
            if 'hol_context_switch_policy' in policy_name:
                policy_name_2 = [data['name'] for data in http_policy_set
                                 if data['name'] == policy_name][0]
                print(policy_name, " ", policy_name_2)
                assert policy_name == policy_name_2

    @pytest.mark.travis
    def test_check_dup_of_key_should_not_be_in_json(self):
        f5_conv(
            bigip_config_file=setup.get('config_file_name_v11'),
            f5_config_version=setup.get('file_version_v11'),
            controller_version=setup.get('controller_version_v17'),
            tenant=file_attribute['tenant'],
            cloud_name=file_attribute['cloud_name'],
            output_file_path=setup.get('output_file_path'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)

        for key in data.keys():
            if isinstance(data[key], list):
                for i in data[key]:
                    assert 'dup_of' not in i.keys()

    @pytest.mark.travis
    def test_distinct_app_profile(self):
        f5_conv(
            bigip_config_file=setup.get('config_file_name_v11'),
            f5_config_version=setup.get('file_version_v11'),
            controller_version=setup.get('controller_version_v17'),
            tenant=file_attribute['tenant'],
            cloud_name=file_attribute['cloud_name'],
            output_file_path=setup.get('output_file_path'),
            distinct_app_profile=setup.get('distinct_app_profile'))

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)

        assert len(data['ApplicationProfile']) > 34
        vs = [vs for vs in data['VirtualService']
              if vs['name'] == '33-hol-advanced-http-vs']
        assert '33-hol-advanced-http-vs' in vs[0]['application_profile_ref']

    @pytest.mark.travis
    def test_http_policy_sharing_on_v11(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                reuse_http_policy=True
                )

        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']
            first_vs = [vs for vs in vs_object if vs['name']
                        == "81-hol-advanced-http-vs-dmz"][0]
            second_vs = [vs for vs in vs_object if vs['name']
                         == "82-hol-advanced-http-vs-dmz"][0]
            vs1_http_policy = first_vs['http_policies'][0] \
                ['http_policy_set_ref'].split("=")[-1]
            vs2_http_policy = second_vs['http_policies'][0] \
                ['http_policy_set_ref'].split("=")[-1]
            assert vs1_http_policy == vs2_http_policy
            http_policies = data['HTTPPolicySet']
            shared_http_policy = [policy for policy in http_policies
                                  if "hol_hdr_insert-HTTP-Policy-Set"
                                  in policy['name']]
            assert len(shared_http_policy) == 1

    @pytest.mark.travis
    def test_http_policy_sharing_on_v10(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v10'),
                f5_config_version=setup.get('file_version_v10'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path'),
                f5_ssh_port=setup.get('f5_ssh_port'),
                reuse_http_policy=True)

        o_file = "%s/%s" % (output_file, "bigip_v10-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService']
            first_vs = [vs for vs in vs_object if vs['name']
                        == "vs_http_policy_share_1"][0]
            second_vs = [vs for vs in vs_object if vs['name']
                         == "vs_http_policy_share_2"][0]
            vs1_http_policy = first_vs['http_policies'][0] \
                ['http_policy_set_ref'].split("=")[-1]
            vs2_http_policy = second_vs['http_policies'][0] \
                ['http_policy_set_ref'].split("=")[-1]
            assert vs1_http_policy == vs2_http_policy == \
                   '_sys_https_redirect'
            http_policies = data['HTTPPolicySet']
            shared_http_policy = [policy for policy in http_policies
                                  if "_sys_https_redirect"
                                  in policy['name']]
            assert len(shared_http_policy) == 1

    @pytest.mark.travis
    def test_pool_vrf_on_v11(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path')
                )
        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        custom_vrf_pools = {"Peer_test": "vrf-101"}
        custom_vrf_vs = {"vs_custome_vrf": "vrf-101"}
        with open(o_file) as json_file:
            data = json.load(json_file)
            pool_objects = data['Pool']
            vs_objects = data['VirtualService']
            for pool in pool_objects:
                if pool["name"] in custom_vrf_pools:
                    assert custom_vrf_pools[pool["name"]] in pool["vrf_ref"]
                else:
                    assert "global" in pool["vrf_ref"]
            for vs in vs_objects:
                if vs["name"] in custom_vrf_vs:
                    assert custom_vrf_vs[vs["name"]] in vs["vrf_context_ref"]
                else:
                    assert "global" in vs["vrf_context_ref"]

    @pytest.mark.travis
    def test_monitor_config(self):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path')
                )
        o_file = "%s/%s" % (output_file, "hol_advanced_bigip-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            ssl_cert_objects = data['SSLKeyAndCertificate']
            ssl_profile_objects = data['SSLProfile']
            expected_cert = [ssl_cert for ssl_cert in ssl_cert_objects
                             if ssl_cert['name'] == 'monitor.fmr.com.crt']
            expected_ssl_profile = [ssl_profile for ssl_profile in ssl_profile_objects
                                    if ssl_profile['name'] == 'client_ssl_profile']
            assert expected_cert, "Expected cert monitor.fmr.com.crt not found"
            assert expected_ssl_profile, "Expected ssl profile monitor.fmr.com not found"

    @pytest.mark.travis
    def test_configuration_with_config_yaml(self, cleanup):
        f5_conv(args_config_file=setup.get('args_config_file'))
        o_file = "%s/%s" % (output_file, "bigip_v11-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = data['VirtualService'][0]
            assert not vs_object.get('enabled')
        assert not os.path.exists("%s/%s" % (output_file, "avi_config_create_object.yml"))
        assert not os.path.exists("%s/%s" % (output_file, "avi_config_delete_object.yml"))

    @pytest.mark.travis
    def test_configuration_with_overriding_config_yaml(self, cleanup):
        f5_conv(args_config_file=setup.get('args_config_file'),
                ansible=True, vs_state='enable')
        o_file = "%s/%s" % (output_file, "bigip_v11-Output.json")
        with open(o_file) as json_file:
            data = json.load(json_file)
            vs_object = [vs for vs in data['VirtualService'] if vs['name'] == 'vs_2_up'][0]
            assert vs_object.get('enabled')
        assert os.path.exists("%s/%s" % (output_file, "avi_config_create_object.yml"))
        assert os.path.exists("%s/%s" % (output_file, "avi_config_delete_object.yml"))

    def test_profile_http_na_enforcement(self, cleanup):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path')
                )
        self.excel_path = os.path.abspath(
            os.path.join(
                output_file, 'hol_advanced_bigip-ConversionStatus.xlsx'
            )
        )
        data = pd.read_excel(self.excel_path)
        for k, row in data.iterrows():
            if row['F5 SubType'] in ["http"]:
                na_attr = row['Not Applicable']
                na_attr = common_avi_util.format_string_to_json(na_attr)
                for item in na_attr:
                    if isinstance(item, dict):
                        for k in item.keys():
                            if k == 'enforcement':
                                enf = item[k]
                                for item in enf:
                                    assert item in ['max-requests', 'truncated-redirects',]
                                break

    def test_profile_indirect_http_enforcement(self, cleanup):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path')
                )
        self.excel_path = os.path.abspath(
            os.path.join(
                output_file, 'hol_advanced_bigip-ConversionStatus.xlsx'
            )
        )
        data = pd.read_excel(self.excel_path)
        for k, row in data.iterrows():
            if row['F5 SubType'] in ["http"]:
                indirect_attr = row['Indirect mapping']
                indirect_attr = common_avi_util.format_string_to_json(indirect_attr)
                for item in indirect_attr:
                    if isinstance(item, dict):
                        for k in item.keys():
                            if k == 'enforcement':
                                enf = item[k]
                                for item in enf:
                                    assert item in ['pipeline']
                                break


    def test_profile_http_skipped_enforcement(self, cleanup):
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path')
                )
        self.excel_path = os.path.abspath(
            os.path.join(
                output_file, 'hol_advanced_bigip-ConversionStatus.xlsx'
            )
        )
        data = pd.read_excel(self.excel_path)
        for k, row in data.iterrows():
            if row['F5 SubType'] in ["http"]:
                if row['Status'] not in ['SUCCESSFUL', 'SKIPPED']:
                    skipped_attr = row['Skipped settings']
                    skipped_attr = common_avi_util.format_string_to_json(skipped_attr)
                    for item in skipped_attr:
                        if isinstance(item, dict):
                            for k in item.keys():
                                if k == 'enforcement':
                                    enf = item[k]
                                    for item in enf:
                                        assert item not in ['max-requests', 'truncated-redirects', 'pipeline']
                                    break

    def test_skipped_objects(self,cleanup):
        """
        test case for skipped objct
        """
        f5_conv(bigip_config_file=setup.get('config_file_name_v11'),
                f5_config_version=setup.get('file_version_v11'),
                controller_version=setup.get('controller_version_v17'),
                tenant=file_attribute['tenant'],
                cloud_name=file_attribute['cloud_name'],
                no_profile_merge=file_attribute['no_profile_merge'],
                output_file_path=setup.get('output_file_path')
                )
        self.excel_path = os.path.abspath(
            os.path.join(
                output_file, 'hol_advanced_bigip-ConversionStatus.xlsx'
            )
        )
        data = pd.read_excel(self.excel_path)
        for k, row in data.iterrows():
            if row['F5 SubType'] in ["universal", "dest-addr"]:
                assert row['Status'] == 'SKIPPED'

    def test_tenant_ref(self):
        input =["/common/test-monitor", "common/test-monitor","common test-monitor"]
        for ipt in input:
            tenant, name = common_avi_util.get_tenant_ref(ipt)
            assert tenant == tenant.strip()
            assert tenant != "common"
            assert not name.__contains__("name=")
            assert not name.__contains__("/")
            assert not name.__contains__("=")


def teardown():
    pass
