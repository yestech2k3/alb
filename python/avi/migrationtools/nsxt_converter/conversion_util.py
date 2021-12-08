# Copyright 2021 VMware, Inc.
# SPDX-License-Identifier: Apache License 2.0

import logging
import os
from functools import reduce

import pandas
import avi.migrationtools.f5_converter.converter_constants as conv_const

from xlsxwriter import Workbook
from openpyxl import load_workbook

from avi.migrationtools.avi_migration_utils import MigrationUtil
from avi.migrationtools.f5_converter.conversion_util import F5Util

LOG = logging.getLogger(__name__)
csv_writer_dict_list = []

# Added variable for checking progress and get overall object.
ppcount = 0
ptotal_count = 0
global fully_migrated
fully_migrated = 0
used_pool_groups = {}
used_pool = {}

class NsxtConvUtil(MigrationUtil):

    STATIC_PORT_MAP = {
        "http" : conv_const.HTTP_PORT,
        "https" : conv_const.HTTPS_PORT,
        "ftp" : conv_const.FTP_PORT,
        "smtp" : conv_const.SMTP_PORT,
        "snmp" : conv_const.SNMP_PORT,
        "telnet" : conv_const.TELNET_PORT,
        "snmp-trap" : conv_const.SNMP_TRAP_PORT,
        "ssh" : conv_const.SSH_PORT,
        "xfer" : conv_const.XFER_PORT,
        "pcsync-https" : conv_const.PCSYNC_HTTPS_PORT,
        "macromedia-fcs" : conv_const.MACROMEDIA_FCS_PORT,
        "imap" : conv_const.IMAP_PORT,
        "pop3" : conv_const.POP3_PORT,
        "any" : None
    }

    def add_conv_status(self, nsxt_type, nsxt_sub_type, nsxt_id, conv_status,
                        avi_object=None, need_review=None):
        """
        Adds as status row in conversion status csv
        :param nsxt_type: Object type
        :param nsxt_sub_type: Object sub type
        :param nsxt_id: Name oconv_f object
        :param conv_status: dict of conversion status
        :param avi_object: Converted objectconverted avi object
        """
        global csv_writer_dict_list
        # Added space if nsxt_sub_type None for pivot table
        row = {
            'NsxT type': nsxt_type,
            'NsxT SubType': nsxt_sub_type if nsxt_sub_type else ' ',
            'NsxT ID': nsxt_id,
            'Status': conv_status.get('status', ''),
            'Skipped settings': str(conv_status.get('skipped', '')),
            'Skipped for defaults': str(conv_status.get('default_skip', '')),
            'Indirect mapping': str(conv_status.get('indirect', '')),
            'Not Applicable': str(conv_status.get('na_list', '')),
            'User Ignored': str(conv_status.get('user_ignore', '')),
            'Avi Object': str(avi_object),
            'Needs Review': need_review
        }
        csv_writer_dict_list.append(row)

    def add_status_row(self, nsxt_type, nsxt_sub_type, nsxt_id, status, avi_obj=None):
        """
        Adds as status row in conversion status csv
        :param nsxt_type: Object type
        :param nsxt_sub_type: Object sub type
        :param nsxt_id: Name of object
        :param status: conversion status
        :param avi_obj: Converted avi object
        """
        global csv_writer_dict_list
        # Added space if nsxt_sub_type None for pivot table
        row = {
            'NsxT type': nsxt_type,
            'NsxT SubType': nsxt_sub_type if nsxt_sub_type else ' ',
            'NsxT ID': nsxt_id,
            'Status': status
        }
        if avi_obj:
            row.update({
                'Avi Object': str(avi_obj)
            })
        csv_writer_dict_list.append(row)

    def add_complete_conv_status(self, output_dir, avi_config, report_name,
                                 vs_level_status):

        global csv_writer_dict_list
        global ptotal_count
        for status in conv_const.STATUS_LIST:
            status_list = [row for row in csv_writer_dict_list if
                           row['Status'] == status]
            print('%s: %s' % (status, len(status_list)))
        print("Writing Excel Sheet For Converted Configuration...")
        ptotal_count = ptotal_count + len(csv_writer_dict_list)
        if vs_level_status:
            self.vs_per_skipped_setting_for_references(avi_config)
            self.correct_vs_ref(avi_config)
        else:
            # Update the complexity level of VS as Basic or Advanced
            self.vs_complexity_level()
        self.write_status_report_and_pivot_table_in_xlsx(
            output_dir, report_name, vs_level_status)

    def get_port_by_protocol(self, protocol):
        """
        Instead of default ports for protocols nsxt config has protocol in
        destination value for Avi object need to conver it to port number
        :param protocol: protocol name
        :return: integer value for protocol
        """

        return self.STATIC_PORT_MAP.get(protocol, None)



    def update_pool_for_service_port(self, pool_list, pool_name, hm_list,
                                     sys_hm_list):
        rem_hm = []
        pool = [obj for obj in pool_list if obj['name'] == pool_name]
        if pool:
            pool[0]['use_service_port'] = True
            # Checking monitor ports if use_service_port is true
            if pool[0].get('health_monitor_refs'):
                for hm in pool[0]['health_monitor_refs']:
                    hm_name = self.get_name(hm)
                    hm_ob = [ob for ob in (hm_list + sys_hm_list) if
                             ob['name'] == hm_name]
                    if hm_ob and (not hm_ob[0].get('monitor_port')):
                        rem_hm.append(hm)
                        LOG.debug("Removing monitor reference of %s from pool"
                                  " %s as 'use_service_port' is true but "
                                  "monitor has no port", hm_name,
                                  pool_name)
                if rem_hm:
                    pool[0]['health_monitor_refs'] = [
                        h_monitor for h_monitor in pool[0]
                        ['health_monitor_refs'] if h_monitor not in rem_hm]

                    rem_hm = [self.get_name(hmonitor) for hmonitor in rem_hm]
                    csv_row = [cl for cl in csv_writer_dict_list if cl[
                               'NsxT type'] == 'pool' and self.get_tenant_ref(
                        cl['NsxT ID'])[1] == pool_name]
                    if csv_row:
                        if csv_row[0]['Skipped settings'] in ('[]', ''):
                            csv_row[0]['Skipped settings'] = str([{
                                                            'monitor': rem_hm}])
                        else:
                            init_val = eval(csv_row[0]['Skipped settings'])
                            if not isinstance(init_val, list):
                                init_val = [init_val]
                            mon_val = [
                                val['monitor'].extend(rem_hm) for val in
                                init_val if isinstance(val, dict) and
                                'monitor' in val]
                            if bool(mon_val):
                                csv_row[0]['Skipped settings'] = str(init_val)
                            else:
                                init_val.append({'monitor': rem_hm})
                                csv_row[0]['Skipped settings'] = str(init_val)
                        csv_row[0]['Status'] = conv_const.STATUS_PARTIAL
                        csv_row[0]['Avi Object'] = str({'pools': pool})

    def write_status_report_and_pivot_table_in_xlsx(
            self, output_dir, report_name, vs_level_status):
        """
        This function defines that add status sheet and pivot table sheet in
        xlsx format
        :param output_dir: Path of output directory
        :param report_name: filename to write report
        :param vs_level_status: Flag to include VS wise detailed status or not
        :return: None
        """
        global ppcount
        global ptotal_count
        # List of fieldnames for headers
        if vs_level_status:
            fieldnames = ['NsxT type', 'NsxT SubType', 'NsxT ID', 'Status',
                          'Skipped settings', 'Indirect mapping',
                          'Not Applicable', 'User Ignored',
                          'Skipped for defaults', 'Complexity Level',
                          'VS Reference', 'Overall skipped settings',
                          'Avi Object', 'Needs Review']
        else:
            fieldnames = ['NsxT type', 'NsxT SubType', 'NsxT ID', 'Status',
                          'Skipped settings', 'Indirect mapping',
                          'Not Applicable',
                          'User Ignored', 'Skipped for defaults',
                          'Complexity Level', 'Avi Object', 'Needs Review']

        # xlsx workbook
        report_path = output_dir + os.path.sep + "%s-ConversionStatus.xlsx" % \
                                                 report_name
        status_wb = Workbook(report_path)
        # xlsx worksheet
        status_ws = status_wb.add_worksheet("Status Sheet")
        # Lock the first row of xls report.
        status_ws.freeze_panes(1, 0)
        first_row = 0
        for header in fieldnames:
            col = fieldnames.index(header)
            status_ws.write(first_row, col, header)
        row = 1
        for row_data in csv_writer_dict_list:
            ppcount += 1
            for _key, _value in row_data.items():
                col = fieldnames.index(_key)
                status_ws.write(row, col, _value)
            # Added call for progress function.
            msg = "excel sheet conversion started..."
            self.print_progress_bar(ppcount, ptotal_count, msg,
                                    prefix='Progress', suffix='')
            row += 1
        status_wb.close()
        # create dataframe for row list
        df = pandas.DataFrame(csv_writer_dict_list, columns=fieldnames)
        # create pivot table using pandas
        pivot_table = \
            pandas.pivot_table(df, index=["Status", "NsxT type", "NsxT SubType"],
                               values=[], aggfunc=[len], fill_value=0)
        # create dataframe for pivot table using pandas
        pivot_df = pandas.DataFrame(pivot_table)
        master_book = \
            load_workbook(report_path)
        master_writer = pandas.ExcelWriter(report_path, engine='openpyxl')
        master_writer.book = master_book
        # Add pivot table in Pivot sheet
        pivot_df.to_excel(master_writer, 'Pivot Sheet')
        master_writer.save()

    def vs_complexity_level(self):
        """
        This method calculate the complexity of vs.
        :return:
        """
        # Get the VS object list which is having status successful and partial.
        vs_csv_objects = [row for row in csv_writer_dict_list
                          if row['Status'] in [conv_const.STATUS_PARTIAL,
                                               conv_const.STATUS_SUCCESSFUL]
                          and row['NsxT type'] == 'virtual']
        for vs_csv_object in vs_csv_objects:
            virtual_service = self.format_string_to_json(
                vs_csv_object['Avi Object'])
            # Update the complexity level of VS as Basic or Advanced
            self.update_vs_complexity_level(vs_csv_object, virtual_service)

    def vs_per_skipped_setting_for_references(self, avi_config):
        """
        This functions defines that Add the skipped setting per VS CSV row
        :param avi_config: this method use avi_config for checking vs skipped
        :return: None
        """

        # Get the count of vs fully migrated
        global fully_migrated
        global ptotal_count
        global ppcount
        fully_migrated = 0
        # Get the VS object list which is having status successful and partial.
        vs_csv_objects = [row for row in csv_writer_dict_list
                          if row['Status'] in [conv_const.STATUS_PARTIAL,
                                               conv_const.STATUS_SUCCESSFUL]
                          and row['NsxT type'] == 'virtual']
        # Get the list of csv rows which has profile as NsxT type
        profile_csv_list = self.get_csv_object_list(
            csv_writer_dict_list, ['profile'])
        ptotal_count = ptotal_count + len(vs_csv_objects)
        for vs_csv_object in vs_csv_objects:
            ppcount += 1
            skipped_setting = {}
            virtual_service = self.format_string_to_json(
                vs_csv_object['Avi Object'])
            # Update the complexity level of VS as Basic or Advanced
            self.update_vs_complexity_level(vs_csv_object, virtual_service)
            vs_ref = virtual_service['name']
            repls = ('[', ''), (']', '')
            # Get list of skipped setting attributes
            skipped_setting_csv = reduce(lambda a, kv: a.replace(*kv), repls,
                                         vs_csv_object['Skipped settings'])
            if skipped_setting_csv:
                skipped_setting['virtual_service'] = [skipped_setting_csv]
            # Get the skipped list for ssl key and cert
            if 'ssl_key_and_certificate_refs' in virtual_service:
                for ssl_key_and_certificate_ref in \
                        virtual_service['ssl_key_and_certificate_refs']:
                    ssl_key_cert = self.get_name(ssl_key_and_certificate_ref)
                    ssl_kc_skip = self.get_csv_skipped_list(
                        profile_csv_list, ssl_key_cert, vs_ref,
                        field_key='ssl_cert_key')
                    if ssl_kc_skip:
                        skipped_setting['ssl cert key'] = {}
                        skipped_setting['ssl cert key']['name'] = ssl_key_cert
                        skipped_setting['ssl cert key'][
                            'skipped_list'] = ssl_kc_skip

            # Get the skipped list for ssl profile name.
            # Changed ssl profile name to ssl profile ref.
            if 'ssl_profile_ref' in virtual_service:
                name, skipped = self.get_ssl_profile_skipped(
                    profile_csv_list, virtual_service['ssl_profile_ref'],
                    vs_ref)
                if skipped:
                    skipped_setting['ssl profile'] = {}
                    skipped_setting['ssl profile']['name'] = name
                    skipped_setting['ssl profile']['skipped_list'] = skipped
            # Get the skipped list for pool group.
            if 'pool_group_ref' in virtual_service:
                pool_group_name = self.get_name(
                    virtual_service['pool_group_ref'])
                csv_pool_rows = self.get_csv_object_list(csv_writer_dict_list,
                                                         ['pool'])
                pool_group_skipped_settings = self.get_pool_skipped_list(
                    avi_config, pool_group_name, csv_pool_rows,
                    csv_writer_dict_list, vs_ref, profile_csv_list)
                if pool_group_skipped_settings:
                    skipped_setting['Pool Group'] = pool_group_skipped_settings
            # Get the skipped list for pool.
            if 'pool_ref' in virtual_service:
                pool_skipped_settings = {'pools': []}
                pool_name = self.get_name(virtual_service['pool_ref'])
                csv_pool_rows = self.get_csv_object_list(csv_writer_dict_list,
                                                         ['pool'])
                self.get_skipped_pool(
                    avi_config, pool_name, csv_pool_rows, csv_writer_dict_list,
                    vs_ref, profile_csv_list, pool_skipped_settings)
                if pool_skipped_settings['pools']:
                    skipped_setting['Pool'] = pool_skipped_settings
            # Get the skipepd list for http policy.
            if 'http_policies' in virtual_service:
                policy_csv_list = self.get_csv_object_list(
                    csv_writer_dict_list, ['policy', 'profile'])
                for http_ref in virtual_service['http_policies']:
                    policy_set_name, skipped_list = self.get_policy_set_skipped(
                        policy_csv_list, http_ref['http_policy_set_ref'],
                        vs_ref)
                    if skipped_list:
                        skipped_setting['Httppolicy'] = {}
                        skipped_setting['Httppolicy']['name'] = policy_set_name
                        skipped_setting['Httppolicy'][
                            'skipped_list'] = skipped_list
                    # Get the http policy name
                    pool_csv_rows = \
                        self.get_csv_object_list(csv_writer_dict_list, ['pool'])
                    for each_http_policy in avi_config['HTTPPolicySet']:
                        if each_http_policy['name'] == policy_set_name and 'http_request_policy' in each_http_policy:
                            for http_req in each_http_policy[
                              'http_request_policy']['rules']:
                                if http_req.get('switching_action', {}):
                                    self.get_skip_pools_policy(
                                        policy_set_name, http_req,
                                        avi_config, pool_csv_rows, vs_ref,
                                        profile_csv_list, skipped_setting)

            # # Get the skipped list for application_profile_ref.
            if 'application_profile_ref' in virtual_service and 'admin:System' \
                    not in virtual_service['application_profile_ref']:
                name, skipped = self.get_application_profile_skipped(
                    profile_csv_list,
                    virtual_service['application_profile_ref'],
                    vs_ref)
                if skipped:
                    skipped_setting['Application profile'] = {}
                    skipped_setting['Application profile'][
                        'name'] = name
                    skipped_setting['Application profile'][
                        'skipped_list'] = skipped
            # # Get the skipped list for network profile ref.
            if 'network_profile_ref' in virtual_service and 'admin:System' \
                    not in virtual_service['network_profile_ref']:
                name, skipped = self.get_network_profile_skipped(
                    profile_csv_list, virtual_service['network_profile_ref'],
                    vs_ref)
                if skipped:
                    skipped_setting['Network profile'] = {}
                    skipped_setting['Network profile'][
                        'name'] = name
                    skipped_setting['Network profile'][
                        'skipped_list'] = skipped
            # Update overall skipped setting of VS csv row
            if skipped_setting:
                vs_csv_object.update(
                    {'Overall skipped settings': str(skipped_setting)})
            else:
                vs_csv_object.update(
                    {'Overall skipped settings': "FULLY MIGRATION"})
                fully_migrated += 1
            # Added call for progress function.
            msg = "excel sheet conversion started..."
            self.print_progress_bar(ppcount, ptotal_count, msg,
                                    prefix='Progress', suffix='')
        csv_objects = [row for row in csv_writer_dict_list
                       if row['Status'] in [
                           conv_const.STATUS_PARTIAL,
                           conv_const.STATUS_SUCCESSFUL]
                       and row['NsxT type'] != 'virtual']

        # Update the vs reference not in used if objects are not attached to
        # VS directly or indirectly
        for row in csv_objects:
            if 'VS Reference' not in row or row['VS Reference'] == '':
                row['VS Reference'] = conv_const.STATUS_NOT_IN_USE


    def correct_vs_ref(self, avi_config):
        """
        This method corrects the reference of VS to different objects
        :param avi_config: avi configuration dict
        :return:
        """
        global csv_writer_dict_list
        avi_graph = self.make_graph(avi_config)
        csv_dict_sub = [row for row in csv_writer_dict_list if row[
                        'NsxT type'] != 'virtual' and row['Status'] in
                        (conv_const.STATUS_PARTIAL,
                         conv_const.STATUS_SUCCESSFUL)]
        for dict_row in csv_dict_sub:
            obj = dict_row['Avi Object']
            vs = []
            if obj.startswith('{'):
                obj = eval(obj)
                for key in obj:
                    for objs in obj[key]:
                        self.add_vs_ref(objs, avi_graph, vs)
            elif obj.startswith('['):
                obj = eval(obj)
                for objs in obj:
                    for key in objs:
                        objval = objs[key]
                        self.add_vs_ref(objval, avi_graph, vs)
            if vs:
                dict_row['VS Reference'] = str(list(set(vs)))
            else:
                dict_row['VS Reference'] = conv_const.STATUS_NOT_IN_USE

