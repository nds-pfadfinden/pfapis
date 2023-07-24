# docs: https://doku.dpsg.de/display/NAMI/Service+Architektur
import json

import requests
from decouple import config
import urllib.parse
from datetime import datetime

class NamiResponseTypeError(Exception):
    pass


class NamiResponseSuccessError(Exception):
    """
    This is being raised when the response 'success' field is not True
    """
    pass


class NamiHTTPError(Exception):
    pass


def _check_response(response):
    if response.status_code != requests.codes.ok:  # pylint: disable=E1101
        raise NamiHTTPError('HTTP Error. Status Code: %s' %
                            response.status_code)

    rjson = response.json()
    if not rjson['success']:
        raise NamiResponseSuccessError(
            'succes state from NAMI was %s %s' % (rjson['message'], rjson))
    return rjson['data']


class Nami():

    def __init__(self, config):
        self.s = requests.Session()
        self.config = {
            'server': 'https://mv.meinbdp.de',
            'auth_url': '/ica/rest/nami/auth/manual/sessionStartup',
            'search_url': '/ica/rest/api/1/2/service/nami/search/result-list'
        }
        self.config.update(config)

    def auth(self, username, password):
        payload = {
            'Login': 'API',
            'username': username,
            'password': password
        }

        url = "%s%s" % (self.config['server'], self.config['auth_url'])
        r = self.s.post(url, data=payload)
        if r.status_code != 200:
            raise ValueError('authentication failed')
        return self.s

    # GET requests

    def search(self, parameter: dict, limit: int = 1):
        parameter["searchType"] = "MITGLIEDER"

        search_value = json.dumps(parameter)
        search_values = urllib.parse.quote(search_value)
        limit = int(limit)
        start = 0
        page = 1

        url = f'https://mv.meinbdp.de/ica/rest/nami/search-multi/result-list?_dc=1652274221216&searchedValues={search_values}&page={page}&start={start}&limit={limit}'
        r = self.s.request('GET', url)

        return _check_response(r)

    # url = f'https://mv.meinbdp.de/ica/rest/nami/search-multi/result-list?_dc=1636399371787&searchedValues=%7B%22vorname%22%3A%22{mitglied_vorname}%22%2C%22nachname%22%3A%22{mitglied_nachname}%22%2C%22spitzname%22%3A%22%22%2C%22mitgliedsNummber%22%3A%22%22%2C%22mglWohnort%22%3A%22%22%2C%22alterVon%22%3A%22%22%2C%22alterBis%22%3A%22%22%2C%22mglStatusId%22%3Anull%2C%22funktion%22%3A%22%22%2C%22mglTypeId%22%3A%5B%5D%2C%22organisation%22%3A%22%22%2C%22tagId%22%3A%5B%5D%2C%22bausteinIncludedId%22%3A%5B%5D%2C%22zeitschriftenversand%22%3Afalse%2C%22searchName%22%3A%22%22%2C%22taetigkeitId%22%3A%5B%5D%2C%22untergliederungId%22%3A%5B%5D%2C%22mitAllenTaetigkeiten%22%3Afalse%2C%22withEndedTaetigkeiten%22%3Afalse%2C%22ebeneId%22%3Anull%2C%22grpNummer%22%3A%22%22%2C%22grpName%22%3A%22%22%2C%22gruppierung1Id%22%3Anull%2C%22gruppierung2Id%22%3Anull%2C%22gruppierung3Id%22%3Anull%2C%22gruppierung4Id%22%3Anull%2C%22gruppierung5Id%22%3Anull%2C%22gruppierung6Id%22%3Anull%2C%22inGrp%22%3Afalse%2C%22unterhalbGrp%22%3Afalse%2C%22privacy%22%3A%22%22%2C%22searchType%22%3A%22MITGLIEDER%22%7D&page=1&start=0&limit=10'

    def user(self, mitglied_vorname, mitglied_nachname):
        search_params = {"vorname": mitglied_vorname, "nachname": mitglied_nachname}
        return self.search(search_params, 1)

    def usersbytaetigkeit(self, taetigkeit_id, method='GET'):
        search_params = {"taetigkeitId": taetigkeit_id}
        return self.search(search_params, limit=9999)

    def taetigkeit(self, mglid, method='GET'):
        url = "%s/ica/rest/nami/zugeordnete-taetigkeiten/filtered-for-navigation/gruppierung-mitglied/mitglied/%s/flist?_dc=1636459771397&page=1&start=0&limit=20" % (
            self.config['server'], mglid)
        r = self.s.request(method, url)
        return _check_response(r)

    def taetigkeitById(self, mglid, taetigkeitId, method='GET'):
        url = "%s/ica/rest/nami/zugeordnete-taetigkeiten/filtered-for-navigation/gruppierung-mitglied/mitglied/%s/flist?_dc=1636459771397&page=1&start=0&limit=20/%s" % (
            self.config['server'], mglid, taetigkeitId)
        r = self.s.request(method, url)
        return _check_response(r)

    def fuehrungsZeugnisInfo(self, mglied, method='GET'):
        url = "%s/ica/rest/nami/mitglied-sgb-acht/filtered-for-navigation/empfaenger/empfaenger/%s/flist?_dc = 1646639062672 & page = 1 & start = 0 & limit = 10" % (
            self.config['server'], mglied)
        r = self.s.request(method, url)
        return _check_response(r)

    def fuehrungsZeugnisGueltigkeit(self,mglied, gueltigkeit_jahre: int = 5,bezugs_datum=datetime.now()):
        """

        Check the validity of the documentation of an efz. The validity period can
        be handle over. The period is going to calculate with a timedelta in days divide with 365.25.

        @param mglied: id of the that has to check
        @param gueltigkeit_jahre: validity period of the documentation of the efz
        @return: string of [gültig,ungültig,n.e] based on the validity
        """
        efz_list = self.fuehrungsZeugnisInfo(mglied)

        if not efz_list:
            return 'n.e.'

        for efz in efz_list:

            entries_datum_einsicht = efz['entries_datumEinsicht']
            datum_ensicht = datetime.strptime(entries_datum_einsicht, "%Y-%m-%d %H:%M:%S")
            alter_einsicht_tage = (bezugs_datum - datum_ensicht).days
            alter_einsicht_jahre = alter_einsicht_tage/365.25

            # if one efz is valid, then end the loop and return
            if alter_einsicht_jahre < gueltigkeit_jahre:
                return 'gültig'

        return 'ungültig'

    def trainingById(self, memberId:int):
        """
        Return a list auf all trainings of one member, search by the member id
        @param memberId: MemberId (MitgliedsId)
        @return: list of trainings
        """
        url = f'https://mv.meinbdp.de/ica/rest/nami/mitglied-ausbildung/filtered-for-navigation/mitglied/mitglied/{memberId}/flist?_dc=1654165754686&page=1&start=0&limit=40'
        r = self.s.request('GET',url)
        return _check_response(r)

    def checkForTrainingname(self, memberId, trainingName):
        """
        Checks if a member has attended the trainings with the passed name.
        The method returns 'besucht' or 'n. besucht'.

        @param memberId: ID of the Member
        @param trainingName: Name of the training
        @return: return 'besucht' or 'n. besucht'
        """

        trainings = self.trainingById(memberId)

        for training in trainings:
            if training['entries_vstgName'] == trainingName:
                return 'besucht'

        return 'n.besucht'

    def userById(self, mglied, method="GET"):
        url = f'https://mv.meinbdp.de/ica/rest/nami/mitglied/filtered-for-navigation/gruppierung/gruppierung/253/{mglied}?_dc=1647435214372'
        r = self.s.request(method, url)
        return _check_response(r)
