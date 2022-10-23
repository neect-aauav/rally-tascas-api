import os

from .logger import Logger
from neectrally.settings import BASE_DIR

# initialize Logger that will be used throughout the project
logger = Logger(os.path.join(BASE_DIR, 'static/logs/'))