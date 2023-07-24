# PfadiApis (pfapis)

In this repo you can find several api to system, they are use for the BdP LV Nds.
This Lib is experimental and for other scouts, they are want to interact with these systems.

These Api ar exists:

## bdp_mv

This API is made for interact with member registration of our club. 
The System is called Nami. For authentication you need your MV Username and Passwort. 

The Nami could be import this way:

```
from pfapis.bdp_mv import Nami
```

## o365

This API is made for interact with O365. This file is a wrapper for the MS Graph Api.
For authentication you need a grap secret key. For generation one key see this manual: https://docs.jamcracker.com/Orion/CSB%20SP/topic/Graph%20API%20Client%20ID%20and%20Graph%20API%20Secret%20Key.html

With this Api you can write E-Mail, edit oder add Users.
The Api can import this way:

```
from pfapis.o365 import O365
```

## confluence

Confluence is a wiki based software of atlassian. 
With this api you can edit pages or get information from them. 
The data are stored in pd.Dataframe. 

For example you can upload a pd.Dataframe like this way:

```
from pfapis.confuence import Confluence
import pandas as pd

data = pd.DataFrame()

page_id = 320406536
parent_id = 295635982
title = 'Page Title'
#This note is printed above
note='Diese Seite wird automatisch aus der MV generiert. Die Daten nicht händisch anpassen!' 
header=''

#login
conf = Confluence(url='https://nds.meinbdp.de:443', username=conf_user, password=conf_password)
conf.uplaod_data_to_page(page_id=page_id, parent_id=parent_id, title=title, upload_file=False, content=datta,
                         header=header,
                         note=note)


```

