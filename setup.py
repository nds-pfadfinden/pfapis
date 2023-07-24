from setuptools import find_packages, setup

setup(name="Pfadi Apis",
      version="0.1",
      description="Internal lib to interact with system in a scouts context",
      author='Umberto Albano',
      author_email='umberto.albano@nds.pfadfinden.de',
      packages=find_packages(exclude=("test",)),
      install_requires=["python-docx" ,"html5lib","O365","openpyxl", "requests", "python-decouple","pandas","atlassian-python-api","httplib2","lxml","urllib3"],
      extras_require={
          'opt1': ['autopep8'],
      }
      )
