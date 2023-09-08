import pkg_resources
from freevpn import network, neural
import re


def get_password(region: str, use_cpu: bool):
    region_page = network.get_region_page(region=region)
    image_path = re.search(r'src="(img/password\.php\?\w+)"', region_page).group(1)
    image_bytes = network.get_password_image_bytes(image_path, region)
    return neural.extract_password_from_image(image_bytes, use_cpu)