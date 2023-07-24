from __future__ import print_function

import logging
import pathlib

import pandas as pd
from decouple import config

from pfapis.bdp_mv import Nami

logging.basicConfig(level=logging.INFO)
# variables
path = str(pathlib.Path(__file__).parent.resolve())
mv_username = config("MV_USER")
mv_password = config("MV_PASSWORD")


config = []
mv = Nami(config)
rc = mv.auth(mv_username, mv_password)

umberto = mv.user("Umberto","Albano")
print(umberto)
