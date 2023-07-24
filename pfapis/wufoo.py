import api.pyfoo
import pandas as pd


def search_for_field_id(fields, id: str):

    for field in fields:
        for subfield in field.SubFields:
            if id == subfield.ID:   
                return f"{field.Title}_{subfield.Label}".replace(" ","_")
        if id == field.ID:   
            return field.Title

class Wufoo:

    def __init__(self, account: str, api_key: str):
        self.__api = api.pyfoo.PyfooAPI(account, api_key)

    def get_entries_of_form(self, form_name: str) -> pd.DataFrame:
        """
        Returns every finished Entries in a Wufoo Form

        @param form_name: Name of the Form in Wufoo
        @return: pandas.Dataframe
        """
        entries = pd.DataFrame
        contact_form = None
        # print(self.__api.forms)
        for form in self.__api.forms:
            if form.Name == form_name:
                contact_form = form

        entries = self.make_dataframe(contact_form)
        return entries

    @staticmethod
    def make_dataframe(raw_entries: api.pyfoo.pyfoo.Form) -> pd.DataFrame:

        fields = raw_entries.fields
        entries = pd.DataFrame.from_dict(raw_entries.get_entries())
        
        rename_map = {}
        columns = entries.columns.values.tolist()
        for column in columns:
            field_name = search_for_field_id(fields,column)
            if field_name:
                rename_map[column] = field_name
        entries = entries.rename(columns=rename_map)
        if entries.empty:
            return entries
        if 'IP' in entries.keys():
            del entries['IP']
        if 'Immutable' in entries.keys():
            del entries['Immutable']
        complete_entries = entries[entries['CompleteSubmission'] == '1']
        return complete_entries

    def forms(self):
        return self.__api.forms
