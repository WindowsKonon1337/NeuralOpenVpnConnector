import os
import tempfile

import pkg_resources

from freevpn import network
from freevpn.password import get_password

OVPN_TCP_CONFIG_PATH = pkg_resources.resource_filename(__name__, "meta/config.ovpn")
CREDENTIALS_PATH = pkg_resources.resource_filename(__name__, "meta/credentials")


def connect_to_vpn(credentials, config, daemon: bool):
    daemon_flag = '--daemon' if daemon else ''
    os.system(
        f'openvpn --config {config} --auth-user-pass {credentials}'
    )

def get_ovpn_tcp_config(region: str):
    with open(OVPN_TCP_CONFIG_PATH, 'w') as config:
        ovpn_tcp_config = network.get_ovpn_tcp_config(region)
        config.write(ovpn_tcp_config)
    return OVPN_TCP_CONFIG_PATH
    
def get_credentials_file(login: str, password: str | None, region: str, use_cpu: bool):
    with open(CREDENTIALS_PATH, 'w') as credentials:
        password = password or get_password(region, use_cpu)
        credentials.write(f'{login}\n{password}')
    return CREDENTIALS_PATH
