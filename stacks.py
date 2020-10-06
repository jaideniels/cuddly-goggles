import debugpy

from app import app, db

debugpy.listen(5678)
