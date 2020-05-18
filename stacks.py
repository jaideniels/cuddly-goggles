import ptvsd

from app import app, db

ptvsd.enable_attach(address=('0.0.0.0', 5678))
