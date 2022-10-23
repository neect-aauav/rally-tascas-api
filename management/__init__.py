import os

from .logger import Logger
from neectrally.settings import BASE_DIR

logger = Logger(os.path.join(BASE_DIR, 'static/logs/'))