import logging

from api.bdp_mv import Nami
from api.utils import Utility


class UserInfo():
    @staticmethod
    def compareUserDataToInput(user, vorname, nachname):
        returnVar = []
        logging.info(user)
        if len(user) == 1:
            return user[0]["entries_id"]
        for i in user:
            if i["entries_vorname"] == vorname and i["entries_nachname"] == nachname:
                logging.info("compareUserDataToInput - if Vor und Nachname")
                returnVar.append(i["entries_id"])
        if len(returnVar) != 1:
            return "ERROR : Mehr als ein user mit dem gleichen Namen"
        return returnVar[0]

    @staticmethod
    def getUserIDAndData(nami, user, vorname, nachname):

        if user == []:
            return ["ERROR: No user!"]
        id = UserInfo.compareUserDataToInput(user, vorname, nachname)
        if isinstance(id, int) == True:
            return [id, nami.userById(id)]
        return [id]

    @staticmethod
    def getUserEfZInfo(nami, user):
        try:
            return nami.fuehrungsZeugnisInfo(user)[-1]["entries_erstelltAm"]
        except:
            return "Kein efz Eintrag!"

    @staticmethod
    def userTätigkeit(nami, userId, filterList, dateToCompare=0):
        for i in nami.taetigkeit(userId):
            for x in Utility.getIDsFromCsvAsList(filterList):
                if not x in i['entries_taetigkeit']:
                    continue
                if i["entries_aktivBis"] != "":
                    if not Utility.checkValidDate(i["entries_aktivBis"], dateToCompare):
                        continue
                return i['entries_taetigkeit']
        return "ERROR: keine Tätigkeit (ERROR)"
