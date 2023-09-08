import argparse
import os

from freevpn import cmd


if __name__ == "__main__":
    if os.geteuid() != 0:
        raise RuntimeError("sudo is required")

    parser = argparse.ArgumentParser()
    parser.add_argument("--login", default="freeopenvpn", help="vpn login")
    parser.add_argument(
        "--password",
        default=None,
        help="vpn password. If None, it will be obtained from the website",
    )
    parser.add_argument("--daemon", action="store_true")
    parser.add_argument(
        "--region",
        default="Netherlands",
        choices=["Netherlands", "USA", "UK", "Germany"],
    )
    parser.add_argument("--cpu", action="store_true")
    args = parser.parse_args()

    cmd.connect_to_vpn(
        cmd.get_credentials_file(args.login, args.password, args.region, args.cpu),
        cmd.get_ovpn_tcp_config(args.region),
        args.daemon,
    )
