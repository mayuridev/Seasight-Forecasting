
import configparser
import os

config = configparser.ConfigParser()
configFilePath = r'app.conf'
config.read(configFilePath)

server_IP = config['INSTALLATION']['server_IP']
project_location = config['INSTALLATION']['project_location']

os.system('source venv/bin/activate')
os.system('python manage.py runserver {}:8000'.format(server_IP))