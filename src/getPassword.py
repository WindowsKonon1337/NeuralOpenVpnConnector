from bs4 import BeautifulSoup
import os
import requests
from PIL import Image, ImageOps
import torch
from torchvision import transforms
from CNN import ConvNet

if __name__ == '__main__':

    req = requests.get('https://www.freeopenvpn.org/premium.php?cntid=Netherlands&lang=en')

    soup = BeautifulSoup(req.text, 'html.parser')

    script_block = soup.find('div', attrs={'style' : 'margin: 21px 0 22px;'}).find('script').text
    script_block = script_block[script_block.find('<img src=\"img'):]

    url = script_block.split('\"')[1]

    os.system(f'./openvpnConnect/downloadPassword.sh {url}')

    img = ImageOps.grayscale(Image.open('./openvpnConnect/password.png').resize((162, 21)))

    transform = transforms.Compose([
        transforms.ToTensor()
    ])

    numbers = []

    for i in range(0, 163 - 18, 18):
        numbers.append(
            img.crop((i, 0, 18 + i, 21)).resize((28, 28))
        )

    model = ConvNet()
    model.load_state_dict(torch.load('./openvpnConnect/cnn.pth')) # Можно асинхронно делать request, чтобы в самом начале скрипта загружать веса
    result = ""
    for img in numbers:
        result += str(torch.argmax(model(transform(img)[None,:,:,:])).item())

    print(result)