from __future__ import print_function

import logging
import pathlib
import json
import pandas as pd
from decouple import config

from pfapis.o365 import O365

logging.basicConfig(level=logging.INFO)
# variables
path = str(pathlib.Path(__file__).parent.resolve())
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")


api = O365()
api.graph_connection(cliend_id=CLIENT_ID, client_secret=CLIENT_SECRET)

text="Hallo"
Subject="Test"
to = ['umberto.albano@nds.pfadfinden.de']
sender="admin@nds.pfadfinden.de"

api.write_email(message=text,subject=Subject,to=to,cc=[],sender_address=sender)
# Sending an E-Mail from a different address:
#api.write_email(message=text,subject=Subject,to=to,cc=[],sender_address=sender) 