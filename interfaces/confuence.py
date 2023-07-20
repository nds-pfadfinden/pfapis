from xmlrpc.client import boolean
from atlassian import Confluence as AtlassianConf
import pandas as pd
from datetime import datetime
import time


class Confluence:

    def __init__(self, url, username, password) -> None:

        self.c = AtlassianConf(
            url=url,
            username=username,
            password=password
        )

    def attach_file(self, content: pd.DataFrame, page_id: int, title: str) -> None:
        """Attach the content as a Datafram as csv and xlsx file to the given page

        Args:
            content (pd.DataFrame): Content of for generating the file
            page_id (int): ID of the Page
            title (str): Title for the file Name
        """

        file_title = title.lower()
        file_title = file_title.replace(' ', '_')
        csv_file = f'/tmp/{file_title}.csv'
        excel_file = f'/tmp/{file_title}.xlsx'
        content.to_csv(csv_file)
        content.to_excel(excel_file)

        self.c.attach_file(csv_file, name=None, content_type=None, page_id=page_id, title=None, space=None,
                           comment=None)
        self.c.attach_file(excel_file, name=None, content_type=None, page_id=page_id, title=None, space=None,
                           comment=None)

    def get_data_from_page(self,page_id:int):

        page = self.c.get_page_by_id(page_id=page_id, expand="body.storage")
        content = page['body']['storage']['value']
        return pd.read_html(content)[0]

    def uplaod_data_to_page(self, content: (pd.DataFrame, str), page_id: int, parent_id: int, title: str, note: str = None,
                            header: str = None, upload_file: boolean = False):
        """Add the given Dataframe as Table to a confluence Page. Notice: The Page must be exist.

        Args:
            content (pd.DataFrame): Content to Add to the Page
            page_id (int): PageID of the Page
            parent_id (int): ParentPageID of the Page
            title (str): Title of Page
            note (str, optional): Note at the Head of the Page in Boxes. Defaults to None.
            header (str, optional): Some Text above the actual Data. Defaults to None.
            upload_file (boolean, optional): If true add the Data as a csv and excel to the Page. Defaults to False.
        """

        page_id = int(page_id)
        title = str(title)
        new_page_content = ''

        if note:
            new_page_content = new_page_content + f'<div class="confluence-information-macro ' \
                                                  f'confluence-information-macro-information conf-macro output-block" ' \
                                                  f'data-hasbody="true" data-macro-name="info"><span class="aui-icon ' \
                                                  f'aui-icon-small aui-iconfont-info ' \
                                                  f'confluence-information-macro-icon"> </span><div ' \
                                                  f'class="confluence-information-macro-body"><p>' \
                                                  f'{note}</p></div></div> '

        timestamp = str(datetime.now())
        t_header = f'Stand der Daten: {timestamp}'
        new_page_content = new_page_content + f'<p>{t_header}</p>\n'

        if header:
            new_page_content = new_page_content + header + '\n'

        if content is None:
            return
        if  isinstance(content,pd.DataFrame):
            new_page_content = new_page_content + content.to_html()
        else:
            new_page_content = new_page_content + content

        if upload_file:
            self.attach_file(content=content, page_id=page_id, title=title)

        self.c.update_page(
            page_id=page_id,
            body=new_page_content,
            parent_id=parent_id,
            type='page',
            title=title
        )
