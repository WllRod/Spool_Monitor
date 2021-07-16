"""
DESCRIÇÃO: IRÁ GERAR E ENVIAR O LOG DE ERRO E FINALIZARÁ A EXECUÇÃO DA API
_____________________________________________________________________________
AUTOR: WILLIAM RODRIGUES
_____________________________________________________________________________
DATA: 08/07/2021
"""

from datetime import date, datetime
from components.Config import returnConfig
import requests


def ErrorLog(**kwargs):
    """
    Gerará o texto de log e tombará a execução da API
    params: **kwargs -> dicionario de dados
    """
    data_atual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    text = f"[{data_atual}]\n"
    for keys, values in kwargs.items():
        text += f"{keys}: {values}\n"
    
    server = returnConfig()["SERVER"]
    requests.get(server+"/sendClientErrorLog", json={"Message": text})
    #send_email(text, "Monitorador De Spool - Client")
    

