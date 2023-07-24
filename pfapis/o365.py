import json
import secrets

import requests
from O365 import Account, Connection, MSGraphProtocol

GRAPH_URL = 'https://graph.microsoft.com/v1.0'
DEFAULT_LICENSE = "3b555118-da6a-4418-894f-7df1e2096870"
DEFAULT_PASSWORD_LENGTH = 14


class GroupNotFoundError(Exception):
    pass


class AuthenticatedConnection:

    def __authenticate(self, cliend_id, client_secret) -> Account:

        credentials = (cliend_id, client_secret)
        account = Account(credentials)

        if not account.is_authenticated:
            if account.authenticate(scopes=['basic', 'message_all']):
                print('Authenticated!')
            else:
                raise ConnectionError('Connection to the o365 is not possible')

        return account

    def graph_connection(self, cliend_id, client_secret) -> Connection:
        """
        Creates a Graph Connection with the given Secrets

        Args:
            cliend_id (str): Client ID of the Graph App 
            client_secret (str): Client Secret of the Graph App

        Returns:
            Connection: MS Graph Connection.
        """
        self.__authenticate(cliend_id, client_secret)

        protocol = MSGraphProtocol()  # or maybe a user defined protocol
        con = Connection(('client_id', 'client_secret'), scopes=protocol.get_scopes_for(['...']))

        self.connection = con


class Utility(AuthenticatedConnection):

    def get_group_by_name(self, group_name: str) -> dict:
        """Returns Group Info
        Args:
            group_name (str): Name of the group as string

        Raises:
            TypeError: If group_name is not a str

        Returns:
            json: group info as dict
        """

        if not isinstance(group_name, str):
            raise TypeError

        url = f'{GRAPH_URL}/groups'

        resp = self.connection.get(url=url)

        for i in resp.json()["value"]:
            if i["displayName"] == group_name:
                return i

        raise GroupNotFoundError(f'The group "{group_name}" does not exist in this organization!')

    def add_single_user_to_group(self, group_name: str, user_email: str) -> str:
        """ Adds single Users to O365 Group

        Args:
            group_name (str): name of the group as string
            user_emails (list): List of all users emails to be added to the group
        Raises:
            TypeError: If group_id is not a str
            TypeError: If user_emails ist not a str
        Returns:
            Status if user was added as str:
             - User {user_email} was added to the group.
             - User {user_email} is already in the group.

        """
        if not isinstance(group_name, str):
            raise TypeError
        if not isinstance(user_email, str):
            raise TypeError

        group_id = self.get_group_by_name(group_name=group_name)["id"]
        temp_user_id = self.user_information(user=user_email)["id"]
        data = {
            "members@odata.bind": [f'https://graph.microsoft.com/v1.0/directoryObjects/{temp_user_id}']
        }
        url = f'{GRAPH_URL}/groups/{group_id}'

        try:
            self.connection.patch(url=url, data=data)

        except requests.HTTPError as err:
            if err.response.json()["error"]["message"] == "One or more added object references already exist for the following modified properties: 'members'.":
                return f'User {user_email} is already in the group.'

            else:
                raise

        return f'User {user_email} was added to the group.'


class O365(Utility):

    def write_email(self,message:str,subject:str, to:list, cc:list,sender_address=None,user=None):
        """ Write an E-Mail

        Args:
            message (str): Message (body) of the E-Mail
            subject (str): Subject of the E-Mail
            to (list): List of Recipients
            cc (list): List of E-Mails for cc
            sender_address (str): From Address, otherwise use the users E-Mail

        """

        if user:
            url = f"{GRAPH_URL}/{user}/sendMail"
        else:
            url = f"{GRAPH_URL}/me/sendMail"
        data= {}
        content={}

        content['toRecipients'] = [{"emailAddress": {"address": item }} for item in to ]
        content['ccRecipients'] = [{"emailAddress": {"address": item}} for item in cc]
        if sender_address:
            content['from'] = { "emailAddress": {"address": sender_address } }
        content['body'] = {"contentType": "HTML", "content": message}
        content['subject'] = subject
        data['message']= content
        data['saveToSentItems'] = True
        self.connection.post(url=url, data=data)
