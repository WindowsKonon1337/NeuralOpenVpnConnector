import argparse
import os
import sys

sys.path.insert(1, './utils')

import requests
import torch
from bs4 import BeautifulSoup
from CNN import ConvNet
from PIL import Image, ImageOps
from torchvision import transforms


def default_connection(login: str, password: str, vpnpath: str):
    with open('./utils/auth.cfg', mode='w') as file:
        file.write(login + '\n')
        file.write(password + '\n')

    os.system(
        f'sudo openvpn --config {vpnpath} --auth-user-pass ./utils/auth.cfg'
    )

if __name__ == '__main__':

    MODEL_BINARY_PATH = './utils/cnn.pth'
    REGION = ''

    parser = argparse.ArgumentParser()

    parser.add_argument('--vpnpath', type=str, help='absolute path to .ovpn file')
    parser.add_argument('--login', type=str, default='freeopenvpn', help='vpn login')
    parser.add_argument('--password', type=str, default=None, help='vpn password. If None, it will be obtained from the website')

    args = parser.parse_args()

    if args.vpnpath is None:
        raise Exception(f'Please write the path to .ovpn file')
    
    if args.password is not None:
        default_connection(args.login, args.password, args.vpnpath)
        exit(0)
    
    REGION = args.vpnpath.split('/')[-1].split('_')[0]

    response = requests.get(f'https://www.freeopenvpn.org/premium.php?cntid={REGION}&lang=en')

    soup = BeautifulSoup(response.text, 'html.parser')

    script_block = soup.find('div', attrs={'style' : 'margin: 21px 0 22px;'}).find('script').text
    script_block = script_block[script_block.find('<img src=\"img'):]

    url = script_block.split('\"')[1]

    os.system(f'./utils/downloadPassword.sh {url} {REGION}')

    img = ImageOps.grayscale(Image.open('./utils/password.png').resize((162, 21)))

    transform = transforms.Compose([
        transforms.ToTensor()
    ])

    numbers = []

    for i in range(0, 163 - 18, 18):
        numbers.append(
            img.crop((i, 0, 18 + i, 21)).resize((28, 28))
        )

    model = ConvNet()
    model.load_state_dict(torch.load('./utils/cnn.pth'))
    result = ""
    for img in numbers:
        result += str(torch.argmax(model(transform(img)[None,:,:,:])).item())

    default_connection(args.login, result, args.vpnpath)