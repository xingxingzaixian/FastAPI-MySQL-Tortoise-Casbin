import os
import sys

from dotenv import load_dotenv

from core.config import settings

# 把 core 目录加入到环境变量，主要是 tortoise 的 router 配置必须是 module.class
sys.path.insert(1, os.path.join(settings.BASE_PATH, 'core'))

config_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(config_dir, 'config', '.env'))