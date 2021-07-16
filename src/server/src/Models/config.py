import json
from sys import argv
import os

def return_config():

    path = os.path.dirname(argv[0])+"\\config.json"

    if not os.path.exists(path):
        raise Exception("Arquivo de configuração não encontrado!")
    

    with open(path, 'r') as f:
        json_data = json.load(f)
    f.close()

    if(json_data['Network_Folder']) and (json_data['Credentials']['User'] == "") or (json_data['Credentials']['Password'] == ""):
        raise Exception('Opção de pasta em Rede esta habilitada, mas as credenciais para acesso não foram informadas!')
    return json_data

def return_oid():
    path = os.path.dirname(argv[0])+"\\PrintersOID.json"

    if not os.path.exists(path):
        raise Exception("Arquivo de OID não encontrado!")
    

    with open(path, 'r') as f:
        json_data = json.load(f)
    f.close()

    return json_data
