# !/usr/bin/env python3
import logging
import os
import json
import argparse
from datetime import datetime
from avi.migrationtools.avi_converter import AviConverter
from avi.migrationtools.avi_migration_utils import get_count
from avi.migrationtools.nsxt_converter.nsxt_util import NSXUtil

LOG = logging.getLogger(__name__)


class TrafficCutover(AviConverter):
    def __init__(self, args):
        '''

        :param args:
        '''
        self.nsxt_ip = args.nsxt_ip
        self.nsxt_user = args.nsxt_user
        self.nsxt_passord = args.nsxt_passord
        self.nsxt_port = args.nsxt_port

        self.controller_ip = args.controller_ip
        self.controller_version = args.controller_version
        self.user = args.user
        self.password = args.password
        self.cutover_vs = None
        if args.cutover:
            self.cutover_vs = \
                (set(args.cutover) if type(args.cutover) == list
                 else set(args.cutover.split(',')))
        self.output_file_path = args.output_file_path if args.output_file_path \
            else 'output'

        output_dir = os.path.normpath(self.output_file_path)
        output_path = output_dir + os.path.sep + self.nsxt_ip + os.path.sep + "output"

        # Load values from state file if not given on command line while executing script
        if self.nsxt_ip:
            output_path = output_dir + os.path.sep + self.nsxt_ip + os.path.sep + "output"
        with open(output_path + os.path.sep + "state.json", 'r') as file:
            data = json.load(file)
        if not self.nsxt_user:
            self.nsxt_user = data.get('nsxt_user')
        if not self.nsxt_port:
            self.nsxt_port = data.get('nsxt_port')
        if not self.controller_ip:
            self.controller_ip = data.get('controller_ip')
        if not self.controller_version:
            self.controller_version = data.get('controller_version')
        if not self.user:
            self.user = data.get('user')
        if not self.password:
            self.password = data.get('password')

    def initiate_cutover_vs(self):

        if not os.path.exists(self.output_file_path):
            os.mkdir(self.output_file_path)
        self.init_logger_path()

        cutover_msg = "Performing cutover for applications"
        LOG.debug(cutover_msg)
        print(cutover_msg)
        nsx_util = NSXUtil(self.nsxt_user, self.nsxt_passord, self.nsxt_ip, self.nsxt_port \
                           , self.controller_ip, self.user, self.password, self.controller_version)
        nsx_util.cutover_vs(self.cutover_vs)

        print("Total Warning: ", get_count('warning'))
        print("Total Errors: ", get_count('error'))
        LOG.info("Total Warning: {}".format(get_count('warning')))
        LOG.info("Total Errors: {}".format(get_count('error')))


if __name__ == "__main__":
    HELP_STR = """
    Usage:
    python nsxt_converter.py -n 192.168.100.101 -u admin -p password 
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, description=HELP_STR)

    parser.add_argument('-n', '--nsxt_ip',
                        help='Ip of NSXT')
    parser.add_argument('-u', '--nsxt_user',
                        help='NSX-T User name')
    parser.add_argument('-p', '--nsxt_passord',
                        help='NSX-T Password')
    parser.add_argument('-port', '--nsxt_port', default=443,
                        help='NSX-T Port')
    parser.add_argument('-o', '--output_file_path',
                        help='Folder path for output files to be created in',
                        )

    parser.add_argument('-c', '--controller_ip',
                        help='controller ip for auto upload')
    parser.add_argument('--controller_version',
                        help='Target Avi controller version')
    parser.add_argument('--user',
                        help='controller username for auto upload')
    parser.add_argument('--password',
                        help='controller password for auto upload. Input '
                             'prompt will appear if no value provided')

    # Added command line args to take skip type for ansible playbook
    parser.add_argument('--cutover',
                        help='comma separated names of virtualservices for cutover.\n'
                        )

    start = datetime.now()
    args = parser.parse_args()
    traffic_cutover = TrafficCutover(args)
    traffic_cutover.initiate_cutover_vs()
    end = datetime.now()
    print("The time of execution of above program is :",
          str(end - start))
