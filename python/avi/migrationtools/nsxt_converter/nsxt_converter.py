# !/usr/bin/env python3
import os

from avi.migrationtools import avi_rest_lib
from avi.migrationtools.ansible.ansible_config_converter import \
    AviAnsibleConverterMigration
from avi.migrationtools.avi_converter import AviConverter
from avi.migrationtools.avi_migration_utils import get_count
from avi.migrationtools.nsxt_converter import nsxt_config_converter
import argparse

ARG_CHOICES = {
    'option': ['cli-upload', 'auto-upload'],
    'migrate_option': ['Avi', 'NSX']

}

class NsxtConverter(AviConverter):
    def __init__(self, args):
        '''

        :param args:
        '''
        self.nsxt_ip = args.nsxt_ip
        self.nsxt_user = args.nsxt_user
        self.nsxt_passord = args.nsxt_passord
        self.nsxt_port = args.nsxt_port
        self.cloud_name = args.cloud_name
        self.prefix = args.prefix
        self.prefix = args.prefix
        self.controller_ip = args.controller_ip
        self.user = args.user
        self.password = args.password
        self.tenant = args.tenant
        self.not_in_use = args.not_in_use
        self.ansible_skip_types = args.ansible_skip_types
        self.controller_version = args.controller_version
        self.ansible_filter_types = args.ansible_filter_types
        self.output_file_path = args.output_file_path if args.output_file_path \
            else 'output'
        self.migrate_to = args.migrate_to

    def conver_lb_config(self):
        if not os.path.exists(self.output_file_path):
            os.mkdir(self.output_file_path)
        self.init_logger_path()
        output_dir = os.path.normpath(self.output_file_path)
        alb_config = nsxt_config_converter.convert(
            self.nsxt_ip, self.nsxt_user, self.nsxt_passord, self.nsxt_port,
            self.output_file_path, self.cloud_name, self.prefix, self.migrate_to
                                                   )
        avi_config = self.process_for_utils(alb_config)

        output_path = (output_dir + os.path.sep + self.nsxt_ip + os.path.sep +
                       "output")
        self.write_output(avi_config, output_path, 'avi_config.json')
        if args.ansible:
            self.convert(alb_config)
        if args.option == 'auto-upload':
            self.upload_config_to_controller(alb_config)
        print("Total Warning: ", get_count('warning'))
        print("Total Errors: ", get_count('error'))

    def upload_config_to_controller(self, alb_config):
        avi_rest_lib.upload_config_to_controller(
            alb_config, self.controller_ip, self.user, self.password,
            self.tenant)

    def convert(self, alb_config):
        avi_traffic = AviAnsibleConverterMigration(
            alb_config, self.output_file_path, self.prefix, self.not_in_use,
             skip_types=self.ansible_skip_types,
             controller_version=self.controller_version,
            filter_types=self.ansible_filter_types)
        avi_traffic.write_ansible_playbook(
            self.nsxt_ip, self.nsxt_user, self.nsxt_passord, 'nsxt')


if __name__ == "__main__":
    HELP_STR = """
    Usage:
    python nsxt_converter.py -n 192.168.100.101 -u admin -p password 
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, description=HELP_STR)

    # Create Ansible Script based on Flag
    parser.add_argument('--ansible',
                        help='Flag for create ansible file',
                        action='store_true')

    parser.add_argument('-n', '--nsxt_ip', required=True,
                        help='Ip of NSXT')
    parser.add_argument('-u', '--nsxt_user', required=True,
                        help='NSX-T User name')
    parser.add_argument('-p', '--nsxt_passord', required=True,
                        help='NSX-T Password')
    parser.add_argument('-port', '--nsxt_port', default=443,
                        help='NSX-T Port')
    parser.add_argument('-o', '--output_file_path',
                        help='Folder path for output files to be created in',
                        )
    parser.add_argument('--prefix', help='Prefix for objects')
    parser.add_argument('--cloud_name', help='cloud name for auto upload',
                        required=True)
    parser.add_argument('--password',
                        help='controller password for auto upload. Input '
                             'prompt will appear if no value provided')
    parser.add_argument('-c', '--controller_ip',
                        help='controller ip for auto upload')
    parser.add_argument('--controller_version',
                        help='Target Avi controller version')
    parser.add_argument('--user',
                        help='controller username for auto upload')
    parser.add_argument('-t', '--tenant', help='tenant name for auto upload')
    parser.add_argument('-O', '--option', choices=ARG_CHOICES['option'],
                        help='Upload option cli-upload genarates Avi config ' +
                             'file auto upload will upload config to ' +
                             'controller')
    parser.add_argument('--migrate_to', choices=ARG_CHOICES['migrate_option'],
                        help='Select migration to NSX-T ALB or ALB Controller',
                        default='Avi')
    # Added command line args to take skip type for ansible playbook
    parser.add_argument('--ansible_skip_types',
                        help='Comma separated list of Avi Object types to skip '
                             'during conversion.\n  Eg. -s DebugController,'
                             'ServiceEngineGroup will skip debugcontroller and '
                             'serviceengine objects')
    # Added command line args to take skip type for ansible playbook
    parser.add_argument('--ansible_filter_types',
                        help='Comma separated list of Avi Objects types to '
                             'include during conversion.\n Eg. -f '
                             'VirtualService, Pool will do ansible conversion '
                             'only for Virtualservice and Pool objects')
    parser.add_argument('--not_in_use',
                        help='Flag for skipping not in use object',
                        action="store_true")

    args = parser.parse_args()
    nsxt_converter = NsxtConverter(args)
    nsxt_converter.conver_lb_config()
