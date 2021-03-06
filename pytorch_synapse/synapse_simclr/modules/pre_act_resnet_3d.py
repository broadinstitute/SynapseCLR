#########################################################################################
# code is based on:                                                                     #
# https://github.com/kenshohara/3D-ResNets-PyTorch/blob/master/models/pre_act_resnet.py #
#########################################################################################

import torch

from .resnet_3d import conv3x3x3, conv1x1x1, get_inplanes, ResNet


class PreActivationBasicBlock(torch.nn.Module):
    expansion = 1

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super().__init__()

        self.bn1 = torch.nn.BatchNorm3d(inplanes)
        self.conv1 = conv3x3x3(inplanes, planes, stride)
        self.bn2 = torch.nn.BatchNorm3d(planes)
        self.conv2 = conv3x3x3(planes, planes)
        self.relu = torch.nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.bn1(x)
        out = self.relu(out)
        out = self.conv1(out)

        out = self.bn2(out)
        out = self.relu(out)
        out = self.conv2(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual

        return out


class PreActivationBottleneck(torch.nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super().__init__()

        self.bn1 = torch.nn.BatchNorm3d(inplanes)
        self.conv1 = conv1x1x1(inplanes, planes)
        self.bn2 = torch.nn.BatchNorm3d(planes)
        self.conv2 = conv3x3x3(planes, planes, stride)
        self.bn3 = torch.nn.BatchNorm3d(planes)
        self.conv3 = conv1x1x1(planes, planes * self.expansion)
        self.relu = torch.nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.bn1(x)
        out = self.relu(out)
        out = self.conv1(out)

        out = self.bn2(out)
        out = self.relu(out)
        out = self.conv2(out)

        out = self.bn3(out)
        out = self.relu(out)
        out = self.conv3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual

        return out


def generate_model(model_depth, **kwargs):
    assert model_depth in [10, 18, 34, 50, 101, 152, 200]

    if model_depth == 10:
        model = ResNet(PreActivationBasicBlock, [1, 1, 1, 1], get_inplanes(),
                       **kwargs)
    elif model_depth == 18:
        model = ResNet(PreActivationBasicBlock, [2, 2, 2, 2], get_inplanes(),
                       **kwargs)
    elif model_depth == 34:
        model = ResNet(PreActivationBasicBlock, [3, 4, 6, 3], get_inplanes(),
                       **kwargs)
    elif model_depth == 50:
        model = ResNet(PreActivationBottleneck, [3, 4, 6, 3], get_inplanes(),
                       **kwargs)
    elif model_depth == 101:
        model = ResNet(PreActivationBottleneck, [3, 4, 23, 3], get_inplanes(),
                       **kwargs)
    elif model_depth == 152:
        model = ResNet(PreActivationBottleneck, [3, 8, 36, 3], get_inplanes(),
                       **kwargs)
    elif model_depth == 200:
        model = ResNet(PreActivationBottleneck, [3, 24, 36, 3], get_inplanes(),
                       **kwargs)

    return model