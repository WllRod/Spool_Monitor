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

    return json_data
