"""
DESCRIÇÃO:  FONTE RESPONSÁVEL PELA LEITURA DO ARQUIVO DE CONFIGURAÇÃO
            E REALIZAR A CONFIGURAÇÃO INICIAL DA API 
______________________________________________________________________

AUTOR: WILLIAM RODRIGUES

______________________________________________________________________

DATA: 08/07/2021

"""


from flask import Flask
from Models import return_config
import subprocess
from Error import ErrorLog
import sys
import os

def generate_error(error):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__)
    
    ErrorLog(
        Error=error,
        Script=filename,
        Line=exc_tb.tb_lineno
    )

try:
    configs = return_config()

    if(configs['Network_Folder']):
        user = configs['Credentials']['User']
        password = configs['Credentials']['Password']
        subprocess.Popen("net use {} /User:{} {}".format(
            configs['UPLOAD_FOLDER'],
            user,
            password
            ), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            stdin=subprocess.DEVNULL, 
            shell=True
        )
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = configs['UPLOAD_FOLDER']
except Exception as e:
    generate_error(e)
    
from .Routes import Routes