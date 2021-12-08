# !/usr/bin/env python3
from avi.migrationtools import avi_rest_lib
from avi.migrationtools.ansible.ansible_config_converter \
    import AviAnsibleConverterMigration
from avi.migrationtools.nsxt_converter import nsxt_config_converter
import argparse

ARG_CHOICES = {
    'option': ['cli-upload', 'auto-upload']

}


def convert_lb_config(args):
    output_file_path = (args.output_file_path if args.output_file_path
                        else 'output')
    alb_config = nsxt_config_converter.convert(
        args.nsxt_ip, args.nsxt_user, args.nsxt_passord, args.nsxt_port,
        output_file_path, args.cloud_name, args.prefix)
    if args.ansible:
        convert(args, alb_config)
    if args.option == 'auto-upload':
        upload_config_to_controller(alb_config, args)


def upload_config_to_controller(alb_config, args):
    avi_rest_lib.upload_config_to_controller(
        alb_config, args.controller_ip, args.user, args.password, args.tenant)


def convert(args, alb_config):
    output_file_path = (args.output_file_path if args.output_file_path
                        else 'output')
    avi_traffic = AviAnsibleConverterMigration(
        alb_config, output_file_path, args.prefix, args.not_in_use,
        skip_types=args.ansible_skip_types,
        controller_version=args.controller_version,
        filter_types=args.ansible_filter_types)
    avi_traffic.write_ansible_playbook(
        args.nsxt_ip, args.nsxt_user, args.nsxt_passord, 'nsxt')


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
    convert_lb_config(args)
