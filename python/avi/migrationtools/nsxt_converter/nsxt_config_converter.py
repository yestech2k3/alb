import sys
from avi.migrationtools.nsxt_converter import nsxt_client as nsx_client_util
from avi.migrationtools.nsxt_converter import monitor_converter
from vmware.vapi.bindings.struct import PrettyPrinter
from com.vmware.vapi.std.errors_client import NotFound
from com.vmware.nsx.loadbalancer_client import Pools
import com.vmware.nsx_policy.infra_client as infra_client
import com.vmware.nsx_policy.model_client as model_client
import random
from com.vmware.vapi.std.errors_client import Error
from avi.migrationtools.avi_rest_lib import upload_config_to_controller

from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil
from avi.migrationtools.nsxt_converter.monitor_converter \
    import MonitorConfigConv
from avi.migrationtools.nsxt_converter.nsxt_util import NSXUtil
import os
import json
import avi.migrationtools.nsxt_converter.converter_constants as conv_const
from avi.migrationtools.nsxt_converter.pools_converter import PoolConfigConv
from avi.migrationtools.nsxt_converter.profile_converter \
    import ProfileConfigConv
from avi.migrationtools.nsxt_converter.ssl_profile_converter \
    import SslProfileConfigConv

conv_utils = NsxtConvUtil()


def convert(nsx_ip, nsx_un, nsx_pw, nsx_port, output_dir, cloud_name, prefix
            ):
    # load the yaml file attribute in nsxt_attributes.
    nsxt_attributes = conv_const.init("11")

    nsx_util = NSXUtil(nsx_un, nsx_pw, nsx_ip, nsx_port)
    nsx_lb_config = nsx_util.get_nsx_config()
    input_path = output_dir + os.path.sep + nsx_ip + os.path.sep + "input"
    if not os.path.exists(input_path):
        os.makedirs(input_path)
    input_config = input_path + os.path.sep + "config.json"
    with open(input_config, "w", encoding='utf-8') as text_file:
        json.dump(nsx_lb_config, text_file, indent=4)

    alb_config = dict()  # Result Config

    monitor_converter = MonitorConfigConv(nsxt_attributes)
    monitor_converter.convert(alb_config, nsx_lb_config, prefix)

    pool_converter = PoolConfigConv(nsxt_attributes)
    pool_converter.convert(alb_config, nsx_lb_config, cloud_name, prefix)

    profile_converter = ProfileConfigConv(nsxt_attributes)
    profile_converter.convert(alb_config, nsx_lb_config, prefix)

    ssl_profile_converter = SslProfileConfigConv(nsxt_attributes)
    ssl_profile_converter.convert(alb_config, nsx_lb_config, prefix)

    output_path = output_dir + os.path.sep + nsx_ip + os.path.sep + "output"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_config = output_path + os.path.sep + "avi_config.json"
    with open(output_config, "w", encoding='utf-8') as text_file:
        json.dump(alb_config, text_file, indent=4)

    # Add nsxt converter status report in xslx report
    conv_utils.add_complete_conv_status(
        output_dir, alb_config, "nsxt-report", False)

    pp = PrettyPrinter()
    pp.pprint(alb_config)

    return alb_config

