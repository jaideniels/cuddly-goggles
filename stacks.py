import os
from app import app, db
import ptvsd

ptvsd.enable_attach(address=('0.0.0.0', 5678))
