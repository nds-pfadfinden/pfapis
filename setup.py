from setuptools import find_packages, setup

setup(name="Lib Interfaces",
      version="1.0",
      description="Internal lib for the important inferfaces",
      packages=find_packages(exclude=("test",)),
      install_requires=["python-docx" ,"html5lib","O365","openpyxl", "requests", "python-decouple","pandas","atlassian-python-api","httplib2","lxml","urllib3"],
      extras_require={
          'opt1': ['autopep8'],
      }
      )
