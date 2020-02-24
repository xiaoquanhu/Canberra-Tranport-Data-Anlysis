import urllib.request
import os
import ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


url = 'https://www.data.act.gov.au/api/views/jxpp-4iiz/rows.csv?accessType=DOWNLOAD'
urllib.request.urlretrieve(
    url, 'Canberra_Metro_Light_Rail_Transit_Feed_-_Trip_Updates__Historical_Archive_.csv')


def run_solver(file_name: str):
    command = ['python modifiedcalculator.py',
               'python analysis.py', 'python showdata.py']
    for t in command:
        run_bash(t)


def run_bash(cmd: str):
    os.system(cmd)


run_solver('')
