# Copyright 2021 VMware, Inc.
# SPDX-License-Identifier: Apache License 2.0

import yaml
import os

def init(version):
    """
    This function defines that to initialize constant from yaml file
    :return: None
    """
    global nsxt_command_status
    with open(os.path.dirname(__file__) + "/command_status.yaml") as stream:
        nsxt_command_status = yaml.safe_load(stream)
    if version == '10':
        return nsxt_command_status['VERSION_10']
    else:
        return nsxt_command_status['VERSION_11']


if __name__ == "__main__":
    print(init(11))
