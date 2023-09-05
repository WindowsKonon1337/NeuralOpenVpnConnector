import argparse
import io
import os
import re
import sys

sys.path.insert(1, './neural')

import torch
from neural.CNN import ConvNet
from PIL import Image, ImageOps
from torchvision import transforms
import network


def default_connection(login: str, password: str, vpnpath: str, background_mode):
    with open('./auth.cfg', mode='w') as file:
        file.write(login + '\n')
        file.write(password + '\n')
    background_key = '' if background_mode else '-b'
    os.system(
        f'sudo {background_key} openvpn --config {vpnpath} --auth-user-pass ./auth.cfg'
    )

if __name__ == '__main__':

    MODEL_BINARY_PATH = './neural/cnn.pth'
    region = ''
    background_mode = True

    parser = argparse.ArgumentParser()

    parser.add_argument('--login', type=str, default='freeopenvpn', help='vpn login')
    parser.add_argument('--password', type=str, default=None, help='vpn password. If None, it will be obtained from the website')
    parser.add_argument('--background', type=str, default='n', help='If the flag is set to any char except n, then the program will be run as a daemon')
    parser.add_argument('--region', type=str, default='Netherlands', help='set one of the available region. region list:\n\
                        Netherlands\n\
                        USA\n\
                        UK\n\
                        Germany')

    args = parser.parse_args()

    if args.region is None:
        raise Exception(f'Please write the available region')
    
    region = args.region
    
    network.get_ovpn_tcp_config(region)

    vpnpath = f'./{region}_freeopenvpn_tcp.ovpn'

    background_mode = True if args.background == 'n' else False
    
    if args.password is not None:
        default_connection(args.login, args.password,vpnpath, background_mode)
        exit(0)

    region_page = network.get_region_page(region='Netherlands')
    image_path = re.search(r'src="(img/password\.php\?\w+)"', region_page).group(1)
    image_bytes = network.get_password_image_bytes(image_path, region)

    img = Image.open(io.BytesIO(image_bytes))
    img = ImageOps.grayscale(img.resize((162, 21)))

    transform = transforms.Compose([
        transforms.ToTensor()
    ])

    numbers = []

    for i in range(0, 163 - 18, 18):
        numbers.append(
            img.crop((i, 0, 18 + i, 21)).resize((28, 28))
        )

    model = ConvNet()
    model.load_state_dict(torch.load('./neural/cnn.pth'))
    result = ""
    for img in numbers:
        result += str(torch.argmax(model(transform(img)[None,:,:,:])).item())

    default_connection(args.login, result, vpnpath, background_mode)