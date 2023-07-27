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

GRAPH_URL = 'https://graph.microsoft.com/v1.0'


url = f"{GRAPH_URL}/groups/?$filter=startswith(displayname,'LGS.Vorstand')"
r = api.connection.get(url).json()
print(json.dumps(r,indent=4))
groud_id= r["value"][0]["id"]

file_path = "Sommer-LL-Sitzung 2023.xlsx"
url = f"{GRAPH_URL}/groups/{groud_id}/drive/root/children"
r = api.connection.get(url).json()
print(json.dumps(r,indent=4))

url = f"{GRAPH_URL}/groups/{groud_id}/drive/items/01EYOA6E22TO522HL6U5FZFEMRLLLCA3K5/content"
r = api.connection.get(url)
print(str(r))



