import io
import pkg_resources
import torch
import torch.nn as nn
import torch.nn.functional as F

from PIL import Image, ImageOps
from torchvision import transforms

WEIGHTS_PATH = pkg_resources.resource_filename(__name__, "meta/cnn.pth")


class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.conv3 = nn.Conv2d(64, 128, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(15488, 128)
        self.fc2 = nn.Linear(128, 10)
        self.batchnorm1 = nn.BatchNorm2d(32)
        self.batchnorm2 = nn.BatchNorm2d(64)
        self.batchnorm3 = nn.BatchNorm2d(128)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.batchnorm1(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = self.batchnorm2(x)
        x = self.conv3(x)
        x = F.relu(x)
        x = self.batchnorm3(x)
        x = F.max_pool2d(x, 2)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


def extract_password_from_image(image_bytes, use_cpu: bool):
    img = Image.open(io.BytesIO(image_bytes))
    img = ImageOps.grayscale(img.resize((162, 21)))

    transform = transforms.Compose([transforms.ToTensor()])

    numbers = []

    for i in range(0, 163 - 18, 18):
        numbers.append(img.crop((i, 0, 18 + i, 21)).resize((28, 28)))

    model = ConvNet()
    map_location = torch.device("cpu") if use_cpu else None
    model.load_state_dict(torch.load(WEIGHTS_PATH, map_location=map_location))
    result = ""
    for img in numbers:
        result += str(torch.argmax(model(transform(img)[None, :, :, :])).item())

    return result
