from easydict import EasyDict
from datetime import datetime
import requests
import os
import yaml
import torch
import logging
import torch.backends.cudnn as cudnn
import lightning as L


def get_configs():
    config_path = "configs/"

    # 기본 설정 파일
    with open(os.path.join(config_path, "base.yaml"), "r") as file:
        base_config = yaml.safe_load(file)
        args = EasyDict(base_config)

    # 현재 실험중인 hyperparameter 설정 파일
    with open(os.path.join(config_path, "config.yaml"), "r") as file:
        config = yaml.safe_load(file)
        args.update(config)

    # 모델 설정 파일
    with open(os.path.join(config_path, f"models/{args.model}.yaml"), "r") as file:
        model_config = yaml.safe_load(file)
        args.update(model_config)

    return args


def init_configs(args):
    args.current_time = datetime.now().strftime("%Y%m%d")

    # Set Device
    args.device = get_device(args.GPU_NUM)

    return args


def get_device(GPU_NUM: str) -> torch.device:
    if torch.cuda.device_count() == 1:
        output = torch.device(f"cuda:{GPU_NUM}")
    elif torch.cuda.device_count() > 1:
        output = torch.device(f"cuda")
    else:
        output = torch.device("cpu")

    print(f"{output} is checked")
    return output


def init_settings(args):
    cudnn.benchmark = False
    cudnn.deterministic = True

    L.seed_everything(args.SEED)
