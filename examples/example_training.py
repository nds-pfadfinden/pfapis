from pfapis.bdp_mv import Nami
import logging
from decouple import config
import pathlib

mem_id = 52870

logging.basicConfig(level=logging.INFO)
# variables
path = str(pathlib.Path(__file__).parent.resolve())
mv_username = config("MV_USER")
mv_password = config("MV_PASSWORD")


config = []
mv = Nami(config)
rc = mv.auth(mv_username, mv_password)

print(mv.checkForTrainingname(memberId=mem_id,trainingName="Fortbildung Prävention/Intervention"))
